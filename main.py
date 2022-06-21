import pygame
import pygame_menu
from snake.main import snakeGame

pygame.init()

screen = pygame.display.set_mode((600, 400))

def start_the_game():
    snakeGame.start()

menu = pygame_menu.Menu('Welcome', 400, 300,
                       theme=pygame_menu.themes.THEME_BLUE)

menu.add.text_input('Name :', default='John Doe')
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(screen)
