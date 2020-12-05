import paho.mqtt.client as mqtt  # import the client
import struct
import pygame
import colors

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

SCREEN_WIDTH = int(Width) * 10
W_R = Width / SCREEN_WIDTH
SCREEN_HEIGHT = int(Length) * 10
H_R = Length / SCREEN_HEIGHT
SCREEN_DEPTH = int(Height) * 10
D_R = Height / SCREEN_DEPTH

rectangle = pygame.rect.Rect(int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2), 17, 17)
slider = pygame.rect.Rect(SCREEN_WIDTH - 17, 0, 17, 17)
slider_draging = False
rectangle_draging = False


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
                if slider.collidepoint(event.pos):
                    slider_draging = True
                    mouse_x, mouse_y = event.pos
                    offset_y = slider.y - mouse_y

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                slider_draging = False
                rectangle_draging = False

        elif event.type == pygame.MOUSEMOTION:
            if rectangle_draging:
                mouse_x, mouse_y = event.pos
                rectangle.x = mouse_x + offset_x
                rectangle.y = mouse_y + offset_y
                new_lengths = [distance(rectangle.x * W_R, rectangle.y * H_R, slider.y * D_R, x2, y2, z2) for x2, y2, z2 in [
                    (0, 0, 0), (Width, 0, 0), (Width, Length, 0), (0, Length, 0)]]
                for name, length in zip(["A", "B", "C", "D"], new_lengths):
                    client.publish(name, str(length))# struct.pack('f', length))
                    print("{} Target: {} cm".format(name,length))
            elif slider_draging:
                mouse_x, mouse_y = event.pos
                slider.y = mouse_y + offset_y
                new_lengths = [distance(rectangle.x * W_R, rectangle.y * H_R, slider.y * D_R, x2, y2, z2) for x2, y2, z2 in [
                    (0, 0, 0), (Width, 0, 0), (Width, Length, 0), (0, Length, 0)]]
                for name, length in zip(["A", "B", "C", "D"], new_lengths):
                    client.publish(name, str(length))# struct.pack('f', length))  # Publish
                    print("{} Target: {} cm".format(name,length))

    # - draws (without updates) -

    screen.fill(colors.WHITE)

    pygame.draw.rect(screen, colors.RED, rectangle)
    pygame.draw.rect(screen, colors.BLACK, slider)

    pygame.display.flip()

    # - constant game speed / FPS -

    clock.tick(FPS)


# - end -
client.loop_stop()
pygame.quit()
