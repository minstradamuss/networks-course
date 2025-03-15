import socket
import subprocess

HOST = '127.0.0.1'
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"Server is listening on {HOST}:{PORT}")

print("Waiting for client...")
client_socket, addr = server_socket.accept()
print("Connected by ", addr)

try:
    while True:
        command = client_socket.recv(1024).decode()
        if command.lower() == 'exit':
            client_socket.close()
            server_socket.close()
            break
        print(f"Received command: {command}")

        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        while True:
            output = process.stdout.readline()
            client_socket.sendall(output)
            return_code = process.poll()
            if return_code is not None:
                print('RETURN CODE', return_code)
                for output in process.stdout.readlines():
                    client_socket.sendall(output)
                client_socket.sendall("END OF COMMAND OUTPUT".encode())
                break
except:
    client_socket.close()
    server_socket.close()