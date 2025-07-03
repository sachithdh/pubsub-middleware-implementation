import socket
import threading
import sys

HOST = "0.0.0.0"


lock = threading.Lock()
topics = {}


def client_handler(client_socket, client_ip, role, topic):

    print(f"{client_ip} CONNECTED as {role} on topic {topic}")

    try:
        if role == "SUBSCRIBER":
            with lock:
                if topic not in topics:
                    topics[topic] = set()
                topics[topic].add(client_socket)
            client_socket.sendall(f"Subscribed to {topic}\n".encode())

            while True:
                try:
                    message = client_socket.recv(1024).decode().strip().lower()
                    if message == "terminate":
                        break
                except:
                    break
            
        elif role == "PUBLISHER":
            while True:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                
                with lock:
                    if topic in topics:
                        for subscribe_socket in topics[topic]:
                            try:
                                subscribe_socket.sendall(f"{topic}: {message}\n".encode())
                            except:
                                pass
                    else:
                        client_socket.sendall(f"No subscriber for the topic {topic}\n".encode())
    
    except Exception as e:
        print(f"Error from {client_ip}: {e}")
    
    finally:
        print(f"{client_ip} DISCONNECTED")
        with lock:
            for subscribers in topics.values():
                subscribers.discard(client_socket)
        client_socket.close()


def start_server(PORT):

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Server is listening on {HOST}:{PORT}")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            role, topic = client_socket.recv(1024).decode().split(",")
            role = role.strip()
            topic = topic.strip()

            if role not in ("PUBLISHER", "SUBSCRIBER"):
                print(f"Invalid role from {addr}. Disconnecting.")
                client_socket.close()
                continue

            thread = threading.Thread(target=client_handler, args=(client_socket, addr, role, topic), daemon=True)
            thread.start()

    except KeyboardInterrupt:
        print("\nServer is shutting down!")

    finally:
        server_socket.close()

if __name__ == "__main__":
    if len(sys.argv) < 2 :
        print(f"Invalid command")
        print("Usage: python file_name.py <port>")
        sys.exit(1)

    else:
        PORT = int(sys.argv[1])
        if not (1 <= PORT <= 65535):
            print("ERROR: Port must be between 1 and 65535")
            sys.exit(1)
        
        start_server(PORT)