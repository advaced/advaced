from base64 import b64encode, b64decode
from hashlib import sha3_256

from Crypto import Random
from Crypto.Cipher import AES


class AESCipher:
    def __init__(self, key):
        self.bs = AES.block_size
        self.key = sha3_256(key.encode()).digest()

    def encrypt(self, data: str):
        init_vector = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, init_vector)

        return b64encode(init_vector + cipher.encrypt(self._pad(data).encode()))

    def decrypt(self, token: str):
        encoded = b64decode(token)

        init_vector = encoded[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, init_vector)

        return self._unpad(cipher.decrypt(encoded[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]
