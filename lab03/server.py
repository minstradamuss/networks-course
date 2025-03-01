import socket
import sys

def handle_request(client_socket):
    request = client_socket.recv(1024).decode()
    filename = request.split()[1][1:]
    
    try:
        with open(filename, 'rb') as file:
            content = file.read()
            response = b'HTTP/1.1 200 OK\n\n' + content
    except FileNotFoundError:
        response = b'HTTP/1.1 404 Not Found\n\nFile Not Found'

    client_socket.sendall(response)
    client_socket.close()

def run_server(server_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', server_port))
    server_socket.listen(1)

    print(f"Server listening on port {server_port}")

    while True:
        print('Waiting for connection...')
        client_socket, addr = server_socket.accept()
        print(f'Connection from {addr}')
        handle_request(client_socket)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Format: python server.py server_port")
        sys.exit(1)

    server_port = int(sys.argv[1])
    run_server(server_port)
