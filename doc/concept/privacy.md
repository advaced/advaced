# Privacy
To prevent coin-robbery a secure password system must be added to the wallets.

## Cryptographic key pairs
A cryptographic key pair is created with the ECDSA hash function. 
With the private key transactions can be signed. 
The signature can be verified with the public key of the sender, but the private key can not be restored from the signature.

## Privacy of identities
Even if the public key is available for everyone in the network [4], the identities stay private until the individual reveals wich public key belongs to him.
The private key stays like a password private and this key should be never ever shared with someone else.

[4] [More about the network](./network.md)