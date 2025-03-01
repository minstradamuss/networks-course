import socket
import sys
import threading
from queue import Queue

def handle_request(client_socket):
    request = client_socket.recv(1024)
    filename = request.split()[1][1:]

    try:
        with open(filename, 'rb') as file:
            content = file.read()
            response = b'HTTP/1.1 200 OK\n\n' + content
    except FileNotFoundError:
        response = b'HTTP/1.1 404 Not Found\n\nFile Not Found'

    client_socket.sendall(response)
    client_socket.close()

def handle_connection(client_socket, semaphore):
    with semaphore:
        handle_request(client_socket)

def run_server(server_port, concurrency_level):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', server_port))
    server_socket.listen(5)

    print(f"Server listening on port {server_port} with concurrency level {concurrency_level}")

    semaphore = threading.Semaphore(concurrency_level)

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        client_thread = threading.Thread(target=handle_connection, args=(client_socket, semaphore))
        client_thread.start()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Format: python server.py server_port concurrency_level")
        sys.exit(1)

    server_port = int(sys.argv[1])
    concurrency_level = int(sys.argv[2])

    run_server(server_port, concurrency_level)
