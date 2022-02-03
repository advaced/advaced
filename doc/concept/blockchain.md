# Blockchain

Advaced is an electronic cash system as a decentralized chain of blocks.
Each block contains an index, so that it is not possible to generate blocks twice.
Every block also includes all the transactions [1] that were emitted to the network since the last block was made. 
To prove that the data must have existed at this time, the block gets a timestamp, when the block is validated. 

The block is validated by a (pseudo) random validator within the network wich makes the blockchain decentralized.
The address of the validator is included in the block too, so everyone knows who made this block.
All the data is hashed with the SHA256 hashing function and this hash is also mentioned in the block (in hex format).

To make it a chain the hash of the previous block is also contained in the current block and hash
The version is included too, so that the chain is upgradable.

[1] [More about transactions](./transactions.md)
