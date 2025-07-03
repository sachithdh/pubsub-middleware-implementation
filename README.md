# pubsub-middleware-implementation

A progressive implementation of a publish-subscribe middleware system using Python sockets, demonstrating three different levels of client-server communication patterns, which I developed as part of a university Middleware Architecturecourse module assignment.

## Project Structure

- **task_01/**: Basic client-server communication
- **task_02/**: Publisher-subscriber pattern without topics
- **task_03/**: Full pub-sub system with topic-based messaging

## Task 01: Basic Client-Server Communication

Simple client-server setup where clients can send messages to the server.

### Running Task 01

**Start the server:**
```bash
python task_01/server_app.py <port>
```

**Start the client:**
```bash
python task_01/client_app.py <server_ip> <port>
```

**Example:**
```bash
# Terminal 1 (Server)
python task_01/server_app.py 8080

# Terminal 2 (Client)
python task_01/client_app.py 127.0.0.1 8080
```

## Task 02: Publisher-Subscriber Pattern

Implements a broadcast-based pub-sub system where publishers send messages to all subscribers.

### Running Task 02

**Start the server:**
```bash
python task_02/server_app.py <port>
```

**Start a publisher:**
```bash
python task_02/client_app.py <server_ip> <port> PUBLISHER
```

**Start a subscriber:**
```bash
python task_02/client_app.py <server_ip> <port> SUBSCRIBER
```

**Example:**
```bash
# Terminal 1 (Server)
python task_02/server_app.py 8080

# Terminal 2 (Publisher)
python task_02/client_app.py 127.0.0.1 8080 PUBLISHER

# Terminal 3 (Subscriber)
python task_02/client_app.py 127.0.0.1 8080 SUBSCRIBER
```

## Task 03: Topic-Based Publish-Subscribe

Complete pub-sub implementation with topic-based message routing.

### Running Task 03

**Start the server:**
```bash
python task_03/server_app.py <port>
```

**Start a publisher for a topic:**
```bash
python task_03/client_app.py <server_ip> <port> PUBLISHER <topic>
```

**Start a subscriber for a topic:**
```bash
python task_03/client_app.py <server_ip> <port> SUBSCRIBER <topic>
```

**Example:**
```bash
# Terminal 1 (Server)
python task_03/server_app.py 8080

# Terminal 2 (Publisher for "news" topic)
python task_03/client_app.py 127.0.0.1 8080 PUBLISHER news

# Terminal 3 (Subscriber for "news" topic)
python task_03/client_app.py 127.0.0.1 8080 SUBSCRIBER news

# Terminal 4 (Subscriber for "sports" topic)
python task_03/client_app.py 127.0.0.1 8080 SUBSCRIBER sports
```

## Usage Instructions

1. **Port Range**: Use ports between 1-65535
2. **Role**: Must be either "PUBLISHER" or "SUBSCRIBER" (case insensitive)
3. **Exit**: Type "terminate" to disconnect from the server
4. **Topics**: In Task 03, messages are only delivered to subscribers of the same topic

## Features

- **Multi-threaded server** handling multiple clients concurrently
- **Thread-safe operations** using locks for shared resources
- **Graceful shutdown** with proper resource cleanup
- **Error handling** for invalid inputs and network issues
- **Real-time messaging** between publishers and subscribers

## Requirements

- Python 3.x
- No external dependencies (uses only standard library)