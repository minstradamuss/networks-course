import socket
import pickle
import sys
import time

def calculate_checksum(data):
    return sum(data) & 0xFF

def run_client(server_address, server_port, input_filename, timeout_val):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout_val)
    packet_number = 0

    try:
        with open(input_filename, 'rb') as input_file:
            file_data = input_file.read()
            packet_size = 3
            packets = [file_data[i:i + packet_size] for i in range(0, len(file_data), packet_size)]

            for i, packet in enumerate(packets):
                pkt = {'packet_num': packet_number, 'data': packet, 'checksum': calculate_checksum(packet)}
                serialized_pkt = pickle.dumps(pkt)
                sock.sendto(serialized_pkt, (server_address, server_port))

                while True:
                    try:
                        ack_data, _ = sock.recvfrom(1024)
                        ack = pickle.loads(ack_data)
                        if ack['packet_num'] == packet_number:
                            print(f"Packet {i} ACK received")
                            packet_number = 1 - packet_number
                            break
                    except socket.timeout:
                        print(f"Timeout for packet {i}, resending...")
                        sock.sendto(serialized_pkt, (server_address, server_port))

        sock.sendto(b'EOF', (server_address, server_port))

    except Exception as e:
        print(f"Exception: {e}")
        sock.sendto(b'EXCEPTION', (server_address, server_port))

    sock.close()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(f"you provide {len(sys.argv) - 1} arguments, at least 2 expected (filename, timeout)")
        sys.exit(1)

    input_file = sys.argv[1]
    timeout = float(sys.argv[2])
    server_ip = '127.0.0.1'
    server_port = 12345

    run_client(server_ip, server_port, input_file, timeout)
