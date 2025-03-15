# -*- coding: utf-8 -*-

import socket
import ssl
import base64
import sys
import getpass

def ensure_utf8(text):
    if isinstance(text, bytes):
        return text.decode('utf-8', errors='ignore')
    return str(text)

def send_email(sender_email, sender_password, receiver_email, subject, body, message_type='text/plain', image_filename=None):
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
    with context.wrap_socket(client_socket, server_hostname=smtp_server) as ssl_socket:
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

        if "535" in response:
            print("Authentication failed")
            return

        ssl_socket.sendall(f'MAIL FROM:<{sender_email}>\r\n'.encode())
        response = ssl_socket.recv(1024).decode()
        print(response)

        ssl_socket.sendall(f'RCPT TO:<{receiver_email}>\r\n'.encode())
        response = ssl_socket.recv(1024).decode()
        print(response)
        
        ssl_socket.sendall(b'DATA\r\n')
        response = ssl_socket.recv(1024).decode()
        print(response)

        boundary = "my-boundary-123"

        email_message = f"From: {sender_email}\r\n"
        email_message += f"To: {receiver_email}\r\n"
        email_message += f"Subject: {subject}\r\n"
        email_message += "MIME-Version: 1.0\r\n"
        email_message += f"Content-Type: multipart/mixed; boundary={boundary}\r\n\r\n"

        email_message += f"--{boundary}\r\n"
        email_message += f"Content-Type: {message_type}; charset=utf-8\r\n\r\n"
        email_message += f"{body}\r\n\r\n"

        if image_filename:
            try:
                with open(image_filename, "rb") as image_file:
                    encoded_image = base64.b64encode(image_file.read()).decode()

                email_message += f"--{boundary}\r\n"
                email_message += "Content-Type: image/jpeg\r\n"
                email_message += "Content-Transfer-Encoding: base64\r\n"
                email_message += f"Content-Disposition: attachment; filename=\"{image_filename.split('/')[-1]}\"\r\n\r\n"
                email_message += encoded_image + "\r\n"
                email_message += f"--{boundary}--\r\n"

            except FileNotFoundError:
                print(f"Image file '{image_filename}' not found. Sending email without attachment.")

        ssl_socket.sendall(email_message.encode())
        ssl_socket.sendall(b'\r\n.\r\n')
        response = ssl_socket.recv(1024).decode()
        print(response)

        ssl_socket.sendall(b'QUIT\r\n')
        response = ssl_socket.recv(1024).decode()
        print(response)

    print('Email sent successfully!')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Format: {sys.argv[0]} <receiver_email> <sender_password>")
        sys.exit(1)

    sender_email = "st115109@student.spbu.ru"
    receiver_email = sys.argv[1]
    sender_password = getpass.getpass("Enter your email password: ")

    subject = ensure_utf8('Цитата')
    message_txt = ensure_utf8('Тому, кто наукам сердце отдал: почёт, признание и слава!')
    message_html = ensure_utf8('<h1>Цитата</h1><p>Тому, кто наукам сердце отдал: почёт, признание и слава!</p>')

    image_path = r"C:\Users\User\Source\Repos\networks-course\lab05\image.jpeg"

    send_email(sender_email, sender_password, receiver_email, subject, message_txt, "text/plain", image_path)
    send_email(sender_email, sender_password, receiver_email, subject, message_html, "text/html", image_path)
