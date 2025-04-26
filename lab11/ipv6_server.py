import socket
import threading

def handle_client(client_socket, client_address):
    print(f'Connected by {client_address}')
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            response = data.decode('utf-8').upper()
            client_socket.send(response.encode('utf-8'))
    except Exception as e:
        print(f'Error with {client_address}: {e}')
    finally:
        client_socket.close()
        print(f'Connection closed: {client_address}')

def main():
    server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    server_socket.bind(('::1', 12345))
    server_socket.listen()

    print('Server is listening on [::1]:12345')

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            thread.start()
    except KeyboardInterrupt:
        print('Server shutting down.')
    finally:
        server_socket.close()

if __name__ == '__main__':
    main()
