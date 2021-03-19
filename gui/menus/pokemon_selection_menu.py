from pygame_menu.locals import ALIGN_CENTER
from pygame_menu.menu import Menu
from gui.menus import move_list_menu
from gui.menus import menu_template
from gui.menus import pokemon_details_menu

from gui.menu_registry import MenuRegistry
import people_pokemon.pokemon

import glob

class PokemonSelectionMenu(menu_template.MenuTemplate):

    def __init__(self, factory, manager, save_directory = './saves/pokemon/'):
        super().__init__(factory, manager)
        self.save_directory = save_directory
        # increase number of columns if you want to increase the amount of data presented to the user
        self.rebuild_menu()
    
    def rebuild_menu(self):
        self.columns = 3

        self.mons = list(glob.glob(self.save_directory + '*.mon'))
        self.mons = list(map(people_pokemon.pokemon.Pokemon.load, self.mons))
        # every entry in mons should now be a loaded pokemon, and it should be every pokemon in the pokemon save directory
        self.rows = len(self.mons)
        if self.rows < 1:
            self.rows = 1
        self.rows += 2 # need headers + back button

        self.menu = self._factory.build_menu('Choose your pokemon!', columns=self.columns, rows=self.rows)

        self._add_label('Pokemon')
        for mon in self.mons:
            self._add_image('./people_pokemon/pokemon_images/full_images/' + mon.id + '.png', scale=(0.25,0.25), align=ALIGN_CENTER)
        self._add_back_button()

        self._add_label('Nickname')
        for mon in self.mons:
            self._add_button(mon.nickname, self.select_mon, mon)
        self._add_vertical_margin(20)
        
        self._add_label('Level')
        for mon in self.mons:
            self._add_label(mon.level)
        
        self._add_vertical_margin(20)
        

    
    def select_mon(self, mon):
        mon = mon[0]
        self._gui_manager.registered_menus[MenuRegistry.PokemonDetails].change_pokemon(mon)
        self._gui_manager.new_registered_menu(MenuRegistry.PokemonDetails)
