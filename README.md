# VQTT - A MQTT-like protocol
- *VQTT* will be a publish-subscribe protocol running over TCP/IP.
- Very much inspired by MQTT

### Objectives
- Create a functional publish-subscribe protocol that is easy to use.
- It should have a simple cli interface.
- Practise coding a bigger project and keeping it structured.
- Practise documenting a bigger project.
- (*Bonus*) Web interface, something like Node-red.

## Server
- Always on, listening for new TCP connections.
- Using *asyncio* instead of threading.
- Stores state on disk (file or database).
- Clients can subscribe to different `topics`.
- When a new `message` is published to a specific `topic`, all subscribers of that topic is notified with the message.
- *Pings* subscribers every *X* seconds.
  - If a subscriber doesn't respond with *pong*, the server repeats the process *Y* times and then closes the connection.

## Topics
Topics must follow:
- Different topics are separated by `/`.
- Topics should not start or end with a `/`.
  - `/weather` -> `weather`.
  - `weather/` -> `weather`.
  - `/weather/` -> `weather`.
- Subscribing to `/` is equivalent to subscribing to all topics.
- Publishing to `/` is **not** permitted.

## Security


## Client
- Publish/Subscribe to different topics.
- See what topics you're subscribed to

### Subscriber
- Subscribe to a `topic`.
- Identified by **ID** from TCP connection.
- A subscriber waits for `messages` to be published.
- The subscriber must respond to server *pings* if it wants to keep connected.

### Publisher
- Publishes a `message` on a given `topic`.
- Can provide several flags:
  - TODO

Client connects to server and subscribes:
- Server decides if new client or previous known. This is done by checking *(potential)* **ID**.
- If **NOT** previous client:
  - The server creates a new configuration state for the client.
- The server adds the subscription to the client state.

## API

### Subscription
1. `Client` Connect
2. `Server` Connect ACK
3. `Client` Subscribe *"topic"*
4. `Server` Subscribe OK/NOT OK
5. `Client` Starts listening
6. `Server` *pings* `Client` every *X* seconds.


### Publish
1. `Client` Publish
2. `Server` Publish ACK
3. `Client` Publish *"message"* to *"topic"*
4. `Server` Publish OK/NOT OK
5. `Client` Disconnects
6. `Server` Sends the messages to the topics.


### Packet format
| Byte | Data |
| ---- | --- |
| 0 | Command |
| 1 | Flags |
| 2-5 | Length of packet |
| 6-* | Data |

#### Commands:
| Command | Value |
| ---- | --- |
| `publish` | |
| `publish_ack` | |
| `subscribe` | |
| `subscribe_ack` | |
| `new_data` | |
| `new_data_ack` | |
| `ping` | |
| `pong` | |
| `incorrect_format` | |

