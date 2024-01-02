"""An AEAD style OpenSSL wrapper

API:

    encrypt(data, header=b'', aad_offset=0) -> envelope
    decrypt(envelope, header_len=0, aad_offset=0) -> data

Envelope layout:

|<--------------------------- envelope ------------------------------------------>|
|<------------ header ----------->|<---------- ciphersuite specific ------------->|
|<-- not auth data -->|<-- aad -->|<-- e.g.:  S(aad, iv, E(data)), iv, E(data) -->|

|--- #aad_offset ---->|
|------------- #header_len ------>|

S means a cryptographic signature function (like HMAC or GMAC).
E means a encryption function (like AES).
iv is the initialization vector / nonce, if needed.

The split of header into not authenticated data and aad (additional authenticated
data) is done to support the legacy envelope layout as used in attic and early borg
(where the TYPE byte was not authenticated) and avoid unneeded memcpy and string
garbage.

Newly designed envelope layouts can just authenticate the whole header.

IV handling:

    iv = ...  # just never repeat!
    cs = CS(hmac_key, enc_key, iv=iv)
    envelope = cs.encrypt(data, header, aad_offset)
    iv = cs.next_iv(len(data))
    (repeat)
"""

import hashlib
import hmac
from math import ceil

from cpython cimport PyMem_Malloc, PyMem_Free
from cpython.buffer cimport PyBUF_SIMPLE, PyObject_GetBuffer, PyBuffer_Release
from cpython.bytes cimport PyBytes_FromStringAndSize

API_VERSION = '1.2_01'

cdef extern from "openssl/crypto.h":
    int CRYPTO_memcmp(const void *a, const void *b, size_t len)


cdef extern from "openssl/evp.h":
    ctypedef struct EVP_MD:
        pass
    ctypedef struct EVP_CIPHER:
        pass
    ctypedef struct EVP_CIPHER_CTX:
        pass
    ctypedef struct ENGINE:
        pass

    const EVP_CIPHER *EVP_aes_256_ctr()

    EVP_CIPHER_CTX *EVP_CIPHER_CTX_new()
    void EVP_CIPHER_CTX_free(EVP_CIPHER_CTX *a)
    void EVP_CIPHER_CTX_init(EVP_CIPHER_CTX *a)
    void EVP_CIPHER_CTX_cleanup(EVP_CIPHER_CTX *a)

    int EVP_EncryptInit_ex(EVP_CIPHER_CTX *ctx, const EVP_CIPHER *cipher, ENGINE *impl,
                           const unsigned char *key, const unsigned char *iv)
    int EVP_DecryptInit_ex(EVP_CIPHER_CTX *ctx, const EVP_CIPHER *cipher, ENGINE *impl,
                           const unsigned char *key, const unsigned char *iv)
    int EVP_EncryptUpdate(EVP_CIPHER_CTX *ctx, unsigned char *out, int *outl,
                          const unsigned char *in_, int inl)
    int EVP_DecryptUpdate(EVP_CIPHER_CTX *ctx, unsigned char *out, int *outl,
                          const unsigned char *in_, int inl)
    int EVP_EncryptFinal_ex(EVP_CIPHER_CTX *ctx, unsigned char *out, int *outl)
    int EVP_DecryptFinal_ex(EVP_CIPHER_CTX *ctx, unsigned char *out, int *outl)

    int EVP_CIPHER_CTX_ctrl(EVP_CIPHER_CTX *ctx, int type, int arg, void *ptr)

    const EVP_MD *EVP_sha256() nogil


cdef extern from "_crypto_helpers.h":
    long OPENSSL_VERSION_NUMBER


import struct

_int = struct.Struct('>I')
_long = struct.Struct('>Q')

bytes_to_int = lambda x, offset=0: _int.unpack_from(x, offset)[0]
bytes_to_long = lambda x, offset=0: _long.unpack_from(x, offset)[0]
long_to_bytes = lambda x: _long.pack(x)


def num_cipher_blocks(length, blocksize=16):
    """Return the number of cipher blocks required to encrypt/decrypt <length> bytes of data.

    For a precise computation, <blocksize> must be the used cipher's block size (AES: 16).

    For a safe-upper-boundary computation, <blocksize> must be the MINIMUM of the block sizes (in
    bytes) of ALL supported ciphers. This can be used to adjust a counter if the used cipher is not
    known (yet).
    The default value of blocksize must be adjusted so it reflects this minimum, so a call of this
    function without a blocksize is "safe-upper-boundary by default".

    Padding cipher modes are not supported.
    """
    return (length + blocksize - 1) // blocksize


