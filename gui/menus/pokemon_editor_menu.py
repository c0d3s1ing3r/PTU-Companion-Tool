from gui.menus import menu_template
from gui.menus import pokemon_selection_menu
from gui.menus import pokemon_search_menu

import people_pokemon.pokemon

import glob

class PokemonEditorMenu(menu_template.MenuTemplate):

    def __init__(self, factory, manager):
        super().__init__(factory, manager)
        
        self.rebuild_menu()
    
    def rebuild_menu(self):
        self.menu = self._factory.build_menu('Choose your pokemon!')
        self._add_button('Choose existing pokemon', self._gui_manager.new_menu, pokemon_selection_menu.PokemonSelectionMenu(self._factory, self._gui_manager))
        self._add_button('Choose new pokemon', self._gui_manager.new_menu, pokemon_search_menu.PokemonSearchMenu(self._factory, self._gui_manager))
        self._add_back_button()
