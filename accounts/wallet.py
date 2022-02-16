from ecdsa import SigningKey, VerifyingKey, SECP256k1
from hashlib import sha3_512

class Wallet:
    def __init__(self, name=None, public_key=None, private_key=None):
        self.name = name if name else 'Account'

        # Create wallet keypair (with ecdsa, the SECP256k1 curve and sha3-512 as hash-algorithm)
        verifying_key = SigningKey.generate(curve=SECP256k1, hashfunc=sha3_512)

        self.public_key = public_key if public_key else verifying_key.get_verifying_key().to_string().hex()
        self.private_key = private_key if private_key else verifying_key.to_string().hex()


    @staticmethod
    def sign_data(private_key: str, data: str):
        """Sign data (stringified) with string of private-key

        :param private_key: Private-key of the wallet.
        :type private_key: str (hex-digest)
        :param data: Data to sign.
        :type data: str (in most cases stringified json)

        :return: False when the key-fetching did not work.
        :rtype: bool
        :return: Signature of the data.
        :rtype: str (hex-digest)
        """

        # Fetch public-key from hex-string
        try:
            key = SigningKey.from_string(bytes.fromhex(private_key), curve=SECP256k1, hashfunc=sha3_512)

        except:
            return False

        # Create a signature
        signature = key.sign(bytes(data, 'utf-8'), hashfunc=sha3_512).hex()

        return signature


    @staticmethod
    def is_valid_signature(public_key: str, signature: str, data: str) -> bool:
        """Verify signature with the public_key.

        :param public_key: Public-key of the wallet.
        :type public_key: str (hex-digest)
        :param signature: Signature of the data with private-key that is paired with the parsed public-key.
        :type signature: str
        :param data: Data to sign.
        :type data: str (in most cases stringified json)

        :return: Wether the signature is valid or not or the key for it is valid.
        :rtype: bool
        """
        try:
            # Fetch public-key from hex-string
            key = VerifyingKey.from_string(bytes.fromhex(public_key), curve=SECP256k1, hashfunc=sha3_512)

            # Return the results
            return key.verify(bytes.fromhex(signature), bytes(data, 'utf-8'), hashfunc=sha3_512)

        except:
            return False


    @staticmethod
    def keypair_valid(public_key: str, private_key: str) -> bool:
        """Tests whether the keys are matching or not.

        :param public_key: Public-key from key-pair.
        :type public_key: str
        :param private_key: Private-key from key-pair.
        :type: str

        :return: The result wether the keys are matching or not.
        :rtype: bool
        """
        try:
            # Fetch private-key from hex-string
            secret = SigningKey.from_string(bytes.fromhex(private_key), curve=SECP256k1, hashfunc=sha3_512)

            # Check if public-key is valid
            if not secret.get_verifying_key().to_string().hex() == public_key:
                return False

            return True

        # Ouccurres when the private-key can not be fetched
        except:
            return False
