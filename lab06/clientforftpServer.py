import socket
import os
import sys

HOST = '127.1.1.1'
PORT = 2121
USERNAME = 'userTEST'
PASSWORD = '12345'

def receive_data(sock):
    data = b""
    sock.settimeout(5)
    try:
        while True:
            part = sock.recv(1024)
            if not part:
                break
            data += part
            if len(part) < 1024:
                break
    except socket.timeout:
        pass
    return data

def setup_data_connection(sock):
    data_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_listener.bind((HOST, 0))
    data_listener.listen(1)
    ip_parts = HOST.split('.')
    port = data_listener.getsockname()[1]
    p1 = port // 256
    p2 = port % 256
    port_command = f"PORT {','.join(ip_parts)},{p1},{p2}\r\n"
    sock.sendall(port_command.encode())
    print("[>] PORT sent:", port_command.strip())
    print(receive_data(sock).decode(errors='ignore'), flush=True)
    return data_listener

def list_files(sock):
    print(">>> NLST COMMAND", flush=True)
    data_listener = setup_data_connection(sock)
    sock.sendall(b"NLST\r\n")
    data_sock, _ = data_listener.accept()
    data = receive_data(data_sock)
    print("[DATA CONNECTION OUTPUT]:", flush=True)
    print(data.decode(errors='ignore'), flush=True)
    data_sock.close()
    data_listener.close()
    print(receive_data(sock).decode(errors='ignore'), flush=True)
    print(">>> NLST END\n", flush=True)

def change_directory(sock, path):
    command = f"CWD {path}\r\n"
    sock.sendall(command.encode())
    print(f">>> {command.strip()}")
    print(receive_data(sock).decode(errors='ignore'), flush=True)

def print_working_directory(sock):
    sock.sendall(b"PWD\r\n")
    print(">>> PWD")
    print(receive_data(sock).decode(errors='ignore'), flush=True)

def upload_file(sock, filename):
    basename = os.path.basename(filename)
    command = f"STOR {basename}\r\n"
    data_listener = setup_data_connection(sock)
    sock.sendall(command.encode())
    data_sock, _ = data_listener.accept()
    with open(filename, 'rb') as f:
        data_sock.sendall(f.read())
    data_sock.close()
    data_listener.close()
    print(receive_data(sock).decode(errors='ignore'), flush=True)
    print(">>> STOR END\n", flush=True)

def download_file(sock, filename, save_as):
    command = f"RETR {filename}\r\n"
    data_listener = setup_data_connection(sock)
    sock.sendall(command.encode())
    data_sock, _ = data_listener.accept()
    file_data = receive_data(data_sock)
    with open(save_as, 'wb') as f:
        f.write(file_data)
    data_sock.close()
    data_listener.close()
    print(f"[+] File saved as {save_as}")
    print(receive_data(sock).decode(errors='ignore'), flush=True)
    print(">>> RETR END\n", flush=True)

def quit(sock):
    sock.sendall(b"QUIT\r\n")
    print(receive_data(sock).decode(errors='ignore'), flush=True)
    sock.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        print(receive_data(sock).decode(errors='ignore'), flush=True)

        sock.sendall(f"USER {USERNAME}\r\n".encode())
        print(receive_data(sock).decode(errors='ignore'), flush=True)

        sock.sendall(f"PASS {PASSWORD}\r\n".encode())
        print(receive_data(sock).decode(errors='ignore'), flush=True)

        print_working_directory(sock)
        change_directory(sock, "..")
        print_working_directory(sock)

        list_files(sock)

        upload_file(sock, "C:/Users/User/Source/Repos/networks-course/lab06/mytestfile.txt")

        download_file(sock, "C:/Users/User/Source/Repos/networks-course/lab06/mytestfile.txt", "downloaded_copy.txt")

        quit(sock)

if __name__ == "__main__":
    main()
