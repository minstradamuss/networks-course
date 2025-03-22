import socket
import sys
import os

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
        print("[!] Socket receive timeout", flush=True)
    return data

def list_files(sock, data_sock):
    print(">>> LIST COMMAND", flush=True)
    sock.sendall(b"LIST\r\n")

    data = receive_data(data_sock)
    print("[DATA CONNECTION OUTPUT]:", flush=True)
    print(data.decode(errors='ignore'), flush=True)
    print("-" * 40, flush=True)

    response = receive_data(sock)
    print("[CONTROL CONNECTION RESPONSE]:", flush=True)
    print(response.decode(errors='ignore'), flush=True)
    print(">>> LIST END\n", flush=True)

def upload_file(sock, data_sock, filename):
    print(f">>> STOR COMMAND: Uploading {filename}", flush=True)

    try:
        with open(filename, "rb") as file:
            command = b"STOR " + bytes(os.path.basename(filename), "utf-8") + b"\r\n"
            sock.sendall(command)
            file_data = file.read()
            data_sock.sendall(file_data)
            print("[+] File data sent", flush=True)
    except FileNotFoundError:
        print(f"[!] File '{filename}' not found!", flush=True)
        return

    response = receive_data(sock)
    print(response.decode(errors='ignore'), flush=True)
    print(">>> STOR END\n", flush=True)

def download_file(sock, data_sock, filename, response_filename):
    remote_filename = os.path.basename(filename)
    print(f">>> RETR COMMAND: Requesting file: {remote_filename}", flush=True)

    command = b"RETR " + bytes(remote_filename, "utf-8") + b"\r\n"
    print(f"[>] Sending command to server: {command.decode().strip()}", flush=True)
    sock.sendall(command)

    ctrl_response = receive_data(sock)
    print("[<] Server response (control connection):", flush=True)
    print(ctrl_response.decode(errors='ignore'), flush=True)

    file_data = receive_data(data_sock)
    print(f"[<] Received {len(file_data)} bytes from data connection", flush=True)

    try:
        with open(response_filename, "wb") as file:
            file.write(file_data)
        print(f"[+] File saved as {response_filename}", flush=True)
    except Exception as e:
        print(f"[!] Failed to save file: {e}", flush=True)

    print(">>> RETR END\n", flush=True)



def main(command: str, filename, response_filename):
    print("=== FTP CLIENT STARTED ===", flush=True)
    server_address = ('ftp.dlptest.com', 21)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(5)
        sock.connect(server_address)
        print("[+] Connected to server", flush=True)

        data = receive_data(sock)
        print(data.decode(errors='ignore'), flush=True)

        username = "dlpuser"
        password = "rNrKYTX9g7z3RgJRmxWuGHbeu"

        print("[>] Sending USER", flush=True)
        sock.sendall(b"USER " + bytes(username, "utf-8") + b"\r\n")
        print(receive_data(sock).decode(errors='ignore'), flush=True)

        print("[>] Sending PASS", flush=True)
        sock.sendall(b"PASS " + bytes(password, "utf-8") + b"\r\n")
        print(receive_data(sock).decode(errors='ignore'), flush=True)

        print("[>] Entering PASV mode", flush=True)
        sock.sendall(b"PASV\r\n")
        response = receive_data(sock)
        print(response.decode(errors='ignore'), flush=True)

        start = response.decode().find("(") + 1
        end = response.decode().find(")")
        data = response.decode()[start:end].split(",")
        datahost = ".".join(data[:4])
        dataport = int(data[4]) * 256 + int(data[5])
        print(f"[+] PASV -> {datahost}:{dataport}", flush=True)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as data_sock:
            data_sock.settimeout(5)
            data_sock.connect((datahost, dataport))
            print("[+] Data connection established", flush=True)

            if command == "ls":
                list_files(sock, data_sock)
            elif command == "upload":
                upload_file(sock, data_sock, filename)
            elif command == "download":
                download_file(sock, data_sock, filename, response_filename)
            else:
                print("[!] UNKNOWN COMMAND", flush=True)

            data_sock.close()

        final_response = receive_data(sock)
        print("[FINAL RESPONSE]:", flush=True)
        print(final_response.decode(errors='ignore'), flush=True)

    print("=== FTP CLIENT ENDED ===", flush=True)

if __name__ == "__main__":
    receive_filename = ""
    filename = ""

    if len(sys.argv[1:]) < 1:
        print("[!] Missing arguments. Usage: ls | upload <filename> | download <filename> <output>", flush=True)
        sys.exit(1)

    command = sys.argv[1]
    if command in ["upload", "download"]:
        if len(sys.argv) < 3:
            print("[!] Missing filename", flush=True)
            sys.exit(1)
        filename = sys.argv[2]
        if command == "download":
            if len(sys.argv) < 4:
                print("[!] Missing output filename for download", flush=True)
                sys.exit(1)
            receive_filename = sys.argv[3]

    main(command, filename, receive_filename)
