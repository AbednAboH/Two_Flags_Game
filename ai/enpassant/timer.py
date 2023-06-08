import pygame
import pygame_menu
from settings import*
class Timer():
    def __init__(self, time, pos):
        self.initial_time = time
        self.time = time
        self.pos = pos
        self.font = pygame.font.Font(pygame_menu.font.FONT_OPEN_SANS_BOLD, 18)

    def tick(self, dt):
        self.time -= dt

    def reset(self):
        self.time = self.initial_time

    def draw(self,screen):
        mins, secs = divmod(self.time, 60)
        ms = divmod(self.time, 1000)[1]
        if self.time <= 10:
            s = f'{ms:.01f}'
        else:
            s = f'{int(mins):02}:{int(secs):02}'
        txt = self.font.render(s, True, SMALL_TEXT_COLOR)
        if self.pos == "top":
            pygame.draw.rect(screen, "black", pygame.Rect(8 * b_size, 1 * b_size,b_size-10, b_size-36))
            screen.blit(txt,  pygame.Rect(8 * b_size, 1 * b_size, b_size, b_size))
        elif self.pos=="bot":
            pygame.draw.rect(screen, "black", pygame.Rect(8 * b_size, 7 * b_size, b_size-10, b_size-36))
            screen.blit(txt, pygame.Rect(8 * b_size, 7 * b_size, b_size, b_size))
        else:
            pygame.draw.rect(screen, "black", pygame.Rect(8 * b_size, 4 * b_size, b_size - 10, b_size - 36))
            screen.blit(txt, pygame.Rect(8 * b_size, 4 * b_size, b_size, b_size))
