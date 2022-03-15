from ecdsa import SigningKey, VerifyingKey, SECP256k1
from hashlib import sha3_512


class Wallet:
    def __init__(self, public_key: VerifyingKey=None, private_key: SigningKey=None):
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
    def valid_signature(public_key: str, signature: str, data: str) -> bool:
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


    @classmethod
    def valid_versionstamp(cls, public_key: str, signature: str, version: str, timestamp: str, network: str) -> bool:
        """Verify a versionstamp from a developer-key signature (Warning: This function does not check the validity of
           the public-key as a developer key!).

        :param public_key: Public-key of the wallet.
        :type public_key: str (hex-digest)
        :param signature: Signature of the data with private-key that is paired with the parsed public-key.
        :type signature: str
        :param version: Version to check.
        :type version: str
        :param timestamp: Timestamp when the protocol will be migrating or migrated to this version.
        :type timestamp: str
        :param network: The network where the version migrates or already migrated ('mainnet' or 'testnet').
        :type network: str

        :return: Wether the signature is valid or not.
        :rtype: bool
        """

        if not cls.valid_signature(public_key, signature, (version + timestamp + network)):
            return False

        return True


    @staticmethod
    def get_public_key(private_key: str):
        """Returns the public-key of the parsed private-key.

        :param private_key: Private-key of the wallet.
        :type private_key: str (hex-digest)

        :return: Public-key or false whether the private-key is right or not.
        :rtype: str | bool
        """
        try:
            # Fetch private-key from hex-string and return public-key
            return SigningKey.from_string(bytes.fromhex(private_key), curve=SECP256k1, hashfunc=sha3_512).get_verifying_key().to_string().hex()

        # Occurres if private-key is false
        except:
            return False


    @classmethod
    def keypair_valid(cls, public_key: str, private_key: str) -> bool:
        """Tests whether the keys are matching or not.

        :param public_key: Public-key from key-pair.
        :type public_key: str
        :param private_key: Private-key from key-pair.
        :type: str

        :return: The result wether the keys are matching or not.
        :rtype: bool
        """

        # Fetch private-key from hex-string
        verifying_key = cls.get_public_key(private_key)

        # Check if public-key is valid
        if not verifying_key == public_key:
            return False

        return True


    @classmethod
    def coins(cls, public_key: str, blockchain) -> float:
        """Returns the amount of coins the wallet owns.

        :param public_key: Public-key of the wallet.
        :type public_key: str
        :param blockchain: The Blockchain to search.
        :type blockchain: :py:class:`blockchain.Blockchain`

        :return: Amount of coins in the wallet.
        :rtype: float
        """

        # Fetch the claimed coins
        claimed_coins = cls.claims(public_key, blockchain)

        # Fetch the coins that the account spend on staking
        stake_tx = blockchain.fetch_transactions(public_key, tx_type='stake', is_sender=True)
        spend_on_stake = 0

        if len(stake_tx) > 0:
            for transaction in stake_tx:
                spend_on_stake += transaction.amount + transaction.fee

        # Fetch the coins that the wallet received and send as a tx
        tx = blockchain.fetch_transactions(public_key, tx_type='tx')
        tx_coins = 0

        if len(tx) > 1:
            for transaction in tx:
                # Check if it is no real transaction
                if transaction.sender == public_key and transaction.recipient == public_key:
                    continue

                # Check if the transaction comes from this wallet
                if transaction.sender == public_key:
                    tx_coins -= transaction.amount + transaction.fee

                # Transaction goes to this wallet
                else:
                    tx_coins += transaction.amount

        elif len(tx) > 0:
            # Check if the only transaction comes from this wallet
            if tx[0].sender == public_key and not tx[0].recipient == public_key:
                tx_coins -= tx[0].amount + tx[0].fee

            # Transaction goes to this wallet
            elif tx[0].recipient == public_key and not tx[0].sender == public_key:
                tx_coins += tx[0].amount

        # Return total coins
        return claimed_coins + tx_coins - spend_on_stake


    @staticmethod
    def claims(public_key: str, blockchain) -> float:
        """Returns the amount of coins the wallet owns.

        :param public_key: Public-key of the wallet.
        :type public_key: str
        :param blockchain: The Blockchain to search.
        :type blockchain: :py:class:`blockchain.Blockchain`

        :return: Amount of coins in the wallet.
        :rtype: float
        """
        return 0


    @staticmethod
    def stake(public_key: str, blockchain) -> float:
        """Returns the coins that the wallet has staked.

        :param public_key: Public-key of the wallet.
        :type public_key: str
        :param blockchain: The Blockchain to search.
        :type blockchain: :py:class:`blockchain.Blockchain`

        :return: Amount of staked coins of the wallet.
        :rtype: float
        """
        pass


    @staticmethod
    def score(public_key: str, blockchain) -> float:
        """Returns the staking worth of the wallet.

        :param public_key: Public-key of the wallet.
        :type public_key: str
        :param blockchain: The Blockchain to search.
        :type blockchain: :py:class:`blockchain.Blockchain`

        :return: Staking score (the higher the score the higher is the probability of
                 getting chosen to verify a block).
        :rtype: float
        """
        pass
