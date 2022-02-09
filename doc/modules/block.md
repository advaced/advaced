# Block
- `index` (integer): The Index of the block wich is created with `previous_block['index'] + 1`.

- `timestamp` (string): A Timestamp generated with `str(datetime.now())`, e.g. `2022-02-09 08:02:19.766484`.

- `merkle_root` (hex-digest): The root of the [merkle tree](./merkle-tree.md), that contains the hashed hex-digest of all the transactions that are contained in the block.

- `previous_hash` (hex-digest): 
