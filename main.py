import random
import sys
from pygame import *
from paddles import *
from ball import Ball
from ai import *


class Pong:
    # Defining Game Class
    HEIGHT = 500
    WIDTH = 1000

    paddle_short = 5
    paddle_long = 50
    paddle_velocity = 10

    ball_radius = 5
    ball_velocity = 2

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    game_over = False
    # Sounds

    def __init__(self):
        pygame.init()

        # Intializing Audio files into game.
        self.music = pygame.mixer.music.load('bgmusic.mp3')
        self.loseaudio = pygame.mixer.Sound('losescreen.wav')
        self.winaudio = pygame.mixer.Sound('winscreen.wav')
        self.pointlossaudio = pygame.mixer.Sound('pointloss.wav')
        self.pointwinaudio = pygame.mixer.Sound('pointwin.wav')
        self.backpaddleaudio = pygame.mixer.Sound('backboop.wav')
        self.sidepaddleaudio = pygame.mixer.Sound('sideboop.wav')

        # Creating Screen
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()

        # scores
        self.score_player = 0
        self.score_ai = 0

        self.paddles = []
        self.sidepaddles = []
        self.balls = []
        self.aibackpaddle = []
        self.aisidepaddle = []

        # Initialising text screens
        self.font = pygame.font.SysFont(None, 40)
        self.text = self.font.render(str(self.score_player) + "/5       " + str(self.score_ai) + "/5", True, self.WHITE)
        self.aiwin = self.font.render("Computer Wins", True, self.WHITE)
        self.playerwin = self.font.render("You Wins", True, self.WHITE)
        self.instruct = self.font.render("Press anykey to play agian, press corner X to quit", True, self.WHITE)

        # defining the Padddles
        self.sidepaddles.append(Sidepaddle(
            self.paddle_velocity,
            pygame.K_LEFT,
            pygame.K_RIGHT,
            self.WIDTH / 4 - self.paddle_long / 2,
            0,
            self.paddle_long,
            self.paddle_short
        ))
        self.sidepaddles.append(Sidepaddle(
            self.paddle_velocity,
            pygame.K_LEFT,
            pygame.K_RIGHT,
            self.WIDTH / 4 - self.paddle_long / 2,
            self.HEIGHT - self.paddle_short,
            self.paddle_long,
            self.paddle_short
        ))
        self.paddles.append(Backpaddle(
            self.paddle_velocity,
            pygame.K_UP,
            pygame.K_DOWN,
            0,
            self.HEIGHT / 2 - self.paddle_long / 2,
            self.paddle_short,
            self.paddle_long
        ))

        self.balls.append(Ball(
            self.WIDTH / 2 - self.ball_radius / 2,
            self.HEIGHT / 2 - self.ball_radius / 2,
            self.ball_radius,
            self.ball_radius
        ))

        self.aibackpaddle.append(AiBackPaddle(
            self.paddle_velocity - 5,
            self.balls,
            self.WIDTH-self.paddle_short,
            self.HEIGHT / 2 - self.paddle_long / 2,
            self.paddle_short,
            self.paddle_long
        ))

        self.aisidepaddle.append(AiSidePaddle(
            self.paddle_velocity - 5,
            self.balls,
            self.WIDTH * .75 - self.paddle_long / 2,
            0,
            self.paddle_long,
            self.paddle_short
        ))

        self.aisidepaddle.append(AiSidePaddle(
            self.paddle_velocity,
            self.balls,
            self.WIDTH * .75 - self.paddle_long / 2,
            self.HEIGHT - self.paddle_short,
            self.paddle_long,
            self.paddle_short
        ))
    # Check's walls and reset's pong ball

    def check_wall(self):
        for ball in self.balls:
            if ball.x > self.WIDTH or ball.x < 0:
                if ball.x > self.WIDTH/2:
                    self.score_player += 1
                    self.pointwinaudio.play()
                    ball.velocity = random.randint(1, 2)

                else:
                    self.score_ai += 1
                    self.pointlossaudio.play()
                    ball.velocity = random.randint(-2, -1)
                ball.x = self.WIDTH / 2 - self.ball_radius / 2
                ball.y = self.HEIGHT / 2 - self.ball_radius / 2
                ball.velocity = random.randint(-1, 1)
                ball.angle = random.randrange(-5, 5)

            if ball.y > self.HEIGHT - self.ball_radius or ball.y < 0:
                if ball.x > self.WIDTH/2:
                    self.score_player += 1
                    self.pointwinaudio.play()
                    ball.velocity = random.randint(1, 2)
                else:
                    self.score_ai += 1
                    self.pointlossaudio.play()
                    ball.velocity = random.randint(-2, -1)
                ball.x = self.WIDTH / 2 - self.ball_radius / 2
                ball.y = self.HEIGHT / 2 - self.ball_radius / 2
                ball.angle = random.randint(-5, 5)

    # Check collision for player paddle and Ball
    def check_backpaddle(self):
        for ball in self.balls:
            for paddle in self.paddles:
                if ball.colliderect(paddle):
                    self.backpaddleaudio.play()
                    ball.velocity = -ball.velocity
                    ball.velocity += random.randint(1, 2)
                    ball.angle = random.randint(-5, 5)
                    break

    # Check collision for side paddle and Ball
    def check_sidepaddle(self):
        for ball in self.balls:
            for paddle in self.sidepaddles:
                if ball.colliderect(paddle):
                    self.sidepaddleaudio.play()

                    ball.angle = -ball.angle

                    break

    # Check's collision on AI paddle and Ball
    def check_aibackpaddle(self):
        for ball in self.balls:
            for paddle in self.aibackpaddle:
                if ball.colliderect(paddle):
                    self.backpaddleaudio.play()
                    ball.velocity = -ball.velocity
                    ball.velocity -= random.randint(1, 2)
                    ball.angle = random.randint(-5, 5)
                    break

    # Checks a collision between AI side paddles and Ball
    def check_aisidepaddle(self):
        for ball in self.balls:
            for paddle in self.aisidepaddle:
                if ball.colliderect(paddle):
                    self.sidepaddleaudio.play()
                    ball.angle = -ball.angle
                    break

    # Shows winning screen Ket check
    def show_winner_screen(self):
        waiting = True
        self.screen.fill(self.BLACK)
        while waiting:
            self.clock.tick(60)
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif events.type == pygame.KEYUP and events.type != pygame.K_ESCAPE:
                    waiting = False
                    self.game_over = False

    # Start the game
    def game_loop(self):
        # Loop to quite when Escape is pressed
        pygame.mixer.music.play(-1)
        while True:
            # Event Stage
            if self.game_over:
                self.show_winner_screen()
                self.game_over = False
                pygame.mixer.music.play(True, True)

                self.score_ai = 0
                self.score_player = 0

            for events in pygame.event.get():
                if events.type == pygame.KEYDOWN and events.key == pygame.K_ESCAPE:
                    sys.exit(0)

            # Update Stage
            self.check_backpaddle()
            self.check_wall()
            self.check_sidepaddle()
            self.check_aibackpaddle()
            self.check_aisidepaddle()

            # Draw Stage
            # Black out screen after every draw
            self.screen.fill((0, 0, 0))

            # Pong Net
            pygame.draw.rect(self.screen, self.WHITE, pygame.Rect((self.WIDTH / 2) - 1, 0, 2, self.HEIGHT))
            self.text = self.font.render(str(self.score_player) + "/5       " + str(self.score_ai) + "/5",
                                         True, self.WHITE)
            self.screen.blit(self.text, (self.WIDTH / 2 - self.text.get_rect().width / 2, self.HEIGHT / 2 - 100))

            for sidepaddle in self.sidepaddles:
                sidepaddle.move_paddle(self.WIDTH)
                pygame.draw.rect(self.screen, self.WHITE, sidepaddle)

            for aipaddle in self.aibackpaddle:
                aipaddle.move_paddle(self.HEIGHT)
                pygame.draw.rect(self.screen, self.WHITE, aipaddle)

            for aisidepaddle in self.aisidepaddle:
                aisidepaddle.move_paddle(self.WIDTH)
                pygame.draw.rect(self.screen, self.WHITE, aisidepaddle)
            for paddle in self.paddles:
                paddle.move_paddle(self.HEIGHT)
                pygame.draw.rect(self.screen, self.WHITE, paddle)

            for ball in self.balls:
                ball.move_ball()
                pygame.draw.circle(self.screen, self.WHITE, (int(ball.x), int(ball.y)), self.ball_radius)

            if self.score_player == 5:
                self.winaudio.play()
                self.screen.fill(self.BLACK)
                self.game_over = True
                self.screen.blit(self.playerwin, (self.WIDTH / 2 - self.playerwin.get_rect().width / 2,
                                                  self.HEIGHT / 2 - 100))

            if self.score_ai == 5:
                self.loseaudio.play()
                self.screen.fill(self.BLACK)
                self.game_over = True
                self.screen.blit(self.aiwin, (self.WIDTH / 2 - self.aiwin.get_rect().width / 2, self.HEIGHT / 2 - 100))

            if self.game_over:
                pygame.mixer.music.pause()
                self.screen.blit(self.instruct, (self.WIDTH / 2 - self.instruct.get_rect().width / 2,
                                                 self.HEIGHT / 2 - 70))

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == '__main__':
    pong = Pong()
    pong.game_loop()
