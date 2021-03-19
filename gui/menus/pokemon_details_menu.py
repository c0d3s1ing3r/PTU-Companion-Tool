from gui.menu_registry import MenuRegistry
from gui.menus import move_list_menu
from gui.menus import menu_template
from gui.menus.wdigets import pokemon_type
import os

import people_pokemon.pokemon

class PokemonDetailsMenu(menu_template.MenuTemplate):

    def __init__(self, factory, manager, pokemon: people_pokemon.pokemon.Pokemon):
        super().__init__(factory, manager)
        self.columns = 2
        self.rows = 15
        if (pokemon == None):
            # default is Pikachu
            pokemon = people_pokemon.pokemon.Pokemon('025')
        self.pokemon = pokemon
        self.rebuild_menu()
    
    def change_pokemon(self, new_pokemon: people_pokemon.pokemon.Pokemon):
        self.pokemon = new_pokemon
        self.rebuild_menu()

    def rebuild_menu(self):
        self.menu = self._factory.build_menu('Pokemon Details', columns=self.columns, rows=self.rows)
        self._add_text_input('Nickname - ', self.pokemon.nickname, self.update_poke_nick)

        if os.path.exists('./people_pokemon/pokemon_images/full_images/' + self.pokemon.id + '.png'):
            self._add_image('./people_pokemon/pokemon_images/full_images/' + self.pokemon.id + '.png', scale=(0.75,0.75))
        else:
            print(self.pokemon + ' image not found')
            self._add_image('./people_pokemon/pokemon_images/full_images/000.png', scale=(0.75,0.75))
        
        if self.pokemon.ref['secondary_type'] != 'null':
            poke_type = pokemon_type.PokemonTypeWidget(self.pokemon.ref['primary_type'], self.pokemon.ref['secondary_type'], scale=(3.0,3.0))
        else:
            poke_type = pokemon_type.PokemonTypeWidget(self.pokemon.ref['primary_type'], scale=(3.0,3.0))
        
        self._add_generic_widget(poke_type)
        
        self._add_label('Level: ' + str(self.pokemon.level))
        self._add_label('Current EXP: ' + str(self.pokemon.xp))
        self._add_label('EXP to next level: ' + str(people_pokemon.pokemon.Pokemon._lvl_amts[self.pokemon.level] - self.pokemon.xp))
        self._add_label('Stat points: ' + str(self.pokemon.stat_points))
        self._add_label('Health: ' + str(self.pokemon.current_hp) + ' / ' + str(self.pokemon.get_max_hitpoints()))
        self._add_button('+ HP:       ' + str(self.pokemon.hp), self.upgrade_poke_stat, 'HP')
        self._add_button('+ ATK:      ' + str(self.pokemon.atk), self.upgrade_poke_stat, 'ATK')
        self._add_button('+ DEF:      ' + str(self.pokemon.defense), self.upgrade_poke_stat, 'DEF')
        self._add_button('+ SP. ATK:  ' + str(self.pokemon.sp_atk), self.upgrade_poke_stat, 'SP. ATK')
        self._add_button('+ SP. DEF:  ' + str(self.pokemon.sp_def), self.upgrade_poke_stat, 'SP. DEF')
        self._add_button('+ SPEED:    ' + str(self.pokemon.spd), self.upgrade_poke_stat, 'SPEED')

        self._add_button('SAVE', self.save)
        self._add_back_button()
        self._add_vertical_margin(400)
        self._add_text_input('Give EXP - ', '0', self.give_xp, maxchar=11)
        self._add_button('View Moves')

    
    def update_poke_nick(self, newnick):
        self.pokemon.nickname = newnick
        self.pokemon.save()
        self._refresh_if_current()

    def upgrade_poke_stat(self, stat):
        if self.pokemon.stat_points == 0:
            return
        self.pokemon.apply_stat_point(stat)
        self.pokemon.save()
        self._refresh_if_current()

    def save(self):
        self.pokemon.save()

    def give_xp(self, text):
        amt = int(text)
        self.pokemon.give_xp(amt)
        self.pokemon.save()
        self._refresh_if_current()

    def view_moves(self):
        self._gui_manager.registered_menus[MenuRegistry.MoveList].change_pokemon(self.pokemon)
        self._gui_manager.new_registered_menu(MenuRegistry.MoveList)