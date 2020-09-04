import random
import pygame
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((800, 500))
clock = pygame.time.Clock()

# Set up the font
playFont = pygame.font.Font("freesansbold.ttf", 33)
title_font = pygame.font.Font('bubble1.ttf', 80, bold=True)
font = pygame.font.Font("freesansbold.ttf", 25)
pygame.display.set_caption("Chasing Nemo")

background_image = pygame.image.load("waterss.jpg")
#game_over = pygame.image.load("sprites/gameover.png")
replay_button = pygame.image.load("sprites/replay.png")
starting_bg = pygame.image.load("images/ocean2.png")
starting_bg = pygame.transform.scale(starting_bg, (800, 500))

# Set some colors
SAND = (240, 194, 43)
not_hovered_play_color = (237, 218, 129)
hovered_play_color = (228, 194, 104)
GREY = (240, 240, 240)
WHITE = (255, 255, 255)

class Nemo():
    def __init__(self):
        self.Img = pygame.image.load("sprites/standing.png")
        self.WIDTH, self.HEIGHT = 60, 70
        self.Img = pygame.transform.scale(self.Img, (self.WIDTH, self.HEIGHT))
        self.image = self.Img
        self.x = 20
        self.y = 170
        self.g = -0.25 # Gravity
        self.up = 7 # Initial upward velocity
        self.t = 0 # time
        self.hitbox = pygame.Rect(self.x + 5, self.y, self.WIDTH - 15, self.HEIGHT - 5)

        self.runImg1 = pygame.image.load("sprites/R1.png")
        self.runImg2 = pygame.image.load("sprites/R2.png")
        self.runImg1 = pygame.transform.scale(self.runImg1, (self.WIDTH, self.HEIGHT))
        self.runImg2 = pygame.transform.scale(self.runImg2, (self.WIDTH, self.HEIGHT))

        self.runImgs = [self.runImg1, self.runImg2]

        self.count = 0
        self.jumping = False


    def jump(self):
        self.y -= self.up # Start jumping
        self.jumping = True

    def update(self):
        if self.y < 170: # check if jumping
            self.up = self.up + self.g * self.t # v = u + at
            self.y -= self.up
            self.t += 0.15 #  incrementing time

        if self.y > 170: # check if the jump is complete and resetting all variables
            self.y = 170
            self.t = 0
            self.up = 7
            self.jumping = False

        if self.jumping:
            self.hitbox = pygame.Rect(self.x + 5, self.y, self.WIDTH - 15, self.HEIGHT - 5)
            self.image = self.Img
        else:
            self.hitbox = pygame.Rect(self.x + 5, self.y, self.WIDTH - 15, self.HEIGHT - 5)
            self.image = self.runImgs[int(self.count) % 2]
            self.count += 0.2

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        #pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2) In case you want to see the hitbox

class Coral():
    def __init__(self):
        self.image0 = pygame.image.load("sprites/purple.png")
        self.image1 = pygame.image.load("sprites/orange.png")
        self.width0 = 45
        self.height = 44
        self.width1 = 50
        self.image0 = pygame.transform.scale(self.image0, (self.width0, self.height))
        self.image1 = pygame.transform.scale(self.image1, (self.width1, self.height))
        self.coral_dist = 450
        self.x0 = 1350
        self.y = 175
        self.x1 = self.x0 + self.coral_dist
        self.x2 = self.x1 + self.coral_dist - 100
        self.speed = 4

        self.hitbox0 = pygame.Rect(self.x0, self.y, self.width0, self.height)
        self.hitbox1 = pygame.Rect(self.x1, self.y, self.width1, self.height)
        self.hitbox2 = pygame.Rect(self.x2, self.y, self.width0, self.height)
        self.hitboxes = [self.hitbox0, self.hitbox1, self.hitbox2]

    def update(self):
        self.x0 -= self.speed
        self.x1 -= self.speed
        self.x2 -= self.speed

        self.hitbox0 = pygame.Rect(self.x0, self.y, self.width0, self.height)
        self.hitbox1 = pygame.Rect(self.x1, self.y, self.width1, self.height)
        self.hitbox2 = pygame.Rect(self.x2, self.y, self.width0, self.height)
        self.hitboxes = [self.hitbox0, self.hitbox1, self.hitbox2]

        if self.x0 < -30:
            #self.x0 = 1500
            self.x0 = 1400
        elif self.x1 < -30:
            #self.x1 = 1500
            self.x1 = self.x0 + random.randint(300, 700)
        elif self.x2 < -30:
            #self.x2 = 1500
            self.x2 = self.x1 + random.randint(300, 700)

    def draw(self, screen):
        screen.blit(self.image0, (self.x0, self.y))
        screen.blit(self.image1, (self.x1, self.y))
        screen.blit(self.image0, (self.x2, self.y))

