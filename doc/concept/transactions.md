# Transactions

To include the transactions as efficient as possible into the blocks this cryptocurrency makes use of a [merkle tree](https://en.wikipedia.org/wiki/Merkle_tree).


## Merkle tree
A merkle tree is especially good for most efficient and secure verification of the contents of big data structures.
It hashes all the transactions together to the merkle root. Only the merkle root is included into the block headers to save disk space. 
But to verify the transactions the whole tree or at least the transactions itself are required.

## Transaction values
The transactions itself contain 5 values:
- the public key of the sender
- the public key of the recipient
- the amount of coins that is transferred
- the signature of the sender, that contains all the other transaction information
- the transaction fee

The public key [2] of the sender and the recipient are like the addresses of them, but they don't use them to send mails, they use them to send coins. 
The signature [2] is important to proof that the sender is aware of the transaction and wants to make it.
The transaction fee is added to the incentive [3] to create and validate blocks. So this fee is deducted from the senders coin balance.

[2] [More about key pairs and signatures](./privacy.md)

[3] [More about the incentive to create and validate blocks](./proof-of-stake.md)
