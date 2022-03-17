import random

import pygame
from pygame.sprite import AbstractGroup


class Water(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup):
        super().__init__(*groups)
        self.font = pygame.font.Font("Assets/Montserrat-Medium.ttf", 30)
        self.image = self.font.render("H₂O", True, (14, 75, 239))
        self.x = random.randint(0, 550)
        self.y = random.randint(650, 950)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        if self.x != 300:
            self.x += 0.005 * (1500 - (40000 / abs(self.x - 300))) * (1 if self.x - 300 < 0 else -1)

        # How did I manage to introduce calculus into photosynthesis :facepalm:

        self.y -= 0.1 * (self.y - 600)

        self.rect.x = self.x
        self.rect.y = self.y

        if abs(self.x - 300) < 40:
            self.kill()
