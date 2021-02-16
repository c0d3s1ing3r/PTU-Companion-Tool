from gui.menus import menu_template
from gui.menus import pokemon_editor_menu
from gui.menus import pokemon_search_menu

import people_pokemon.pokemon

import glob

class EditorSelectionMenu(menu_template.MenuTemplate):

    def __init__(self, factory, manager):
        super().__init__(factory, manager)
        
        self.rebuild_menu()
    
    def rebuild_menu(self):
        self.menu = self._factory.build_menu('What would you like to edit?')
        self._add_button('Pokemon Editor', self._gui_manager.new_menu, pokemon_editor_menu.PokemonEditorMenu(self._factory, self._gui_manager))
        self._add_button('Character Editor', self._gui_manager.new_menu, menu_template.MenuTemplate(self._factory, self._gui_manager))
        self._add_back_to_main_button()