import pygame
from floppy.flappySnake import FlappySnake

pygame.init()

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), (int(height * scale))))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action

#create game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

#game variables
game_running = True
game_state = "main"

#define fonts
font = pygame.font.SysFont("calibri", 40)

#define colours
TEXT_COL = (255, 255, 255)

#load button images
# resume_img = pygame.image.load("button_resume.png").convert_alpha()
quit_img = pygame.image.load("button_quit.png").convert_alpha()
floppy_img = pygame.image.load('button_floppy.png').convert_alpha()
snake_img = pygame.image.load('button_snake.png').convert_alpha()

#create button instances
# resume_button = Button(304, 125, resume_img, 0.3)
quit_button = Button(600, 375, quit_img, 0.3)
floppy_button = Button(400, 375, floppy_img, 0.3)
snake_button = Button(200, 375, snake_img, 0.3)

def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

#game loop
run = True
while run:

  screen.fill((52, 78, 91))

  #check if game is paused
  if game_running == True:
    #check menu state
    if game_state == "main":
      #draw pause screen buttons
      if floppy_button.draw(screen):
        game_state = "floppy"
      if snake_button.draw(screen):
        game_running = False 
      if quit_button.draw(screen):
        run = False
  if game_state == "floppy":
    FlappySnake.start()

  #event handler
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  pygame.display.update()

pygame.quit()