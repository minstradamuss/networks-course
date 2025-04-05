import socket
import pickle
import random
import sys

def calculate_checksum(data):
    return sum(data) & 0xFF

def send_file(client_socket, server_address, server_port, filename, timeout):
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
                    client_socket.sendto(serialized_data, (server_address, server_port))
                    try:
                        ack, _ = client_socket.recvfrom(1024)
                        ack_data = pickle.loads(ack)
                        if ack_data['packet_num'] == expected_packet:
                            print(f"ACK for packet {i} received.")
                            expected_packet ^= 1
                            break
                    except socket.timeout:
                        print(f"Timeout on packet {i}. Retrying...")

        client_socket.sendto(b'EOF', (server_address, server_port))

    except Exception as e:
        print(f"Error sending: {e}")
        client_socket.sendto(b'EXCEPTION', (server_address, server_port))

def receive_file(client_socket, receive_filename):
    expected_packet = 0
    with open(receive_filename, "wb") as file:
        while True:
            try:
                data, addr = client_socket.recvfrom(1024)

                if data == b'EOF':
                    break
                if data == b'EXCEPTION':
                    print("Server reported an exception.")
                    break

                packet = pickle.loads(data)

                if random.random() < 0.3:
                    continue

                if packet['packet_num'] == expected_packet and packet['checksum'] == calculate_checksum(packet['data']):
                    ack = {'packet_num': packet['packet_num'], 'data': 'ACK'}
                    client_socket.sendto(pickle.dumps(ack), addr)
                    file.write(packet['data'])
                    expected_packet ^= 1
                else:
                    print("Incorrect packet number or checksum.")
            except Exception as e:
                print(f"Error receiving: {e}")
                break

def run_client(server_address, server_port, filename, receive_filename, timeout):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.settimeout(timeout)
        send_file(client_socket, server_address, server_port, filename, timeout)
        client_socket.settimeout(None)
        print("File sent. Waiting to receive file back...")
        receive_file(client_socket, receive_filename)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python client.py <filename_to_send> <filename_to_receive> [timeout]")
        sys.exit(1)

    send_filename = sys.argv[1]
    receive_filename = sys.argv[2]
    timeout = float(sys.argv[3]) if len(sys.argv) > 3 else 5.0

    run_client(server_address='127.0.0.1', server_port=12345, filename=send_filename, receive_filename=receive_filename, timeout=timeout)
