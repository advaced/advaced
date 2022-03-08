import Wallet


class Account(Wallet):
    def __init__(name, password, public_key=None, private_key=None, save_manually=False):
        """Creates a wallet from the given values and if save-manually is off it puts the wallet to the database.

        :param name: Name of the account.
        :type name: str
        :param password: Password that unlocks the account
        :type password: str
        :param public_key: Public key of the wallet.
        :type public_key: str
        :param private_key: Private key of the wallet.
        :type private_key: str
        :param save_manually: Enable/disable writing the account to the database.
        :type save_manually: bool

        :returns: Initialize successful.
        :rtype: bool
        """
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
        pass


    def save(self):
        pass
