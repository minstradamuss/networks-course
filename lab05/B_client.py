# -*- coding: utf-8 -*-

import socket

HOST = '127.0.0.1'
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

try:
    while True:
        command = input("Enter the command to execute on the server (or 'exit' to exit): \n")
        if command.lower() == 'exit':
            client_socket.send(command.encode())
            client_socket.close()
            break

        client_socket.send(command.encode())
        print("COMMAND OUTPUT:")

        while True:
            output = client_socket.recv(1024)
            if not output:
                break
            try:
                decoded_output = output.decode('cp866')
            except UnicodeDecodeError:
                decoded_output = output.decode('utf-8', errors='ignore')

            if "END OF COMMAND OUTPUT" in decoded_output:
                print(decoded_output.replace("END OF COMMAND OUTPUT", ""))
                break
            print(decoded_output, end='')

except Exception as e:
    print("Error:", e)
    client_socket.close()