class CryptoError(Exception):
    """Malfunction in the crypto module."""


class IntegrityError(CryptoError):
    """Integrity checks failed. Corrupted or tampered data."""


cdef Py_buffer ro_buffer(object data) except *:
    cdef Py_buffer view
    PyObject_GetBuffer(data, &view, PyBUF_SIMPLE)
    return view


class UNENCRYPTED:
    # Layout: HEADER + PlainText

    def __init__(self, mac_key, enc_key, iv=None, header_len=1, aad_offset=1):
        assert mac_key is None
        assert enc_key is None
        self.header_len = header_len
        self.set_iv(iv)

    def encrypt(self, data, header=b'', iv=None):
        """
        IMPORTANT: it is called encrypt to satisfy the crypto api naming convention,
        but this does NOT encrypt and it does NOT compute and store a MAC either.
        """
        if iv is not None:
            self.set_iv(iv)
        assert self.iv is not None, 'iv needs to be set before encrypt is called'
        return header + data

    def decrypt(self, envelope):
        """
        IMPORTANT: it is called decrypt to satisfy the crypto api naming convention,
        but this does NOT decrypt and it does NOT verify a MAC either, because data
        is not encrypted and there is no MAC.
        """
        return memoryview(envelope)[self.header_len:]

    def block_count(self, length):
        return 0

    def set_iv(self, iv):
        self.iv = iv

    def next_iv(self):
        return self.iv

    def extract_iv(self, envelope):
        return 0


