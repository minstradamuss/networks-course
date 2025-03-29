import socket
import datetime
import time

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_address = ('127.0.0.1', 12345)
client_socket.settimeout(1.0)

rtt_list = []
lost_packets = 0

for i in range(1, 11):
    send_time = datetime.datetime.now()
    message = f'Ping {i} {send_time.strftime("%H:%M:%S.%f")[:-3]}'
    client_socket.sendto(message.encode(), server_address)

    try:
        start_time = time.time()
        response, addr = client_socket.recvfrom(1024)
        end_time = time.time()
        rtt = end_time - start_time
        rtt_list.append(rtt)

        print(f'Response from server: {response.decode()}')
        print(f'RTT: {rtt:.6f} seconds')

        min_rtt = min(rtt_list)
        max_rtt = max(rtt_list)
        avg_rtt = sum(rtt_list) / len(rtt_list)

        print(f'rtt min/avg/max = {min_rtt:.6f}/{avg_rtt:.6f}/{max_rtt:.6f} seconds\n')

    except socket.timeout:
        lost_packets += 1
        print('Request timed out\n')

client_socket.close()

print(f'Packets: Sent = 10, Received = {10 - lost_packets}, Lost = {lost_packets} ({(lost_packets / 10) * 100:.0f}% loss)')
