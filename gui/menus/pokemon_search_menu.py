from pygame_menu import menu
from gui.menus import menu_template

from gui.menu_registry import MenuRegistry

import people_pokemon.pokedex
import people_pokemon.pokemon


class PokemonSearchMenu(menu_template.MenuTemplate):

    def __init__(self, factory, manager, save_directory = './saves/pokemon'):
        super().__init__(factory, manager)
        
        self.rebuild_menu()
    
    def rebuild_menu(self):
        self.menu = self._factory.build_menu('Choose your Pokemon!')
        self._add_text_input('Name: ', 'Pikachu', self.search_text)
        self._add_back_button()


    def search_text(self, text):
        result = people_pokemon.pokedex.Pokedex.search_by_name(text)
        result = result[0][0]
        result = people_pokemon.pokemon.Pokemon(result)
        self._gui_manager.registered_menus[MenuRegistry.PokemonDetails].change_pokemon(result)
        self._gui_manager.new_registered_menu(MenuRegistry.PokemonDetails)