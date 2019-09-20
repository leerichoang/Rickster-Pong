import pygame


class Backpaddle(pygame.Rect):
    def __init__(self, velocity, up_key, down_key, *args, **kwargs):
        self.velocity = velocity
        self.up_key = up_key
        self.down_key = down_key
        super().__init__(*args, **kwargs)

    def move_paddle(self, board_height):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[self.up_key]:
            if self.y - self.velocity > 0:
                self.y -= self.velocity

        if keys_pressed[self.down_key]:
            if self.y + self.velocity < board_height - self.height:
                self.y += self.velocity


class Sidepaddle(pygame.Rect):
    def __init__(self, velocity, left_key, right_key, *args, **kwargs):
        self.velocity = velocity
        self.left_key = left_key
        self.right_key = right_key
        super().__init__(*args, **kwargs)

    def move_paddle(self, board_width):
        keys_pressed = pygame.key.get_pressed()
        # Check Right Boundry
        if keys_pressed[self.right_key]:
            if self.x + self.velocity < (board_width / 2) - self.width + 5:
                self.x += self.velocity

        if keys_pressed[self.left_key]:
            if self.x - self.velocity > 0:
                self.x -= self.velocity
