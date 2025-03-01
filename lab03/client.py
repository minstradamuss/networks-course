import socket
import sys

def send_request(server_host, server_port, filename):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))

    request = f"GET /{filename} HTTP/1.1\r\nHost: {server_host}:{server_port}\r\n\r\n"
    client_socket.sendall(request.encode())

    response = client_socket.recv(1024)
    print(response)

    client_socket.close()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Format: python client.py server_host server_port filename")
        sys.exit(1)

    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    filename = sys.argv[3]

    send_request(server_host, server_port, filename)