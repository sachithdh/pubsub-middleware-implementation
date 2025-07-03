import socket
import threading
import sys

def receive_messages(sock):
    try:
        while True:
            message = sock.recv(1024).decode()

            if not message:
                break
            print(f"\n{message}\n> ", end="")

    except:
        pass
    finally:
        sock.close()

def client_program(SERVER, PORT, ROLE, TOPIC):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER, PORT))

    client_socket.sendall(f"{ROLE},{TOPIC}".encode())

    print(f"\nConnected to server {SERVER}:{PORT} as {ROLE} on topic {TOPIC}")

    print("type 'terminate' to exit\n")

    if ROLE == "SUBSCRIBER":
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()
        try:
            while True:
                command = input("> ")
                if command.lower() == "terminate":
                    break

        except KeyboardInterrupt:
            print("\nInterrupted by user.")
            sys.exit(1)

        finally:
            client_socket.close()
            print("Disconnected from Server.")

        
    elif ROLE == "PUBLISHER":
        try:
            while True:
                command = input("> ")
                if command.lower() == "terminate":
                    break
                client_socket.sendall(command.encode())
        except KeyboardInterrupt:
            print("\nInterrupted by user.")

        finally:
            client_socket.close()
            print("Disconnected from Server.")


if __name__ == "__main__":
    if len(sys.argv) != 5 :
        print(f"Invalid command")
        print("Usage: python file_name.py <server_ip> <port> <PUBLISHER|SUBSCRIBER>")
        sys.exit(1)

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ROLE = sys.argv[3].strip().upper()
    TOPIC = sys.argv[4].strip()

    if not (1 <= PORT <= 65535):
        print("ERROR: Port must be between 1 and 65535")
        sys.exit(1)
    if ROLE not in ("PUBLISHER", "SUBSCRIBER"):
        print("ERROR: Role must be PUBLISHER or SUBSCRIBER")
        sys.exit(1)

    
    client_program(HOST, PORT, ROLE, TOPIC)