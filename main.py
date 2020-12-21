import people_pokemon.pokemon
import pygame
import pygame_menu

# dimensions should be multiple of 16
display_width = 992
display_height = 992
WINDOW_SIZE = (display_width, display_height)
background_path = 'images/background.png'
icon_path = 'images/icon.png'
FPS = 60.0
pygame.init()

pokedex = people_pokemon.pokemon.Pokemon._pokedex
loaded_character = None

icon = pygame.image.load(icon_path)
menu_background = pygame_menu.baseimage.BaseImage(
    image_path=background_path,
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL
)


poke_font = 'fonts/pokemon-font.ttf'
poke_theme = pygame_menu.themes.THEME_DARK.copy()
poke_theme.background_color = menu_background
#poke_theme.widget_selection_effect = pygame_menu.widgets.LeftArrowSelection
poke_theme.widget_font = poke_font #pygame_menu.font.FONT_MUNRO
poke_theme.widget_font_color = (255,255,255)
poke_theme.widget_font_size = 20
poke_theme.widget_background_color = (0,0,0)
poke_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_TITLE_ONLY_DIAGONAL
poke_theme.title_font = poke_font #pygame_menu.font.FONT_MUNRO
poke_theme.title_font_size = 24


pygame.display.set_icon(icon)

main_screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('PTU')


running = True

#pygame.mixer.music.load('people_pokemon\Welcome to the World of Pokemon Piano Cover - Pokemon Diamond And Pearl.mp3')
#pygame.mixer.music.play(-1)

def bgfun():
    pass

def change_menu(next_menu):
    main_menu.get_current()._open(next_menu)

# POKEMON EDITOR
loaded_pokemon = None
poke_reload = False

pokemon_details_menu = pygame_menu.Menu(
        width=display_width, height=display_height, columns=2, rows=13, theme=poke_theme, title='Pokemon Details'
)

def update_poke_nick(newnick):
    global loaded_pokemon, poke_reload
    loaded_pokemon.nickname = newnick
    poke_reload = True
    

def upgrade_poke_stat(stat):
    global loaded_pokemon, poke_reload
    if loaded_pokemon.stat_points == 0:
        return
    loaded_pokemon.apply_stat_point(stat)
    poke_reload = True

def save_poke():
    global loaded_pokemon
    loaded_pokemon.save()

def give_xp(text):
    global loaded_pokemon, poke_reload
    amt = int(text)
    loaded_pokemon.give_xp(amt)
    poke_reload = True


def reload_pokemon_details_menu(poke):
    global loaded_pokemon
    global pokemon_details_menu
    pokemon_details_menu.clear()
    if loaded_pokemon != None:
        loaded_pokemon.save()
    loaded_pokemon = poke
    
    pokemon_details_menu.add_text_input('Nickname - ', default=loaded_pokemon.nickname, onreturn=update_poke_nick, align=pygame_menu.locals.ALIGN_LEFT)
    pokemon_details_menu.add_image('./people_pokemon/pokemon_images/full_images/' + loaded_pokemon.id + '.png', scale=(0.75,0.75), align=pygame_menu.locals.ALIGN_LEFT)
    pokemon_details_menu.add_label('Level: ' + str(loaded_pokemon.level), align=pygame_menu.locals.ALIGN_LEFT)
    pokemon_details_menu.add_label('Current EXP: ' + str(loaded_pokemon.xp), align=pygame_menu.locals.ALIGN_LEFT)
    pokemon_details_menu.add_label('EXP to next level: ' + str(people_pokemon.pokemon.Pokemon._lvl_amts[loaded_pokemon.level] - loaded_pokemon.xp), align=pygame_menu.locals.ALIGN_LEFT)
    pokemon_details_menu.add_label('Stat points: ' + str(loaded_pokemon.stat_points), align=pygame_menu.locals.ALIGN_LEFT)
    pokemon_details_menu.add_label('Health: ' + str(loaded_pokemon.current_hp) + ' / ' + str(loaded_pokemon.get_max_hitpoints()), align=pygame_menu.locals.ALIGN_LEFT)
    pokemon_details_menu.add_button('+ HP:       ' + str(loaded_pokemon.hp), upgrade_poke_stat, 'HP', align=pygame_menu.locals.ALIGN_LEFT)
    pokemon_details_menu.add_button('+ ATK:      ' + str(loaded_pokemon.atk), upgrade_poke_stat, 'ATK', align=pygame_menu.locals.ALIGN_LEFT)
    pokemon_details_menu.add_button('+ DEF:      ' + str(loaded_pokemon.defense), upgrade_poke_stat, 'DEF', align=pygame_menu.locals.ALIGN_LEFT)
    pokemon_details_menu.add_button('+ SP. ATK:  ' + str(loaded_pokemon.sp_atk), upgrade_poke_stat, 'SP. ATK', align=pygame_menu.locals.ALIGN_LEFT)
    pokemon_details_menu.add_button('+ SP. DEF:  ' + str(loaded_pokemon.sp_def), upgrade_poke_stat, 'SP. DEF', align=pygame_menu.locals.ALIGN_LEFT)
    pokemon_details_menu.add_button('+ SPEED:    ' + str(loaded_pokemon.spd), upgrade_poke_stat, 'SPEED', align=pygame_menu.locals.ALIGN_LEFT)

    pokemon_details_menu.add_button('SAVE', save_poke, align=pygame_menu.locals.ALIGN_LEFT)
    pokemon_details_menu.add_vertical_margin(200)

    pokemon_details_menu.add_text_input('Give EXP - ', default='0', onreturn=give_xp, align=pygame_menu.locals.ALIGN_LEFT)
    


