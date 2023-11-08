import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600

# Couleurs
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Paramètres de la ligne (début et fin)
start_point = (WIDTH, 0)
end_point = (0, 200)

# Position initiale du point (milieu de la ligne)
point_x, point_y = (start_point[0] + end_point[0]) // 2, (start_point[1] + end_point[1]) // 2

# Création de la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Déplacement d'un point sur une ligne diagonale")

# Boucle principale
clock = pygame.time.Clock()
running = True
dragging = False  # Indique si le point est en cours de déplacement

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (point_x - 5 <= mouse_x <= point_x + 5) and (point_y - 5 <= mouse_y <= point_y + 5):
                dragging = True
        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False

    if dragging:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Calcul de la position du point pour qu'il reste sur la ligne
        dx = end_point[0] - start_point[0]
        dy = end_point[1] - start_point[1]
        line_length = (dx ** 2 + dy ** 2) ** 0.5
        if line_length > 0:
            t = ((mouse_x - start_point[0]) * dx + (mouse_y - start_point[1]) * dy) / (line_length ** 2)
            t = max(0, min(1, t))
            point_x = start_point[0] + t * dx
            point_y = start_point[1] + t * dy

    # Effacement de l'écran
    screen.fill((0, 0, 0))

    # Dessin de la ligne diagonale
    pygame.draw.line(screen, WHITE, start_point, end_point, 2)

    # Dessin du point
    pygame.draw.circle(screen, RED, (int(point_x), int(point_y)), 5)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

# import pygame
# import sys
# import math

# # Initialisation de Pygame
# pygame.init()

# # Dimensions de la fenêtre
# WIDTH, HEIGHT = 800, 600

# # Couleurs
# WHITE = (255, 255, 255)
# RED = (255, 0, 0)

# # Centre du cercle et rayon
# circle_center = (WIDTH // 2, HEIGHT // 2)
# circle_radius = 200

# # Paramètres du point
# point_radius = 10
# point_x = circle_center[0] + circle_radius
# point_y = circle_center[1]

# # Création de la fenêtre
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Déplacement d'un point sur un cercle")

# # Boucle principale
# clock = pygame.time.Clock()
# running = True
# dragging = False  # Indique si le point est en cours de déplacement

# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             mouse_x, mouse_y = pygame.mouse.get_pos()
#             if math.sqrt((point_x - mouse_x) ** 2 + (point_y - mouse_y) ** 2) < point_radius:
#                 dragging = True
#         if event.type == pygame.MOUSEBUTTONUP:
#             dragging = False

#     if dragging:
#         mouse_x, mouse_y = pygame.mouse.get_pos()
#         # Calcul de l'angle entre le centre du cercle et la position de la souris
#         angle = math.atan2(mouse_y - circle_center[1], mouse_x - circle_center[0])
#         point_x = circle_center[0] + circle_radius * math.cos(angle)
#         point_y = circle_center[1] + circle_radius * math.sin(angle)

#     # Effacement de l'écran
#     screen.fill((0, 0, 0))

#     # Dessin du cercle
#     pygame.draw.circle(screen, WHITE, circle_center, circle_radius, 2)

#     # Dessin du point
#     pygame.draw.circle(screen, RED, (int(point_x), int(point_y)), point_radius)

#     pygame.display.flip()
#     clock.tick(60)

# pygame.quit()
# sys.exit()
