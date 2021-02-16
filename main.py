from gui.menus import main_menu
import people_pokemon.pokemon
import pygame
import pygame.display
import pygame.image
import pygame_menu

import gui.gui_manager

# dimensions should be multiple of 16
display_width = 992
display_height = 992
WINDOW_SIZE = (display_width, display_height)
FPS = 60.0
pygame.init()


icon_path = './images/icon.png'
icon = pygame.image.load(icon_path)


pygame.display.set_icon(icon)

main_screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('PTU')


gui_manager = gui.gui_manager.GUIManager(display_width, display_height)
main_menu = gui_manager.main_menu.menu


running = True

#pygame.mixer.music.load('sound\music\Welcome\Welcome to the World of Pokemon - Pokemon DiamondPearlPlatinum OST.mp3')
#pygame.mixer.music.play(-1)

def bgfun():
    pass

'''
character_details_menu = pygame_menu.Menu(
        width=display_width, height=display_height, theme=poke_theme, title="Character Editor"
)

new_character_menu = pygame_menu.Menu(
    width=display_width, height=display_height, theme=poke_theme, title="Character Editor"
)
new_character_menu.add_text_input('Name: ', default='Pikachu', onreturn=new_pokemon_selector, align=pygame_menu.locals.ALIGN_LEFT)

character_editor = pygame_menu.Menu(
    width=display_width, height=display_height, theme=poke_theme, title="Character Editor"
)
character_editor.add_button('Choose existing character', character_save_selector, align=pygame_menu.locals.ALIGN_LEFT)
character_editor.add_button('Create new character', new_character_menu, align=pygame_menu.locals.ALIGN_LEFT)

# OPTIONS MENU
def pause_music():
    pygame.mixer.music.pause()

def unpause_music():
    pygame.mixer.music.unpause()

options_menu = pygame_menu.Menu(
    width=display_width, height=display_height, theme=poke_theme, title="Options"
)
options_menu.add_button('Pause Music', pause_music, align=pygame_menu.locals.ALIGN_LEFT)
options_menu.add_button('UnPause Music', unpause_music, align=pygame_menu.locals.ALIGN_LEFT)'''


# Run until the user asks to quit
while running:

    events = pygame.event.get()
    

    if main_menu.is_enabled():
        main_menu.update(events)
        main_menu.draw(main_screen)
        main_menu.mainloop(main_screen, bgfun, fps_limit=FPS, disable_loop=True)

    pygame.display.update()
    
pygame.quit()