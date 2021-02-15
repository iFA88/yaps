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
- Clients can subscribe to different *topics*.
- When a new message is *published* to a specific *topic*, all subscribers of that topic is notified with the message.

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
- Is represented by unique **ID**, that is stored in disk at the client side.

Client connects to server and subscribes:
- Server decides if new client or previous known. This is done by checking *(potential)* **ID**.
- If **NOT** previous client:
  - The server creates a new configuration state for the client.
- The server adds the subscription to the client state.

## API

### Subscription
1. `Client` Connect
2. `Server` Connect OK
3. `Client` Subscribe *"topic"*
4. `Server` Subscribe OK/NOT OK
5. `Client` Starts listening
6. `Server` pings `Client` every *X* seconds.


### Publish
1. `Client` Connect
2. `Server` Connect OK
3. `Client` Publish *"message"* to *"topic"*
4. `Server` Publish OK/NOT OK
5. `Client` Disconnects
6. `Server` Sends the messages to the topics.