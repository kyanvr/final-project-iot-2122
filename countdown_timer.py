import pygame

pygame.init()

screen = pygame.display.set_mode((128, 128))
countdown_clock= pygame.time.Clock()

counter, text = 5, '5'.rjust(3)
pygame.time.set_timer(pygame.USEREVENT, 1000)
font = pygame.font.SysFont("Helvetica Bold.ttf", 64)

run = True
while run:
    for e in pygame.event.get():
        if e.type == pygame.USEREVENT: 
            counter -= 1
            text = str(counter).rjust(3) if counter > 0 else 'boom!'
        if e.type == pygame.QUIT: 
            run = False

    screen.fill((255, 255, 255))
    screen.blit(font.render(text, True, (0, 0, 0)), (32, 48))
    pygame.display.flip()
    countdown_clock.tick(60)