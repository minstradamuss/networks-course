import socket
import pickle
import random
import sys

ADDRESS = '127.0.0.1'

def calculate_checksum(data):
    return sum(data) & 0xFF

def receive_file(server_socket, receive_filename):
    expected_packet = 0
    with open(receive_filename, "wb") as file:
        while True:
            try:
                data, addr = server_socket.recvfrom(1024)

                if data == b'EOF':
                    break
                if data == b'EXCEPTION':
                    print("Client reported an exception.")
                    break

                packet = pickle.loads(data)

                if random.random() < 0.3:
                    continue

                if packet['packet_num'] == expected_packet and packet['checksum'] == calculate_checksum(packet['data']):
                    ack = {'packet_num': packet['packet_num'], 'data': 'ACK'}
                    server_socket.sendto(pickle.dumps(ack), addr)
                    file.write(packet['data'])
                    expected_packet ^= 1
                else:
                    print("Incorrect packet number or checksum.")
            except Exception as e:
                print(f"Error receiving: {e}")
                break

    return addr

def send_file(server_socket, client_addr, filename, timeout):
    expected_packet = 0
    try:
        with open(filename, 'rb') as file:
            file_data = file.read()
            packets = [file_data[i:i+3] for i in range(0, len(file_data), 3)]

            for i, packet in enumerate(packets):
                data = {
                    'packet_num': expected_packet,
                    'data': packet,
                    'checksum': calculate_checksum(packet)
                }
                serialized_data = pickle.dumps(data)

                while True:
                    server_socket.sendto(serialized_data, client_addr)
                    try:
                        ack, _ = server_socket.recvfrom(1024)
                        ack_data = pickle.loads(ack)
                        if ack_data['packet_num'] == expected_packet:
                            print(f"ACK for packet {i} received.")
                            expected_packet ^= 1
                            break
                    except socket.timeout:
                        print(f"Timeout on packet {i}. Retrying...")

        server_socket.sendto(b'EOF', client_addr)

    except Exception as e:
        print(f"Error sending: {e}")
        server_socket.sendto(b'EXCEPTION', client_addr)

def run_server(port, filename, receive_filename, timeout):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((ADDRESS, port))
        print(f"Server listening on {ADDRESS}:{port}")
        server_socket.settimeout(timeout)

        client_addr = receive_file(server_socket, receive_filename)

        print("Receiving complete. Sending file back...")
        send_file(server_socket, client_addr, filename, timeout)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python server.py <filename_to_send> <filename_to_receive> [timeout]")
        sys.exit(1)

    send_filename = sys.argv[1]
    receive_filename = sys.argv[2]
    timeout = float(sys.argv[3]) if len(sys.argv) > 3 else 5.0

    run_server(port=12345, filename=send_filename, receive_filename=receive_filename, timeout=timeout)
