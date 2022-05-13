from ecdsa import SigningKey, VerifyingKey, SECP256k1
from hashlib import sha3_512

from datetime import datetime, timezone


class Wallet:
    def __init__(self, public_key: str = None, private_key: str = None):
        """Create a new wallet.

        :param public_key: Public key of the wallet.
        :type public_key: str (hex digest)
        :param private_key: Private key of the wallet.
        :type private_key: str (hex digest)
        """

        # Create wallet keypair (with ecdsa, the SECP256k1 curve and sha3-512 as hash-algorithm)
        verifying_key = SigningKey.generate(curve=SECP256k1, hashfunc=sha3_512)

        self.public_key = public_key if public_key else verifying_key.get_verifying_key().to_string().hex()
        self.private_key = private_key if private_key else verifying_key.to_string().hex()

    @staticmethod
    def sign_data(private_key: str, data: str):
        """Sign data with string of private-key

        :param private_key: Private-key of the wallet.
        :type private_key: str (hex-digest)
        :param data: Data to sign.
        :type data: str (json)

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
        :type data: str (json)

        :return: Whether the signature is valid or not or the key for it is valid.
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
    def valid_version_stamp(cls, public_key: str, signature: str, version: str, timestamp: str, network: str) -> bool:
        """Verify a version stamp from a developer-key signature (Warning: This function does not check the validity of
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

        :return: Whether the signature is valid or not.
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
            return SigningKey.from_string(bytes.fromhex(private_key), curve=SECP256k1,
                                          hashfunc=sha3_512).get_verifying_key().to_string().hex()

        # Occurred if private-key is false
        except:
            return False

    @classmethod
    def keypair_valid(cls, public_key: str, private_key: str) -> bool:
        """Tests whether the keys are matching or not.

        :param public_key: Public-key from key-pair.
        :type public_key: str
        :param private_key: Private-key from key-pair.
        :type: str

        :return: The result whether the keys are matching or not.
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
        coins = cls.claims(public_key, blockchain)

        # Fetch the coins that the account spend on staking
        stake_tx = blockchain.fetch_transactions(public_key, tx_type='stake', is_sender=True)

        if len(stake_tx) > 0:
            coins -= sum([transaction.amount + transaction.fee for transaction in stake_tx])

        # Fetch the coins that the account spend on unstaking fees
        unstake_tx = blockchain.fetch_transactions(public_key, tx_type='unstake', is_sender=False)

        if len(unstake_tx) > 0:
            coins += sum([transaction.amount - transaction.fee for transaction in unstake_tx])

        # Fetch the coins that the wallet sent and received as a tx
        tx = blockchain.fetch_transactions(public_key, tx_type='tx')

        if len(tx) > 1:
            for transaction in tx:
                # Check if the transaction comes from this wallet
                if transaction.sender == public_key and not transaction.recipient == public_key:
                    coins -= (transaction.amount + transaction.fee)

                # Transaction goes to this wallet
                elif transaction.recipient == public_key and not transaction.sender == public_key:
                    coins += transaction.amount

        elif len(tx) > 0:
            # Check if the only transaction comes from this wallet
            if tx[0].sender == public_key and not tx[0].recipient == public_key:
                coins -= tx[0].amount + tx[0].fee

            # Transaction goes to this wallet
            elif tx[0].recipient == public_key and not tx[0].sender == public_key:
                coins += tx[0].amount

        return coins

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
        # Fetch the coins that the account claimed
        claims_tx = blockchain.fetch_transactions(public_key, tx_type='claim', is_sender=False)

        if not len(claims_tx) > 0:
            return 0

        return sum([transaction.amount - transaction.fee for transaction in claims_tx])

    @staticmethod
    def stake(public_key: str, blockchain, index: int = None) -> float:
        """Returns the coins that the wallet has staked.

        :param public_key: Public-key of the wallet.
        :type public_key: str
        :param blockchain: The Blockchain to search.
        :type blockchain: :py:class:`blockchain.Blockchain`
        :param index: Index of the block to use as last block.
        :type index: int | NoneType

        :return: Amount of staked coins of the wallet.
        :rtype: float
        """
        # Fetch the staked and unstaked coins of this wallet

        stake = 0

        stake_tx = blockchain.fetch_transactions(public_key, tx_type='stake', is_sender=False,
                                                 index=index if index else None)
        unstake_tx = blockchain.fetch_transactions(public_key, tx_type='unstake', is_sender=True,
                                                   index=index if index else None)

        if len(stake_tx) > 0:
            # Go through the stake transactions
            stake -= sum([transaction.amount - transaction.fee for transaction in stake_tx])

        if len(unstake_tx) > 0:
            # Go through the unstake transactions
            stake += sum([transaction.amount - transaction.fee for transaction in unstake_tx])

        return stake

    @classmethod
    def score(cls, public_key: str, blockchain) -> float:
        """Returns the staking worth of the wallet.

        :param public_key: Public-key of the wallet.
        :type public_key: str
        :param blockchain: The Blockchain to search.
        :type blockchain: :py:class:`blockchain.Blockchain`

        :return: Staking score (the higher the score the higher is the probability of
                 getting chosen to verify a block).
        :rtype: float
        """

        # Fetch the staked, unstaked and the burned coins of this wallet
        stake_tx = blockchain.fetch_transactions(public_key, tx_type='stake', is_sender=False)

        # Check if the account has any stake
        if len(stake_tx) < 0:
            return 0

        # Bring the transactions into a better format
        stakes = [(tx.amount, tx.timestamp.timestamp()) for tx in stake_tx]

        stakes.sort(key=lambda x: x[1])

        # Remove unstaked stake
        unstake_tx = blockchain.fetch_transactions(public_key, tx_type='unstake', is_sender=True)

        if len(unstake_tx) > 1:
            for tx in unstake_tx:
                amount_left = tx.amount

                while amount_left > 0:
                    # Check if something really went wrong (if this occurred the stake of the account is negative and
                    # not allowed)
                    if len(stakes) == 0:
                        return 0

                    # Check if unstaking amount is bigger than the last staked amount
                    if amount_left > stakes[-1][0]:
                        amount_left -= stakes[-1][0]
                        stakes.pop(-1)

                    else:
                        stakes[-1][0] -= amount_left
                        break

        # Check if any stake is left
        if len(stakes) == 0:
            return 0

        # Calculate the coin age
        coin_age = sum([stake[0] * 1.000_000_104_051 ** datetime.now(timezone.utc).timestamp() - stake[1]
                        if datetime.now(timezone.utc).timestamp() - stake[1] <= 2_764_800 else 2_764_800  # 32d in sec
                        for stake in stakes])

        # Check if the coin age is above the maximum
        if coin_age > 65_536:
            #     2 ** 16
            return 65_536

        return coin_age
