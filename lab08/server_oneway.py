import socket
import pickle
import sys
import random

def calculate_checksum(data):
    return sum(data) & 0xFF

def run_server(port, output_filename):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', port))
    expected_packet_num = 0

    with open(output_filename, "wb") as output_file:
        while True:
            try:
                data, addr = sock.recvfrom(1024)
                if data == b'EOF':
                    break
                if data == b'EXCEPTION':
                    print("some exception in client")
                    break

                packet = pickle.loads(data)

                if random.random() < 0.3:
                    continue

                if packet['packet_num'] == expected_packet_num and packet['checksum'] == calculate_checksum(packet['data']):
                    output_file.write(packet['data'])
                    ack = {'packet_num': packet['packet_num'], 'data': 'ACK'}
                    sock.sendto(pickle.dumps(ack), addr)
                    expected_packet_num = 1 - expected_packet_num
                else:
                    print("wrong packet_num or checksum")
            except Exception as e:
                print(f"Exception: {e}")
                break

    sock.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"you provide {len(sys.argv) - 1} arguments, at least 1 expected (receive_filename)")
        sys.exit(1)

    output_file = sys.argv[1]
    server_port = 12345
    run_server(server_port, output_file)
