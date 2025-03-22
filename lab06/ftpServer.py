import os
import socket
import threading

HOST = '127.1.1.1'
PORT = 2121
USERNAME = 'userTEST'
PASSWORD = '12345'

class FTPServer:
    def __init__(self):
        self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.control_socket.bind((HOST, PORT))
        self.control_socket.listen(5)
        print(f"[+] FTP Server started on {HOST}:{PORT}")

    def start(self):
        while True:
            client_socket, addr = self.control_socket.accept()
            print(f"[+] Connection from {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, conn):
        conn.sendall(b"220 Simple FTP Server Ready\r\n")
        authenticated = False
        current_dir = os.getcwd()
        data_addr = None

        while True:
            try:
                cmd = conn.recv(1024).decode('utf-8').strip()
                if not cmd:
                    break
                print(f"Command: {cmd}")
                parts = cmd.split(' ', 1)
                command = parts[0].upper()
                arg = parts[1] if len(parts) > 1 else None

                if command == "USER":
                    if arg == USERNAME:
                        conn.sendall(b"331 User name okay, need password.\r\n")
                    else:
                        conn.sendall(b"530 Invalid username.\r\n")

                elif command == "PASS":
                    if arg == PASSWORD:
                        authenticated = True
                        conn.sendall(b"230 User logged in, proceed.\r\n")
                    else:
                        conn.sendall(b"530 Login incorrect.\r\n")

                elif not authenticated:
                    conn.sendall(b"530 Please login with USER and PASS.\r\n")

                elif command == "PWD":
                    conn.sendall(f'257 "{current_dir}" is the current directory.\r\n'.encode())

                elif command == "CWD":
                    try:
                        os.chdir(arg)
                        current_dir = os.getcwd()
                        conn.sendall(b"250 Directory successfully changed.\r\n")
                    except:
                        conn.sendall(b"550 Failed to change directory.\r\n")

                elif command == "PORT":
                    try:
                        nums = list(map(int, arg.split(',')))
                        ip = '.'.join(map(str, nums[:4]))
                        port = (nums[4] << 8) + nums[5]
                        data_addr = (ip, port)
                        conn.sendall(b"200 PORT command successful.\r\n")
                    except:
                        conn.sendall(b"501 Syntax error in parameters or arguments.\r\n")

                elif command == "NLST":
                    if not data_addr:
                        conn.sendall(b"425 Use PORT first.\r\n")
                        continue
                    try:
                        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        data_socket.connect(data_addr)
                        files = os.listdir(current_dir)
                        for f in files:
                            data_socket.sendall((f + '\r\n').encode())
                        data_socket.close()
                        conn.sendall(b"226 Transfer complete.\r\n")
                    except:
                        conn.sendall(b"425 Can't open data connection.\r\n")

                elif command == "STOR":
                    print(f"[SERVER] Received STOR for: {arg}")
                    if not data_addr:
                        conn.sendall(b"425 Use PORT first.\r\n")
                        continue
                    filepath = os.path.join(current_dir, arg)
                    print(f"[SERVER] Will save file to: {filepath}")
                    try:
                        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        data_socket.connect(data_addr)
                        with open(filepath, 'wb') as f:
                            while True:
                                data = data_socket.recv(1024)
                                if not data:
                                    break
                                f.write(data)
                        data_socket.close()
                        print(f"[SERVER] File saved: {filepath}")
                        conn.sendall(b"226 Transfer complete.\r\n")
                    except Exception as e:
                        print(f"[-] STOR failed: {e}")
                        conn.sendall(b"426 Transfer failed.\r\n")

                elif command == "RETR":
                    if not data_addr:
                        conn.sendall(b"425 Use PORT first.\r\n")
                        continue
                    filepath = os.path.join(current_dir, arg)
                    print(f"[SERVER] RETR requested: {filepath}")
                    try:
                        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        data_socket.connect(data_addr)
                        with open(filepath, 'rb') as f:
                            while True:
                                data = f.read(1024)
                                if not data:
                                    break
                                data_socket.sendall(data)
                        data_socket.close()
                        conn.sendall(b"226 Transfer complete.\r\n")
                    except Exception as e:
                        print(f"[-] RETR failed: {e}")
                        conn.sendall(b"550 Failed to retrieve file.\r\n")

                elif command == "QUIT":
                    conn.sendall(b"221 Goodbye.\r\n")
                    conn.close()
                    print("[SERVER] Client disconnected via QUIT")
                    break
                else:
                    conn.sendall(b"502 Command not implemented.\r\n")

            except Exception as e:
                print(f"[-] Error: {e}")
                break

if __name__ == "__main__":
    server = FTPServer()
    server.start()
