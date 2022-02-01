# Transactions

To include the transactions as efficient as possible into the blocks this cryptocurrency makes use of a [merkle tree](https://en.wikipedia.org/wiki/Merkle_tree).

A merkle tree is especially good for most efficient and secure verification of the contents of big data structures.
It hashes all the transactions together to the merkle root. Only the merkle root is included into the block headers to save some disk space. 
But to verify the transactions the whole tree or at least the transactions are needed.

The transactions itself contain 4 values:
- the public-key of the sender
- the public-key of the recipient
- the amount of coins that is transferred
- the signature of the sender, that contains all the other transaction information
