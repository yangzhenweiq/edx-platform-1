import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from django.conf import settings


class AESCipher(object):

    @classmethod
    def encrypt(cls, raw):
        if raw is None:
            return raw
        key = hashlib.sha256(settings.AES_KEY).digest()
        raw = cls._pad(raw)        
        # iv = Random.new().read(AES.block_size)
        # use settings iv instead of random to produce same result
        iv = settings.AES_IV
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    @classmethod
    def decrypt(cls, enc):
        if enc is None:
            return enc
        key = hashlib.sha256(settings.AES_KEY).digest()
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return cls._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    @classmethod
    def _pad(cls, s):
        bs = AES.block_size
        return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)

    @classmethod
    def _unpad(cls, s):
        return s[:-ord(s[len(s) - 1:])]
