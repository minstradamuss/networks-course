# -*- coding: utf-8 -*-

import socket
import base64
import ssl
import sys
import getpass

def ensure_utf8(text):
    if isinstance(text, bytes):
        return text.decode('utf-8', errors='ignore')
    return str(text)

def send_email(sender_email, sender_password, receiver_email, subject, message, message_type='text/plain'):
    smtp_server = 'smtp.mail.ru'
    port = 587

    client_socket = socket.create_connection((smtp_server, port))
    response = client_socket.recv(1024).decode()
    print(response)

    client_socket.sendall(b'EHLO example.com\r\n')
    response = client_socket.recv(1024).decode()
    print(response)

    client_socket.sendall(b'STARTTLS\r\n')
    response = client_socket.recv(1024).decode()
    print(response)

    context = ssl.create_default_context()
    
    ssl_socket = context.wrap_socket(client_socket, server_hostname=smtp_server)

    ssl_socket.sendall(b'EHLO example.com\r\n')
    response = ssl_socket.recv(1024).decode()
    print(response)

    ssl_socket.sendall(b'AUTH LOGIN\r\n')
    response = ssl_socket.recv(1024).decode()
    print(response)

    ssl_socket.sendall(base64.b64encode(sender_email.encode()) + b'\r\n')
    response = ssl_socket.recv(1024).decode()
    print(response)
    
    ssl_socket.sendall(base64.b64encode(sender_password.encode()) + b'\r\n')
    response = ssl_socket.recv(1024).decode()
    print(response)
    
    ssl_socket.sendall(f'MAIL FROM: <{sender_email}>\r\n'.encode())
    response = ssl_socket.recv(1024).decode()
    print(response)

    ssl_socket.sendall(f'RCPT TO: <{receiver_email}>\r\n'.encode())
    response = ssl_socket.recv(1024).decode()
    print(response)

    ssl_socket.sendall(b'DATA\r\n')
    response = ssl_socket.recv(1024).decode()
    print(response)

    email_message = (
        f"From: {sender_email}\r\n"
        f"To: {receiver_email}\r\n"
        f"Subject: {subject}\r\n"
        f"Content-Type: {message_type}; charset=utf-8\r\n"
        f"\r\n"
        f"{message}\r\n"
        f".\r\n"
    )

    ssl_socket.sendall(email_message.encode())
    response = ssl_socket.recv(1024).decode()
    print(response)

    ssl_socket.sendall(b'QUIT\r\n')
    response = ssl_socket.recv(1024).decode()
    print(response)

    ssl_socket.close()
    print('Email sent successfully!')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Format: {sys.argv[0]} <receiver_email> <sender_password>")
        sys.exit(1)

    sender_email = 'st115109@student.spbu.ru'
    receiver_email = sys.argv[1]
    sender_password = getpass.getpass("Enter your email password: ")

    subject = ensure_utf8('Цитата')
    message_txt = ensure_utf8('Тому, кто наукам сердце отдал: почёт, признание и слава!')
    message_html = ensure_utf8('<h1>Цитата</h1><p>Тому, кто наукам сердце отдал: почёт, признание и слава!</p>')

    send_email(sender_email, sender_password, receiver_email, subject, message_txt, 'text/plain')
    send_email(sender_email, sender_password, receiver_email, subject, message_html, 'text/html')
