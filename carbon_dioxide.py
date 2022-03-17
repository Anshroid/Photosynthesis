import random

import pygame
from pygame.sprite import AbstractGroup


class CarbonDioxide(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup):
        super().__init__(*groups)
        self.font = pygame.font.Font("Assets/Montserrat-Medium.ttf", 30)
        self.image = self.font.render("O₂", True, (230, 214, 151))
        self.destx = random.randint(0, 550)
        self.desty = random.randint(0, 350)
        self.x = random.randint(250, 300)
        self.y = random.randint(200, 350)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.x -= 0.01 * (self.x - self.destx)
        self.y -= 0.01 * (self.y - self.desty)

        self.rect.x = self.x
        self.rect.y = self.y

        if abs(self.x - self.destx) + abs(self.y - self.desty) < 40:
            self.kill()
