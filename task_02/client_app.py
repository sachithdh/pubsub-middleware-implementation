#!/usr/bin/python

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


def client_program(SERVER, PORT, ROLE):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER, PORT))

    client_socket.sendall(ROLE.encode())

    print(f"\nConnected to server {SERVER}:{PORT} as {ROLE}")

    print("type 'terminate' to exit\n")

    if ROLE.lower() == "subscriber":
        threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    
    try:
        while True:
            command = input("> ")
            if command.lower() == "terminate":
                break

            if ROLE.lower() == "publisher":
                client_socket.sendall(command.encode())

    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        sys.exit(1)
        
    finally:
        client_socket.close()
        print("Disconnected from Server.")


if __name__ == "__main__":
    if len(sys.argv) != 4 :
        print(f"Invalid command")
        print("Usage: python file_name.py <server_ip> <port> <PUBLISHER|SUBSCRIBER>")
        sys.exit(1)

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ROLE = sys.argv[3].strip().upper()

    if not (1 <= PORT <= 65535):
        print("ERROR: Port must be between 1 and 65535")
        sys.exit(1)
    if ROLE.lower() not in ("publisher", "subscriber"):
        print("ERROR: Role must be PUBLISHER or SUBSCRIBER")
        sys.exit(1)

    
    client_program(HOST, PORT, ROLE)