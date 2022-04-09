from hashlib import sha3_256

# Add path
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from util.database.accounts import fetch_account, push_account, delete_account
from accounts.wallet import Wallet

from util.crypto.password import encrypt_data, decrypt_data, hash_password, verify_password


class Account(Wallet):
    def __init__(self, name, password, public_key=None, private_key=None):
        """Creates a wallet from the given values and if save-manually is off it puts the wallet to the database.

        :param name: Name of the account.
        :type name: str
        :param password: Password that unlocks the account
        :type password: str
        :param public_key: Public key of the wallet.
        :type public_key: str
        :param private_key: Private key of the wallet.
        :type private_key: str

        :returns: Initialize successful.
        :rtype: bool
        """
        super().__init__(public_key, private_key)

        if name:
            self.name = name

        else:
            # Fetch existing account names from the database and set a valid not existing name
            pass

        self.password = password

        # Set the keys
        if public_key:
            self.public_key = public_key

        if private_key:
            self.private_key = private_key

    @property
    def password_hash(self):
        return hash_password(self.password)

    def save(self):
        # Check if private key is set
        if self.private_key is None:
            return False

        # Encrypt the private key with the password
        encrypted_private_key = encrypt_data(self.private_key, sha3_256(self.password.encode('utf-8')).hexdigest())

        # Hash the password
        password_hash = hash_password(self.password)

        # Save the account to the database
        push_account(self.name, password_hash, encrypted_private_key)

        return True

    def load(self, database=None):
        """Load account from database.

        :param database: Database to load the account from.
        :type database: :py:class:`util.database.database.Database`

        :returns: Load successful.
        :rtype: bool
        """
        account_dict = fetch_account(self.name, database)

        # Check if account exists
        if not account_dict:
            return False

        # Check if password is correct
        if not verify_password(self.password, account_dict['password_hash']):
            return False

        # Decrypt the private key with the password
        self.private_key = decrypt_data(account_dict['private_key_hash'], sha3_256(self.password.encode('utf-8'))
                                        .hexdigest())

        # Set the public key
        self.public_key = self.get_public_key(self.private_key)

        # Check if the private key is valid
        if not self.public_key:
            # Reset the keys
            self.public_key = None
            self.private_key = None

            return False

        return True

    def delete(self, database=None):
        """Delete account from database.

        :param database: Database to delete the account from.
        :type database: :py:class:`util.database.database.Database`

        :returns: Delete successful.
        :rtype: bool
        """
        return delete_account(self.name, database)

    def __str__(self):
        return self.name
