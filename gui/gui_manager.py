from __future__ import annotations

from gui.menus import main_menu
from gui.menus import menu_template
from gui.menus import menu_factory
from gui.menus import pokemon_details_menu

from gui.menu_registry import MenuRegistry


import pygame_menu

class GUIManager():

    def __init__(self, display_width, display_height, theme=None, screen=None):
        # maintaining my own menu stack so things are clearer to me.
        # stack is of MENU TEMPLATE objects
        self.menu_stack: list[menu_template.MenuTemplate] = list()
        
        self.theme = theme
        if self.theme == None:
            background_path = 'images/background.png'
            menu_background = pygame_menu.baseimage.BaseImage(
                image_path=background_path,
                drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL
            )

            poke_font = 'fonts/pokemon-font.ttf'
            poke_theme = pygame_menu.themes.THEME_DARK.copy()
            poke_theme.background_color = menu_background
            #poke_theme.widget_selection_effect = pygame_menu.widgets.LeftArrowSelection
            poke_theme.widget_font = poke_font
            poke_theme.widget_font_color = (255,255,255)
            poke_theme.widget_font_size = 20
            poke_theme.widget_background_color = (32,104,96)
            poke_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_TITLE_ONLY_DIAGONAL
            poke_theme.title_font = poke_font
            poke_theme.title_font_size = 24
            self.theme = poke_theme


        self.menu_factory = menu_factory.MenuFactory(display_width, display_height, self.theme)
        self.main_menu = main_menu.MainMenu(self.menu_factory, self)
        self.menu_stack.append(self.main_menu)
        self.__register_menus()
    

    # if you want to add a registered menu, add it to this function
    def __register_menus(self):
        self.registered_menus = {}
        self.registered_menus[MenuRegistry.MainMenu] = self.main_menu
        self.registered_menus[MenuRegistry.PokemonDetails] = pokemon_details_menu.PokemonDetailsMenu(self.menu_factory, self, None)

    
    def _change_menu(self, next_menu: menu_template.MenuTemplate):
        #print('changing menu to: ' + str(next_menu))
        next_menu.rebuild_menu()
        self.main_menu.menu.get_current()._open(next_menu.menu)
    
    def back_to_main(self):
        self.main_menu.rebuild_menu()
        self.get_current().menu._open(self.main_menu.menu)
        self.menu_stack = list()
        self.menu_stack.append(self.main_menu)

    def refresh_current(self):
        self._change_menu(self.menu_stack[-1])
    
    def get_current(self) -> menu_template.MenuTemplate:
        return self.menu_stack[-1]
    
    def go_back(self):
        self.menu_stack.pop()
        self._change_menu(self.menu_stack[-1])
    
    def new_menu(self, new_menu):
        if type(new_menu) == tuple:
            new_menu = new_menu[0]
        self.menu_stack.append(new_menu)
        self._change_menu(new_menu)
    
    def new_registered_menu(self, registered: MenuRegistry):
        if type(registered) == tuple:
            registered = registered[0]
        if registered not in self.registered_menus.keys():
            raise Exception(registered + ' is not registered in registry')
        try:
            # take the menu off the stack if present
            self.menu_stack.remove(self.registered_menus[registered])
        except ValueError:
            # this specific error expected in some cases
            pass
        self.new_menu(self.registered_menus[registered])
