# Block
- `index` (integer): The index of the block wich is created with `previous_block['index'] + 1`.

- `version` (string): The version of the code, that created the block, so the code is changable after the first release.

- `timestamp` (string): A Timestamp generated with `str(datetime.now())`, e.g. `2022-02-09 08:02:19.766484`.

- `base_fee` (int): To be included into the block, this minimum fee is required for a transaction.

- `transactions` (list): Contains all the transactions (with a maximum of 2048) that are included into the block.

- `previous_hash` (hex-digest): The hash of the previous block

- `hash` (hex-digest (SHA256)): The hash of the current block, that contains all the information from above

- `validator` (ECDSA public-key): The public-key of the validator

- `signature` (ECDSA key-signature): Signed hash with the private-key of the validator.


## Transaction
- `sender` (ECDSA public-key): The public-key of the sender.

- `recipient` (ECDSA public-key): The public-key of the recipient.

- `amount` (integer with 18 decimal places): The amount of coins that the sender transacts.

- `fee` (integer): The transaction-fee, that is added to the incentive for the validators. There is always a minimum fee that is required to get into a block. Everything above is a tip and your transaction might be picked earlier the higher your fee is.

- `type` (string): There are three types of transactions:
  - `tx`: A normal transaction (also normal transaction-fee).

  - `stake`: Stakes coins to the recipient account (The recipient can't use these coins for transactions and the transaction-fee is only as half as high as the normal).

  - `claim`: Claims the given value, but in this case the current stake-holding account is the sender and the recipient is the one, who staked these coins earlier to this account or claims the coins that the person earned with his/her validation. Also the signature are is in this case made with the recipient private-key (the transaction-fee is only as half as high as the normal).

  - `burn`: Removes the senders stake and adds it to the recipients value (the recipient is the validator of the current block and the validator can not be the sender)

- `timestamp` (string): A Timestamp generated with `str(datetime.now())`, e.g. `2022-02-09 08:02:19.766484`.

- `hash` (hex-digest (SHA256)): The hash of the information of the transaction.

- `signature` (ECDSA key-signature): Signed hash with the private-key of the sender (or in some cases with the private-key of the recipient).
