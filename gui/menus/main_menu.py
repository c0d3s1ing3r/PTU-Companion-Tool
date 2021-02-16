import pygame
import pygame_menu.events
from gui.menus import menu_template
from gui.menus import editor_selection_menu

class MainMenu(menu_template.MenuTemplate):
    
    def __init__(self, factory, manager):
        super().__init__(factory, manager)
        self.rebuild_menu()
    
    def rebuild_menu(self):
        # every time you build a menu, you need a clean slate
        self.menu = self._factory.build_menu('PokeDnD')
        self._add_button('Editors/Creators', self._gui_manager.new_menu, editor_selection_menu.EditorSelectionMenu(self._factory, self._gui_manager))
        #self._add_button('Options', options_menu, align=pygame_menu.locals.ALIGN_LEFT)
        self._add_button('Exit', pygame_menu.events.EXIT)