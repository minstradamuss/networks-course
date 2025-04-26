import socket
import pygame
import sys

HOST = '127.0.0.1'
PORT = 65432

pygame.init()
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Paint Server")

drawing = False
last_pos = None
brush_color = (0, 0, 0)
brush_size = 4

screen.fill((255, 255, 255))
pygame.display.flip() 

def main():
    last_pos = None
    drawing = False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Waiting for a connection...")
        conn, addr = s.accept()
        print(f"Client connected from {addr}")

        with conn:
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        break

                try:
                    data = conn.recv(1024).decode('utf-8')
                    if not data:
                        print("Connection closed by client.")
                        break

                    if data == "mousedown":
                        drawing = True
                    elif data == "mouseup":
                        drawing = False
                        last_pos = None
                    else:
                        x, y = map(int, data.split(','))
                        if drawing and last_pos:
                            pygame.draw.line(screen, brush_color, last_pos, (x, y), brush_size)
                        last_pos = (x, y)
                    
                    pygame.display.flip()

                except Exception as e:
                    print(f"Error: {e}")
                    break

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
