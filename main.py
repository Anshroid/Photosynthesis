import random

import pygame
from pygame.locals import *

from carbon_dioxide import CarbonDioxide
from oxygen import Oxygen
from water import Water

# Define Colours
WHITE = (255, 255, 255)
DIRT = (143, 103, 73)
SKY = (0, 181, 226)
GRASS = (0, 154, 23)
SUN = (252, 229, 93)
GLUCOSE = (167, 255, 61)
BUTTON = (92, 255, 187)

# FPS
FPS = 60

# Initialise Screen
pygame.init()
screen = pygame.display.set_mode((600, 1000))
pygame.display.set_caption("Photosynthesis: The Game")

# Load sprites
tree = pygame.image.load("Assets/tree.png")
roots = pygame.image.load("Assets/roots.png").convert_alpha()
leaf = pygame.image.load("Assets/leaf.png")

# Load Font
glucose_font = pygame.font.Font("Assets/Montserrat-Medium.ttf", 30)
shop_font = pygame.font.Font("Assets/Montserrat-Medium.ttf", 20)

# List of leaves that can be on the tree
leaf_positions = [[152, 429, 78], [181, 444, 106], [227, 450, 90], [155, 372, 54], [143, 333, 47], [155, 291, 339],
                  [223, 379, 301], [191, 230, 298], [249, 264, 284], [288, 299, 275], [255, 224, 16], [328, 234, 304],
                  [388, 292, 175], [318, 341, 93], [319, 373, 255], [320, 434, 166], [355, 413, 174], [388, 384, 172],
                  [411, 346, 197], [251, 342, 370], [319, 473, 191], [345, 301, 310], [192, 329, 296], [251, 457, 130],
                  [411, 315, 243], [370, 248, 272]]

# Set up root growth overlays
root_growth_radii = [90, 110, 140, 160, 300]
root_growths = [pygame.Surface((400, 250), SRCALPHA) for radius in root_growth_radii]
for radius, surface in zip(root_growth_radii, root_growths):
    surface.fill((0, 0, 0, 0))
    pygame.draw.circle(surface, (0, 0, 0), (200, radius - 5), radius)

# Set up revealed leaves
revealed_leaves = [random.choice(leaf_positions)]
leaf_positions.remove(revealed_leaves[0])

# Roots are minimally grown at first
root_growth_stage = 0

# Set up logic control
texts = pygame.sprite.Group()
clock = pygame.time.Clock()
glucose = 0

# Button hitboxes
button_left = pygame.Rect(50, 850, 225, 100)
button_right = pygame.Rect(325, 850, 225, 100)

# Game Loop
running = True
while running:
    # Check for events
    for event in pygame.event.get():
        # If application is exited
        if event.type == QUIT:
            pygame.quit()
            exit()

        # If a button is clicked
        elif event.type == MOUSEBUTTONDOWN:
            if button_left.collidepoint(pygame.mouse.get_pos()):
                if ((26 - len(leaf_positions)) * 25) < glucose and len(leaf_positions) > 0:
                    glucose -= ((26 - len(leaf_positions)) * 25)
                    for i in range(random.randint(1, 3)):
                        random.shuffle(leaf_positions)
                        if len(leaf_positions) != 0:
                            revealed_leaves.append(leaf_positions.pop())

            if button_right.collidepoint(pygame.mouse.get_pos()):
                if ((4 * (root_growth_stage + 1)) * 5) < glucose and root_growth_stage < 4:
                    glucose -= ((4 * root_growth_stage) * 5)
                    root_growth_stage += 1

    # (Left, Top, Width, Height)
    # Draw on each base part of the screen
    screen.fill(SKY, (0, 0, 600, 600))
    screen.fill(DIRT, (0, 600, 600, 400))
    screen.fill(GRASS, (0, 600, 600, 50))
    pygame.draw.circle(screen, SUN, (500, 100), 50)

    # Draw the tree
    screen.blit(tree, (185, 243))

    # Multiply overlay the root growth onto the roots
    roots_draw = roots.copy()
    roots_draw.blit(root_growths[root_growth_stage], (0, 0), special_flags=BLEND_RGBA_MULT)

    # Draw the resulting roots
    screen.blit(roots_draw, (105, 600))

    # Draw in every currently revealed leaf
    for leaf_pos in revealed_leaves:
        screen.blit(pygame.transform.rotate(leaf, leaf_pos[2]), (leaf_pos[0], leaf_pos[1]))

    # Randomly based on the root growth, spawn a H2O molecule
    if random.randint(0, 4000) < root_growth_radii[root_growth_stage]:
        Water(texts)

    # Randomly based on the leaf count, spawn an O2 molecule
    if random.randint(0, 4000) < ((26 - len(leaf_positions)) / 26) * 800:
        Oxygen(texts)

    # Update all existing molecule positions.
    texts.update()

    # Draw in molecules
    texts.draw(screen)

    # Draw in glucose
    text = glucose_font.render("C₆H₁₂O₆:" + str(int(glucose)) + "mol", True, GLUCOSE)
    screen.blit(text, (0, 0))

    # Update glucose level
    glucose += ((26 - len(leaf_positions)) / 52) * root_growth_radii[root_growth_stage] * 0.01

    # Have a chance of spawning a carbon dioxide molecule
    if random.randint(0, 4000) < ((26 - len(leaf_positions)) / 52) * root_growth_radii[root_growth_stage] * 10:
        CarbonDioxide(texts)

    # Draw buttons onto the bottom of the screen
    pygame.draw.rect(screen, BUTTON, (50, 850, 225, 100))
    pygame.draw.rect(screen, BUTTON, (325, 850, 225, 100))

    left_text = shop_font.render("Upgrade Chloroplast:", True, WHITE)
    left_price_text = glucose_font.render(str((26 - len(leaf_positions)) * 25) if len(leaf_positions) != 0 else "MAX",
                                          True, WHITE)
    right_text = shop_font.render("Upgrade Roots:", True, WHITE)
    right_price_text = glucose_font.render(str((4 * (root_growth_stage + 1)) * 5) if root_growth_stage < 4 else "MAX",
                                           True, WHITE)

    screen.blit(left_text, (55, 850))
    screen.blit(left_price_text, (135, 875))
    screen.blit(right_text, (360, 850))
    screen.blit(right_price_text, (415, 875))

    # Update the screen
    pygame.display.update()

    # Don't over- or underspeed the FPS
    clock.tick(FPS)
