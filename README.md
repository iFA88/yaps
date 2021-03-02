# YAPS - Yet Another Publish Subscribe protocol
- *YAPS* is a publish-subscribe protocol running over TCP/IP.
- Inspired by MQTT

## User guide

---

## Setup
`pip install yaps`

## CLI tools
To use the executables, ensure that yaps is installed which should put *yaps-publish*, *yaps-subscribe* and *yaps-server* available your path.

### Publish
`yaps-publish --topic weather --message "Very cold today!"`

### Subscribe
`yaps-publish --topic weather`


## Python API
The client can be used either asynchronous or synchronous.

### Publish Synchronous
```
from yaps.client import Client

client = Client('127.0.0.1', 8999)
client.publish(topic='weather', message='Very cold today!')
```
### Subscribe Synchronous
```
from yaps.client import Client

client = Client('127.0.0.1', 8999)
client.subscribe(topic='weather',
                 data_received=lambda msg: print(f'New data: {msg}'))
```

### Publish Asynchronous
```
import asyncio
from yaps.client import AsyncClient

client = AsyncClient('127.0.0.1', 8999)
asyncio.run(client.publish(topic='weather', message='Very cold today!'))
```

### Subscribe Asynchronous
```
import asyncio
from yaps.client import AsyncClient

client = AsyncClient('127.0.0.1', 8999)
callback = lambda msg: print(f'New data: {msg}')
asyncio.run(client.subscribe(topic='test',
                             data_received=callback))
```

### Server (Asynchronous only)
```
import asyncio
from yaps.server import Server

server = Server('127.0.0.1', 8999)
asyncio.run(server.start())
```

## Logging
Logging is enabled by default and can be disabled by calling `disable()` on either a client or server.
You can set the logging level by calling `set_loglevel(string)` with either a string, or an int directly from the `logging` module.
Logging output is by default directed to both stdin and a log file, located at `~/.yaps` on Unix systems (not 100% sure where this is located in Windows).

---

## Objectives
- Create a functional publish-subscribe protocol that is easy to use.
- It should have a simple cli interface.
- Practise coding a bigger project and keeping it structured.
- Practise documenting a bigger project.
- (*Bonus*) Web interface, something like Node-red.

## Todos:
- [X] Client state
- [X] Subscription object
- [X] Turn off logging during tests
- [X] Enable wildcard subscribe
- [X] Configuration file location
- [X] Create pip package
- [X] Fix import & paths with pip-package
- [X] Put publications in its own queue.
- [X] Build a *synchronous* client
- [X] Write *User Guides*
- [ ] Write more synchronous tests
- [ ] Write more comprehensive tests, if possible
- [ ] Do performance tests
- [ ] Find use cases
- [ ] *Create stress tests*
- [ ] *Build a Server UI*

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

If the command is publish, `Data` consists of `topic` | `message`, where a
pipe ` | `, seperated the topic from the message.
**Note:** The pipe must be followed by a white-space and have a whitespace
before it.

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