cdef class AES256_CTR_BASE:
    # Layout: HEADER + MAC 32 + IV 8 + CT (same as attic / borg < 1.2 IF HEADER = TYPE_BYTE, no AAD)

    cdef EVP_CIPHER_CTX *ctx
    cdef unsigned char enc_key[32]
    cdef int cipher_blk_len
    cdef int iv_len, iv_len_short
    cdef int aad_offset
    cdef int header_len
    cdef int mac_len
    cdef unsigned char iv[16]
    cdef long long blocks

    @classmethod
    def requirements_check(cls):
        if OPENSSL_VERSION_NUMBER < 0x10000000:
            raise ValueError('AES CTR requires OpenSSL >= 1.0.0. Detected: OpenSSL %08x' % OPENSSL_VERSION_NUMBER)

    def __init__(self, mac_key, enc_key, iv=None, header_len=1, aad_offset=1):
        self.requirements_check()
        assert isinstance(enc_key, bytes) and len(enc_key) == 32
        self.cipher_blk_len = 16
        self.iv_len = sizeof(self.iv)
        self.iv_len_short = 8
        assert aad_offset <= header_len
        self.aad_offset = aad_offset
        self.header_len = header_len
        self.mac_len = 32
        self.enc_key = enc_key
        if iv is not None:
            self.set_iv(iv)
        else:
            self.blocks = -1  # make sure set_iv is called before encrypt

    def __cinit__(self, mac_key, enc_key, iv=None, header_len=1, aad_offset=1):
        self.ctx = EVP_CIPHER_CTX_new()

    def __dealloc__(self):
        EVP_CIPHER_CTX_free(self.ctx)

    cdef mac_compute(self, const unsigned char *data1, int data1_len,
                     const unsigned char *data2, int data2_len,
                     unsigned char *mac_buf):
        raise NotImplementedError

    cdef mac_verify(self, const unsigned char *data1, int data1_len,
                    const unsigned char *data2, int data2_len,
                    unsigned char *mac_buf, const unsigned char *mac_wanted):
        """
        Calculate MAC of *data1*, *data2*, write result to *mac_buf*, and verify against *mac_wanted.*
        """
        raise NotImplementedError

    def encrypt(self, data, header=b'', iv=None):
        """
        encrypt data, compute mac over aad + iv + cdata, prepend header.
        aad_offset is the offset into the header where aad starts.
        """
        if iv is not None:
            self.set_iv(iv)
        assert self.blocks == 0, 'iv needs to be set before encrypt is called'
        cdef int ilen = len(data)
        cdef int hlen = len(header)
        assert hlen == self.header_len
        cdef int aoffset = self.aad_offset
        cdef int alen = hlen - aoffset
        cdef unsigned char *odata = <unsigned char *>PyMem_Malloc(hlen + self.mac_len + self.iv_len_short +
                                                                  ilen + self.cipher_blk_len)  # play safe, 1 extra blk
        if not odata:
            raise MemoryError
        cdef int olen
        cdef int offset
        cdef Py_buffer idata = ro_buffer(data)
        cdef Py_buffer hdata = ro_buffer(header)
        try:
            offset = 0
            for i in range(hlen):
                odata[offset+i] = header[i]
            offset += hlen
            offset += self.mac_len
            self.store_iv(odata+offset, self.iv)
            offset += self.iv_len_short
            rc = EVP_EncryptInit_ex(self.ctx, EVP_aes_256_ctr(), NULL, self.enc_key, self.iv)
            if not rc:
                raise CryptoError('EVP_EncryptInit_ex failed')
            rc = EVP_EncryptUpdate(self.ctx, odata+offset, &olen, <const unsigned char*> idata.buf, ilen)
            if not rc:
                raise CryptoError('EVP_EncryptUpdate failed')
            offset += olen
            rc = EVP_EncryptFinal_ex(self.ctx, odata+offset, &olen)
            if not rc:
                raise CryptoError('EVP_EncryptFinal_ex failed')
            offset += olen
            self.mac_compute(<const unsigned char *> hdata.buf+aoffset, alen,
                              odata+hlen+self.mac_len, offset-hlen-self.mac_len,
                              odata+hlen)
            self.blocks += self.block_count(ilen)
            return odata[:offset]
        finally:
            PyMem_Free(odata)
            PyBuffer_Release(&hdata)
            PyBuffer_Release(&idata)

    def decrypt(self, envelope):
        """
        authenticate aad + iv + cdata, decrypt cdata, ignore header bytes up to aad_offset.
        """
        cdef int ilen = len(envelope)
        cdef int hlen = self.header_len
        assert hlen == self.header_len
        cdef int aoffset = self.aad_offset
        cdef int alen = hlen - aoffset
        cdef unsigned char *odata = <unsigned char *>PyMem_Malloc(ilen + self.cipher_blk_len)  # play safe, 1 extra blk
        if not odata:
            raise MemoryError
        cdef int olen
        cdef int offset
        cdef unsigned char mac_buf[32]
        assert sizeof(mac_buf) == self.mac_len
        cdef Py_buffer idata = ro_buffer(envelope)
        try:
            self.mac_verify(<const unsigned char *> idata.buf+aoffset, alen,
                             <const unsigned char *> idata.buf+hlen+self.mac_len, ilen-hlen-self.mac_len,
                             mac_buf, <const unsigned char *> idata.buf+hlen)
            iv = self.fetch_iv(<unsigned char *> idata.buf+hlen+self.mac_len)
            self.set_iv(iv)
            if not EVP_DecryptInit_ex(self.ctx, EVP_aes_256_ctr(), NULL, self.enc_key, iv):
                raise CryptoError('EVP_DecryptInit_ex failed')
            offset = 0
            rc = EVP_DecryptUpdate(self.ctx, odata+offset, &olen,
                                   <const unsigned char*> idata.buf+hlen+self.mac_len+self.iv_len_short,
                                   ilen-hlen-self.mac_len-self.iv_len_short)
            if not rc:
                raise CryptoError('EVP_DecryptUpdate failed')
            offset += olen
            rc = EVP_DecryptFinal_ex(self.ctx, odata+offset, &olen)
            if rc <= 0:
                raise CryptoError('EVP_DecryptFinal_ex failed')
            offset += olen
            self.blocks += self.block_count(offset)
            return odata[:offset]
        finally:
            PyMem_Free(odata)
            PyBuffer_Release(&idata)

    def block_count(self, length):
        return num_cipher_blocks(length, self.cipher_blk_len)

    def set_iv(self, iv):
        # set_iv needs to be called before each encrypt() call
        if isinstance(iv, int):
            iv = iv.to_bytes(self.iv_len, byteorder='big')
        assert isinstance(iv, bytes) and len(iv) == self.iv_len
        self.iv = iv
        self.blocks = 0  # how many AES blocks got encrypted with this IV?

    def next_iv(self):
        # call this after encrypt() to get the next iv (int) for the next encrypt() call
        iv = int.from_bytes(self.iv[:self.iv_len], byteorder='big')
        return iv + self.blocks

    cdef fetch_iv(self, unsigned char * iv_in):
        # fetch lower self.iv_len_short bytes of iv and add upper zero bytes
        return b'\0' * (self.iv_len - self.iv_len_short) + iv_in[0:self.iv_len_short]

    cdef store_iv(self, unsigned char * iv_out, unsigned char * iv):
        # store only lower self.iv_len_short bytes, upper bytes are assumed to be 0
        cdef int i
        for i in range(self.iv_len_short):
            iv_out[i] = iv[(self.iv_len-self.iv_len_short)+i]

    def extract_iv(self, envelope):
        offset = self.header_len + self.mac_len
        return bytes_to_long(envelope[offset:offset+self.iv_len_short])


