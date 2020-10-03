import paho.mqtt.client as mqtt  # import the client
import struct
import pygame

BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
RED = (255,   0,   0)

FPS = 30

pygame.init()

pygame.display.set_caption("Tracking System")

# Connect to broker
broker_address = "127.0.0.1"
client = mqtt.Client("Master")
client.connect(broker_address)
client.loop_start()


def distance(x1, y1, z1, x2, y2, z2):
    return round(((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)**.5, 2)


#    Width
# A ------- B
# |         |
# |         | Length
# |         |
# D ------- C   # Height = Distance from the floor
Length, Width, Height = 41.91, 55.88, 30  # cm

# Setup pygame
rectangle = pygame.rect.Rect(176, 134, 17, 17)
slider = pygame.rect.Rect(176, 134, 17, 17)
slider_draging = False
rectangle_draging = False

SCREEN_WIDTH = int(Width) * 10
W_R = Width / SCREEN_WIDTH
SCREEN_HEIGHT = int(Height) * 10
H_R = Height / SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# TODO: Add Calibration Phase

clock = pygame.time.Clock()

running = True

while running:
    # - events -
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if rectangle.collidepoint(event.pos):
                    rectangle_draging = True
                    mouse_x, mouse_y = event.pos
                    offset_x = rectangle.x - mouse_x
                    offset_y = rectangle.y - mouse_y
                # elif slider: pass

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                rectangle_draging = False

        elif event.type == pygame.MOUSEMOTION:
            if rectangle_draging:
                mouse_x, mouse_y = event.pos
                rectangle.x = mouse_x + offset_x
                rectangle.y = mouse_y + offset_y
                z = 0
                new_lengths = [distance(rectangle.x * W_R, rectangle.y * H_R, z, x2, y2, z2) for x2, y2, z2 in [
                    (0, 0, 0), (Width, 0, 0), (Width, Length, 0), (0, Length, 0)]]
                for name, length in zip(["A", "B", "C", "D"], new_lengths):
                    client.publish(name, struct.pack('f', length))  # Publish
                    print(f"{name} Target: {length} cm")

    # - draws (without updates) -

    screen.fill(WHITE)

    pygame.draw.rect(screen, RED, rectangle)

    pygame.display.flip()

    # - constant game speed / FPS -

    clock.tick(FPS)


# - end -
client.loop_stop()
pygame.quit()
