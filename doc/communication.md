# Communication
Here you can find the documentation for the communication between the nodes via 0MQ
and the communication between the nodes and the clients.

### 0MQ
Used tcp ports:
- server: `57575`
- client: `67676`

### RPC Protocol
Used rpc server port: `87878`

### Data types

|      Type      |                         Description                         |
|:--------------:|:-----------------------------------------------------------:|
|  `temp_block`  |                      A temporary block                      |
| `winner_block` |           A block that won the validation process           |
|      `tx`      |                      A new transaction                      |
|   `version`    |               A new version of the blockchain               |
|     `burn`     | A transaction that burns tokens with a proof for the reason |
|  `advertise`   |          An advertisement of a node to other nodes          |

### Extra information

- `network`: The network the data is from
- `sender`: The public key of the sender
- `signature`: The signature of the sender
