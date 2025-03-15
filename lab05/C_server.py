# -*- coding: utf-8 -*-

import time
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

port = 12345
server.bind(("", port))

print(f"UDP Broadcast Server запущен на порту {port}")

while True:
    current_time = time.ctime()
    server.sendto(current_time.encode(), ('<broadcast>', port))
    print(f"Отправлено сообщение: {current_time}")
    time.sleep(1)
