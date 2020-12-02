import pygame
import pygameMenu

display_width = 1000
display_height = 1000

pygame.init()

fontdir = pygameMenu.font.FONT_8BIT
background_path = '../images/background.png'
main_screen = pygame.display.set_mode([display_width, display_height])
background = pygame.image.load(background_path).convert_alpha()
running = True