cdef class AES256_CTR_HMAC_SHA256(AES256_CTR_BASE):
    cdef unsigned char mac_key[32]

    def __init__(self, mac_key, enc_key, iv=None, header_len=1, aad_offset=1):
        assert isinstance(mac_key, bytes) and len(mac_key) == 32
        self.mac_key = mac_key
        super().__init__(mac_key, enc_key, iv=iv, header_len=header_len, aad_offset=aad_offset)

    def __cinit__(self, mac_key, enc_key, iv=None, header_len=1, aad_offset=1):
        pass

    def __dealloc__(self):
        pass

    cdef mac_compute(self, const unsigned char *data1, int data1_len,
                     const unsigned char *data2, int data2_len,
                     unsigned char *mac_buf):
        data = data1[:data1_len] + data2[:data2_len]
        mac = hmac.digest(self.mac_key[:self.mac_len], data, 'sha256')
        for i in range(self.mac_len):
            mac_buf[i] = mac[i]

    cdef mac_verify(self, const unsigned char *data1, int data1_len,
                    const unsigned char *data2, int data2_len,
                    unsigned char *mac_buf, const unsigned char *mac_wanted):
        self.mac_compute(data1, data1_len, data2, data2_len, mac_buf)
        if CRYPTO_memcmp(mac_buf, mac_wanted, self.mac_len):
            raise IntegrityError('MAC Authentication failed')


cdef class AES256_CTR_BLAKE2b(AES256_CTR_BASE):
    cdef unsigned char mac_key[128]

    def __init__(self, mac_key, enc_key, iv=None, header_len=1, aad_offset=1):
        assert isinstance(mac_key, bytes) and len(mac_key) == 128
        self.mac_key = mac_key
        super().__init__(mac_key, enc_key, iv=iv, header_len=header_len, aad_offset=aad_offset)

    def __cinit__(self, mac_key, enc_key, iv=None, header_len=1, aad_offset=1):
        pass

    def __dealloc__(self):
        pass

    cdef mac_compute(self, const unsigned char *data1, int data1_len,
                     const unsigned char *data2, int data2_len,
                     unsigned char *mac_buf):
        data = self.mac_key[:128] + data1[:data1_len] + data2[:data2_len]
        mac = hashlib.blake2b(data, digest_size=self.mac_len).digest()
        for i in range(self.mac_len):
            mac_buf[i] = mac[i]

    cdef mac_verify(self, const unsigned char *data1, int data1_len,
                    const unsigned char *data2, int data2_len,
                    unsigned char *mac_buf, const unsigned char *mac_wanted):
        self.mac_compute(data1, data1_len, data2, data2_len, mac_buf)
        if CRYPTO_memcmp(mac_buf, mac_wanted, self.mac_len):
            raise IntegrityError('MAC Authentication failed')


ctypedef const EVP_CIPHER * (* CIPHER)()


