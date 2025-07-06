#!/usr/bin/python

import socket
import threading
import sys



def client_program(SERVER, PORT):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(10)
    client_socket.connect((SERVER, PORT))

    print(f"\nConnected to server {SERVER}:{PORT}")

    print("Enter message (type 'terminate' to exit):")

    try:
        while True:
            
            command = input("> ")

            client_socket.sendall(command.encode())

            if command.lower() == "terminate":
                break

    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        client_socket.sendall("terminate".encode())
        sys.exit(1)
        
    finally:
        client_socket.close()
        print("Disconnected from Server.")

if __name__ == "__main__":
    if len(sys.argv) < 3 :
        print(f"Invalid command")
        print("Usage: python file_name.py <server_ip> <port>")
        sys.exit(1)

    else:
        HOST = sys.argv[1]
        PORT = int(sys.argv[2])

        if not (1 <= PORT <= 65535):
            print("ERROR: Port must be between 1 and 65535")
            sys.exit(1)

        
        client_program(HOST, PORT)