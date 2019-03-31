# -*- coding: utf-8 -*-
#__Author__= allisnone #2019-02-16
"""
加解密
"""
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64

def aes_cbc_encrypt(message, key):
    '''
    use AES CBC to encrypt message, using key and init vector
    :param message: the message to encrypt
    :param key: the secret  key = '1234567890!@#$%^' 
    :return: bytes init_vector + encrypted_content
    '''
    iv_len = 16
    assert type(message) in (str,bytes)
    assert type(key) in (str,bytes)
    if type(message) == str:
        message = bytes(message, 'utf-8')
    if type(key) == str:
        key = bytes(key, 'utf-8')
    backend = default_backend()
    iv = os.urandom(iv_len)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(message) + padder.finalize()
    enc_content = encryptor.update(padded_data) + encryptor.finalize()
    return iv + enc_content

def aes_cbc_decrypt(content, key=b'MTIzNDU2Nzg5MCFAIyQlXg=='):
    '''
    use AES CBC to decrypt message, using key
    :param content: the encrypted content using the above protocol
    :param key: the secret
    :return: decrypted bytes
    '''
    assert type(content) == bytes
    key = base64.decodestring(key).decode('utf-8')
    assert type(key) in (bytes, str)
    if type(key) == str:
        key = bytes(key, 'utf-8')
    iv_len = 16
    assert len(content) >= (iv_len + 16)
    iv = content[:iv_len]
    enc_content = content[iv_len:]
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    unpadder = padding.PKCS7(128).unpadder()
    decryptor = cipher.decryptor()
    dec_content = decryptor.update(enc_content) + decryptor.finalize()
    real_content = unpadder.update(dec_content) + unpadder.finalize()
    return real_content

#from apappwebibs.crypto_sign import *
def get_random_key_readable(key_size=256):
    '''
    get random key for symmetric encryption
    with key_size bits
    :param key_size: bit length of the key
    :return: bytes key
    '''
    # length for urandom
    ulen = int(key_size/8/4*3)
    key = base64.b64encode(os.urandom(ulen))
    return key

#bs = base64.b64encode(bytes('abcde1@163.com','ascii'))
#print(bs)
#base64.decodestring(bs).decode('utf-8')
                 