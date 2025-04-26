import socket
import pygame
import sys

HOST = '127.0.0.1'
PORT = 65432

pygame.init()
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Paint Client")

drawing = False
last_pos = None
brush_color = (0, 0, 0)
brush_size = 4

screen.fill((255, 255, 255))

def send_message(sock, message):
    sock.sendall(message.encode('utf-8'))

def main():
    last_pos = None
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print("Connected to server.")
        except Exception as e:
            print(f"Failed to connect: {e}")
            sys.exit()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    drawing = True
                    send_message(s, "mousedown")
                elif event.type == pygame.MOUSEBUTTONUP:
                    drawing = False
                    send_message(s, "mouseup")
                    last_pos = None
                elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    send_message(s, f"{pos[0]},{pos[1]}")
                    if last_pos:
                        pygame.draw.line(screen, brush_color, last_pos, pos, brush_size)
                    last_pos = pos if drawing else None

            pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
