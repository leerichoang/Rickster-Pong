import pygame
import random

move_ball = True


class Ball(pygame.Rect):
    def __init__(self, *args):

        if move_ball:
            self.velocity = random.randint(-2, 2)
            self.angle = random.randint(-5, 5)
        else:
            self.velocity = 0
            self.angle = 0
        super().__init__(*args)

    def move_ball(self):
        self.x += self.velocity
        self.y += self.angle
