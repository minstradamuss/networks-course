import socket
import datetime
import time

server_address = ('127.0.0.1', 12345)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.settimeout(1.0)

seq_number = 0
received = 0
lost = 0
total = 0

try:
    while True:
        seq_number += 1
        total += 1
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        message = f'{seq_number} {timestamp}'
        client_socket.sendto(message.encode(), server_address)
        print(f'Heartbeat sent: seq={seq_number} time={timestamp}')

        try:
            response, addr = client_socket.recvfrom(1024)
            received += 1
            print(f'Heartbeat ACK from server: {response.decode()}')

        except socket.timeout:
            lost += 1
            print('Heartbeat lost (timeout)')

        loss_percentage = (lost / total) * 100
        print(f'Current loss: {loss_percentage:.0f}%\n')

        time.sleep(1)

except KeyboardInterrupt:
    print('Client stopped.')

    loss_percentage = (lost / total) * 100 if total > 0 else 0
    print(f'\nFinal Statistics:')
    print(f'Total sent: {total}, Received: {received}, Lost: {lost}, Loss: {loss_percentage:.0f}%')

finally:
    client_socket.close()
