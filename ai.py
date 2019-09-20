import pygame


class AiBackPaddle(pygame.Rect):
    def __init__(self, velocity, balls, *args, **kwargs):
        self.velocity = velocity
        self.balls = balls
        super().__init__(*args, **kwargs)

    def move_paddle(self, board_height):
        for ball in self.balls:
            if self.y + self.velocity < board_height - self.height:
                if ball.y > self.y:
                    self.y += self.velocity
            if self.y - self.velocity > 0:
                if ball.y < self.y:
                    self.y -= self.velocity


class AiSidePaddle(pygame.Rect):
    def __init__(self, velocity, balls, *args, **kwargs):
        self.velocity = velocity
        self.balls = balls
        super().__init__(*args, **kwargs)

    def move_paddle(self, board_width):
        for ball in self.balls:
            if self.x + self.velocity < board_width - self.width:
                if ball.x > self.x:
                    self.x += self.velocity

            if self.x - self.velocity > (board_width / 2) - 5:
                if ball.x < self.x:
                    self.x -= self.velocity
