import socket
import threading
import sys

HOST = "192.168.84.98"
clients = []
lock = threading.Lock()

def broadcast(message, sender_ip):
    with lock:
        for client in clients:
            conn, ip, role = client
            if role == "SUBSCRIBER" and ip != sender_ip:
                try:
                    conn.sendall(message.encode())
                except:
                    conn.close()
                    if client in clients:
                        clients.remove(client)


def client_handler(client_socket, client_ip, role):
    print(f"{client_ip} CONNECTED as {role}")

    with lock:
        clients.append([client_socket, client_ip, role])

    try:
        while True:
            message = client_socket.recv(1024).decode()

            if not message:
                break


            if role == "PUBLISHER":
                broadcast(f"[PUBLISHER {client_ip}]: {message}", client_ip)

    except Exception as e:
        print(f"ERROR from {client_ip}: {e}")

    finally:
        print(f"{client_ip} DISCONNECTED")
        with lock:
            for client in clients:
                if client[1] == client_ip:
                    clients.remove(client)
                    break
        client_socket.close()

def start_server(PORT):

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Server is listening on {HOST}:{PORT}")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            role = client_socket.recv(1024).decode().strip().upper()

            if role not in ("PUBLISHER", "SUBSCRIBER"):
                print(f"Invalid role from {addr[0]}. Disconnecting.")
                client_socket.close()
                continue

            thread = threading.Thread(target=client_handler, args=(client_socket, addr, role), daemon=True)
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