# apparently this is a very heavy way of doing things, but it's pretty portable and it worked so I don't mind too much
def pokemon_save_selector():
    import tkinter
    import tkinter.filedialog
    global pokemon_details_menu
    tk_root = tkinter.Tk()

    result = tkinter.filedialog.askopenfilename(
        initialdir = "./", filetypes=[("Pokemon save files", "*.mon")],
    )
    tk_root.destroy()
    if result != '':
        reload_pokemon_details_menu(people_pokemon.pokemon.Pokemon.load(result))
        change_menu(pokemon_details_menu)

def new_pokemon_selector(text):
    global pokemon_details_menu
    result = pokedex.search_by_name(text)
    result = result[0][0]
    reload_pokemon_details_menu(people_pokemon.pokemon.Pokemon(result))
    change_menu(pokemon_details_menu)

pokemon_selection_menu = pygame_menu.Menu(
    width=display_width, height=display_height, theme=poke_theme, title="Pokemon Selection"
)
poke_search_box = pokemon_selection_menu.add_text_input('Pokemon - ', default='Pikachu', onreturn=new_pokemon_selector, align=pygame_menu.locals.ALIGN_LEFT)
#pokemon_selection_menu.add_button('Search', new_pokemon_selector(poke_search_box.get_value()), align=pygame_menu.locals.ALIGN_LEFT)

pokemon_editor = pygame_menu.Menu(
    width=display_width, height=display_height, theme=poke_theme, title="Pokemon Editor"
)
pokemon_editor.add_button('Choose existing pokemon', pokemon_save_selector, align=pygame_menu.locals.ALIGN_LEFT)
pokemon_editor.add_button('Choose new pokemon', pokemon_selection_menu, align=pygame_menu.locals.ALIGN_LEFT)

# CHARACTER EDITOR
loaded_character = None
char_reload = False

character_details_menu = pygame_menu.Menu(
        width=display_width, height=display_height, theme=poke_theme, title="Character Editor"
)

def reload_character_details_menu(char):
    global loaded_character
    global character_details_menu
    character_details_menu.clear()

    if loaded_character != None:
        loaded_character.save()
    loaded_character = char

def character_save_selector():
    import tkinter
    import tkinter.filedialog
    global character_details_menu
    tk_root = tkinter.Tk()

    result = tkinter.filedialog.askopenfilename(
        initialdir = "./", filetypes=[("Character save files", "*.chr")],
    )
    tk_root.destroy()
    if result != '':
        reload_character_details_menu(people_pokemon.people.Character.load(result))
        change_menu(character_details_menu)

def create_new_character(text):
    global pokemon_details_menu
    result = pokedex.search_by_name(text)
    result = result[0][0]
    reload_pokemon_details_menu(people_pokemon.pokemon.Pokemon(result))
    change_menu(pokemon_details_menu)

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
options_menu.add_button('UnPause Music', unpause_music, align=pygame_menu.locals.ALIGN_LEFT)

# EDITOR SELECT
character_creation = pygame_menu.Menu(
    width=display_width, height=display_height, theme=poke_theme, title="Character Creator"
)
character_creation.add_button('Pokemon Editor', pokemon_editor, align=pygame_menu.locals.ALIGN_LEFT)
character_creation.add_button('Character Editor', character_editor, align=pygame_menu.locals.ALIGN_LEFT)


def close():
    global running
    running = False

# MAIN MENU
main_menu = pygame_menu.Menu(
    width=display_width, height=display_height, theme=poke_theme, title="PokeDnD"
)
main_menu.add_button('Character Creator', character_creation, align=pygame_menu.locals.ALIGN_LEFT)
main_menu.add_button('Options', options_menu, align=pygame_menu.locals.ALIGN_LEFT)
main_menu.add_button('Exit', close, align=pygame_menu.locals.ALIGN_LEFT)

def refresh_screen():
    main_screen.fill((0,0,0))

# Run until the user asks to quit
while running:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            if loaded_pokemon != None:
                loaded_pokemon.save()
            exit()

    if main_menu.is_enabled():
        main_menu.update(events)
        main_menu.draw(main_screen)
        main_menu.mainloop(main_screen, bgfun, fps_limit=FPS, disable_loop=True)

    if poke_reload:
        reload_pokemon_details_menu(loaded_pokemon)
        poke_reload = False
        change_menu(pokemon_details_menu)
    
    if char_reload:
        reload_character_details_menu(loaded_character)
        char_reload = False
        change_menu(character_details_menu)

    pygame.display.update()
    

if loaded_pokemon != None:
        loaded_pokemon.save()
pygame.quit()