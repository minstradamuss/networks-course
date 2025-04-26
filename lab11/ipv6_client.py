import socket

def main():
    client_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    server_address = ('::1', 12345)

    try:
        client_socket.connect(server_address)
        print('Connected to the server.')

        while True:
            message = input('Enter message (or "exit" to quit): ')
            if message.lower() == 'exit':
                break

            client_socket.send(message.encode('utf-8'))
            data = client_socket.recv(1024)
            print(f'Server response: {data.decode("utf-8")}')

    except Exception as e:
        print(f'Error: {e}')
    finally:
        client_socket.close()
        print('Disconnected from the server.')

if __name__ == '__main__':
    main()