class Ground():
    def __init__(self):
        self.ground_length = 1202
        self.image1 = pygame.image.load("sprites/ground.png")
        self.image1_x = 0
        self.image1_y = 200
        self.image2 = pygame.image.load("sprites/ground.png")
        self.image2_x = self.image1_x + self.ground_length
        self.image2_y = self.image1_y
        self.speed = 4


    def draw(self, screen):
        screen.blit(self.image1, (self.image1_x, self.image1_y))
        screen.blit(self.image2, (self.image2_x, self.image2_y))

    def update(self):
        self.image1_x -= self.speed
        self.image2_x -= self.speed

        if self.image1_x + self.ground_length < 0:
            self.image1_x = self.image2_x + self.ground_length
        elif self.image2_x + self.ground_length < 0:
            self.image2_x = self.image1_x + self.ground_length

def draw_text(text, font, color, surface, x, y):
  textobj = font.render(text, 1, color)
  textrect = textobj.get_rect()
  textrect.topleft = (x,y)
  surface.blit(textobj, textrect)

click = False 
# M A I N  L O O P
def mainMenu():
  running = True
  while running:
    screen.blit(starting_bg, (0,0))
    draw_text('CHASING NEMO', title_font, (SAND), screen, 145, 100)
    mx, my = pygame.mouse.get_pos()

    # PLAY button
    #play_button = pygame.Rect(300,400,200,50)
    #if play_button.collidepoint((mx, my)):
    #  if click:
    #    game()
    #pygame.draw.rect(screen, (not_hovered_play_color), play_button)

    # making play button interactive
    #if 300+200 > (mx,my)[0] > 300 and 400+50 > (mx,my)[1] > 400:
    #  pygame.draw.rect(screen, not_hovered_play_color, play_button)
    #else:
    #  pygame.draw.rect(screen, hovered_play_color, play_button)
    
    #draw_text('PLAY', playFont, (WHITE), screen, (300+55), (400+12))

    click = False
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == QUIT:
          pygame.quit()
          sys.exit()
        
        #if event.type == MOUSEBUTTONDOWN:
        #  if event.button == 1:
        #    click = True
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE:
            game()

    pygame.display.update()


def game():

  ground = Ground()
  nemo = Nemo()
  coral = Coral()

  running = False
  play_game = True
  dead = False
  high_score_value = 0
  FPS = 100

  while play_game:
      if not dead:
          screen.blit(background_image, [0, 0])
          ground.draw(screen)
          screen.blit(nemo.image, (nemo.x, nemo.y))

      pygame.display.update()

      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              pygame.quit()
              play_game = False
          elif event.type == pygame.KEYDOWN:
              if event.key == pygame.K_SPACE:
                  running = True
                  ground = Ground()
                  nemo = Nemo()
                  coral = Coral()
                  dead = False
                  running = True
                  score_value = 0


      while running:
          clock.tick(FPS) # Controlling Frames Per Second

          score = font.render("Score: " + str(int(score_value)), True, (200, 200, 200))
          score_value += 0.25
          high_score_value = max(high_score_value, score_value)
          high_score = font.render("High Score: " + str(int(high_score_value)), True, (200, 200, 200))
          screen.blit(background_image, [0, 0])

          for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    nemo.jump()

          ground.update()
          ground.draw(screen)

          nemo.update()
          nemo.draw(screen)

          coral.update()
          coral.draw(screen)

          screen.blit(score, (650, 30))
          screen.blit(high_score, (450, 30))

          if int(score_value) % 100 == 0 and int(score_value) % 3 == 0: # Increase game speed after score crosses a multiple of 300
              coral.speed += 0.25
              ground.speed += 0.25


          closest_hitbox = min(coral.hitbox0, coral.hitbox1, coral.hitbox2) # Hitbox of closest coral

          if nemo.hitbox.colliderect(closest_hitbox): # Collision detection with closest coral
              dead = True
              #screen.blit(game_over, (200, 70))
              screen.blit(replay_button, (120, 150))

          pygame.display.update()

          if dead:
              del nemo
              del ground
              del coral
              running = False

mainMenu()
