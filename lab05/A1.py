# -*- coding: utf-8 -*-

import smtplib
import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys

def ensure_utf8(text):
    if isinstance(text, bytes):
        return text.decode('utf-8', errors='ignore')
    return str(text)

def send_email(sender_email, sender_password, receiver_email, subject, message, message_type='txt'):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = ensure_utf8(subject)

    if message_type == 'txt':
        msg.attach(MIMEText(ensure_utf8(message), 'plain'))
    elif message_type == 'html':
        msg.attach(MIMEText(ensure_utf8(message), 'html'))

    try:
        with smtplib.SMTP('smtp.mail.ru', 587) as server:
            server.ehlo()
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print(f"Email sent successfully to {receiver_email} ({message_type})")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Format: {sys.argv[0]} <receiver_email>")
        sys.exit(1)

    sender_email = 'st115109@student.spbu.ru'
    receiver_email = sys.argv[1]
    sender_password = getpass.getpass("Enter your email password: ")

    subject = ensure_utf8('Цитата')
    message_txt = ensure_utf8('Тому, кто наукам сердце отдал: почёт, признание и слава!')
    message_html = ensure_utf8('<h1>Цитата</h1><p>Тому, кто наукам сердце отдал: почёт, признание и слава!</p>')

    send_email(sender_email, sender_password, receiver_email, subject, message_txt, 'txt')
    send_email(sender_email, sender_password, receiver_email, subject, message_html, 'html')  
