#!/usr/bin/python

import socket
import threading
import sys

HOST = "192.168.84.98"

lock = threading.Lock()


def client_handler(client_socket, addr):
    print(f"{addr} CONNECTED.")

    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            if message.lower() == "terminate":
                print(f"{addr} DISCONNECTED.")
                break

            print(f"[CLIENT]: {message}")


    except Exception as e:
        print(f"ERROR: Exception from {addr}: {e}")

    
    finally:
        
        client_socket.close()


def start_server(PORT):

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Server is listening on {HOST}:{PORT}")

    try:
        while True:
            client_socket, addr = server_socket.accept()

            thread = threading.Thread(target=client_handler, args=(client_socket, addr), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        print("\nServer is shutting down!")

    finally:
        server_socket.close()


if __name__ == "__main__":
    if len(sys.argv) < 2 :
        print(f"Invalid command")
        print("Usage: python file_name.py <port>")
        exit

    else:
        PORT = int(sys.argv[1])
        if not (1 <= PORT <= 65535):
            print("ERROR: Port must be between 1 and 65535")
            exit()
        
        start_server(int(PORT))