cdef class AES:
    """A thin wrapper around the OpenSSL EVP cipher API - for legacy code, like key file encryption"""
    cdef CIPHER cipher
    cdef EVP_CIPHER_CTX *ctx
    cdef unsigned char enc_key[32]
    cdef int cipher_blk_len
    cdef int iv_len
    cdef unsigned char iv[16]
    cdef long long blocks

    def __init__(self, enc_key, iv=None):
        assert isinstance(enc_key, bytes) and len(enc_key) == 32
        self.enc_key = enc_key
        self.iv_len = 16
        assert sizeof(self.iv) == self.iv_len
        self.cipher = EVP_aes_256_ctr
        self.cipher_blk_len = 16
        if iv is not None:
            self.set_iv(iv)
        else:
            self.blocks = -1  # make sure set_iv is called before encrypt

    def __cinit__(self, enc_key, iv=None):
        self.ctx = EVP_CIPHER_CTX_new()

    def __dealloc__(self):
        EVP_CIPHER_CTX_free(self.ctx)

    def encrypt(self, data, iv=None):
        if iv is not None:
            self.set_iv(iv)
        assert self.blocks == 0, 'iv needs to be set before encrypt is called'
        cdef Py_buffer idata = ro_buffer(data)
        cdef int ilen = len(data)
        cdef int offset
        cdef int olen = 0
        cdef unsigned char *odata = <unsigned char *>PyMem_Malloc(ilen + self.cipher_blk_len)
        if not odata:
            raise MemoryError
        try:
            if not EVP_EncryptInit_ex(self.ctx, self.cipher(), NULL, self.enc_key, self.iv):
                raise Exception('EVP_EncryptInit_ex failed')
            offset = 0
            if not EVP_EncryptUpdate(self.ctx, odata, &olen, <const unsigned char*> idata.buf, ilen):
                raise Exception('EVP_EncryptUpdate failed')
            offset += olen
            if not EVP_EncryptFinal_ex(self.ctx, odata+offset, &olen):
                raise Exception('EVP_EncryptFinal failed')
            offset += olen
            self.blocks = self.block_count(offset)
            return odata[:offset]
        finally:
            PyMem_Free(odata)
            PyBuffer_Release(&idata)

    def decrypt(self, data):
        cdef Py_buffer idata = ro_buffer(data)
        cdef int ilen = len(data)
        cdef int offset
        cdef int olen = 0
        cdef unsigned char *odata = <unsigned char *>PyMem_Malloc(ilen + self.cipher_blk_len)
        if not odata:
            raise MemoryError
        try:
            # Set cipher type and mode
            if not EVP_DecryptInit_ex(self.ctx, self.cipher(), NULL, self.enc_key, self.iv):
                raise Exception('EVP_DecryptInit_ex failed')
            offset = 0
            if not EVP_DecryptUpdate(self.ctx, odata, &olen, <const unsigned char*> idata.buf, ilen):
                raise Exception('EVP_DecryptUpdate failed')
            offset += olen
            if EVP_DecryptFinal_ex(self.ctx, odata+offset, &olen) <= 0:
                # this error check is very important for modes with padding or
                # authentication. for them, a failure here means corrupted data.
                # CTR mode does not use padding nor authentication.
                raise Exception('EVP_DecryptFinal failed')
            offset += olen
            self.blocks = self.block_count(ilen)
            return odata[:offset]
        finally:
            PyMem_Free(odata)
            PyBuffer_Release(&idata)

    def block_count(self, length):
        return num_cipher_blocks(length, self.cipher_blk_len)

    def set_iv(self, iv):
        # set_iv needs to be called before each encrypt() call,
        # because encrypt does a full initialisation of the cipher context.
        if isinstance(iv, int):
            iv = iv.to_bytes(self.iv_len, byteorder='big')
        assert isinstance(iv, bytes) and len(iv) == self.iv_len
        self.iv = iv
        self.blocks = 0  # number of cipher blocks encrypted with this IV

    def next_iv(self):
        # call this after encrypt() to get the next iv (int) for the next encrypt() call
        iv = int.from_bytes(self.iv[:self.iv_len], byteorder='big')
        return iv + self.blocks



def hmac_sha256(key, data):
    return hmac.digest(key, data, 'sha256')


def blake2b_256(key, data):
    return hashlib.blake2b(key+data, digest_size=32).digest()


def blake2b_128(data):
    return hashlib.blake2b(data, digest_size=16).digest()


def hkdf_hmac_sha512(ikm, salt, info, output_length):
    """
    Compute HKDF-HMAC-SHA512 with input key material *ikm*, *salt* and *info* to produce *output_length* bytes.

    This is the "HMAC-based Extract-and-Expand Key Derivation Function (HKDF)" (RFC 5869)
    instantiated with HMAC-SHA512.

    *output_length* must not be greater than 64 * 255 bytes.
    """
    digest_length = 64
    assert output_length <= (255 * digest_length), 'output_length must be <= 255 * 64 bytes'
    # Step 1. HKDF-Extract (ikm, salt) -> prk
    if salt is None:
        salt = bytes(64)
    prk = hmac.HMAC(salt, ikm, hashlib.sha512).digest()

    # Step 2. HKDF-Expand (prk, info, output_length) -> output key
    n = ceil(output_length / digest_length)
    t_n = b''
    output = b''
    for i in range(n):
        msg = t_n + info + (i + 1).to_bytes(1, 'little')
        t_n = hmac.HMAC(prk, msg, hashlib.sha512).digest()
        output += t_n
    return output[:output_length]
