from bcrypt import gensalt, hashpw, checkpw

from util.crypto.aes import AESCipher


def encrypt_data(data: str, key: str):
    """Encrypt data with help of a key

    :param data: Data to encrypt.
    :type data: str
    :param key: Key to encrypt with.
    :type key: str

    :returns: Encrypted data.
    :rtype: str
    """
    cipher = AESCipher(key)

    return cipher.encrypt(data).decode()


def decrypt_data(token: str, key: str):
    """Decrypt data with help of a key

    :param token: Token to decrypt.
    :type token: str
    :param key: Key to decrypt with.
    :type key: str

    :returns: Decrypted data.
    :rtype: str
    """
    cipher = AESCipher(key)

    return cipher.decrypt(token)


def hash_password(password: str) -> str:
    """Hash the password with bcrypt and salt.

    :param password: Password to hash
    :type password: str

    :return: Hashed password
    :rtype: str
    """
    return hashpw(password.encode('utf-8'), gensalt(rounds=14)).decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    """Hash the password with bcrypt and salt.

    :param password: Used password
    :type password: str
    :param hashed_password: Bcrypt hash of the password
    :type hashed_password: str

    :return: Validity of the password
    :rtype: bool
    """
    return checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
