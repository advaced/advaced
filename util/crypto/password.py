import secrets
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
from bcrypt import gensalt, hashpw, checkpw

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

BACKEND = default_backend()
ITERATIONS = 100_000


def _derive_key(password: bytes, salt: bytes, iterations: int = ITERATIONS) -> bytes:
    """Derive a secret key from a given password and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt,
        iterations=iterations, backend=BACKEND)
    return b64e(kdf.derive(password))


def encrypt_data(data: str, password: str) -> str:
    """Encrypt data with help of a key

    :param data: Data to encrypt.
    :type data: str
    :param password: Key to encrypt with.
    :type password: str

    :returns: Encrypted data.
    :rtype: str
    """
    salt = secrets.token_bytes(16)
    key = _derive_key(password.encode(), salt, ITERATIONS)

    return b64e(b'%b%b%b' % (salt, ITERATIONS.to_bytes(4, 'big'), b64d(Fernet(key).encrypt(data.encode('utf-8'))),)) \
        .decode('utf-8')


def decrypt_data(token: str, password: str) -> str:
    """Decrypt data with help of a key

    :param token: Token to decrypt.
    :type token: str
    :param password: Key to decrypt with.
    :type password: str

    :returns: Decrypted data.
    :rtype: str
    """
    decoded = b64d(token.encode('utf-8'))
    salt, iterations, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
    iterations = int.from_bytes(iterations, 'big')

    key = _derive_key(password.encode('utf-8'), salt, iterations)

    return Fernet(key).decrypt(token).decode('utf-8')


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
