import json
import os
import errno
import uuid
import glob
from people_pokemon import pokedex
from people_pokemon import movedex
from people_pokemon import abilitydex

class Pokemon():

    _max_moves = 6
    _max_level = 100

    _base_stat_points = 10
    _base_tutor_points = 1
    # level thresholds and all that
    # ref core p. 203
    # lvl_amts is a dictionary where the key is the current level and the value is the xp necessary to get to the next one
    _lvl_amts = {
        0: 0,
        1: 10,
        2: 20,
        3: 30,
        4: 40,
        5: 50,
        6: 60,
        7: 70,
        8: 80,
        9: 90,
        10: 110,
        11: 135,
        12: 160,
        13: 190,
        14: 220,
        15: 250,
        16: 285,
        17: 320,
        18: 360,
        19: 400,
        20: 460,
        21: 530,
        22: 600,
        23: 670,
        24: 745,  
        25: 820,  
        26: 900,  
        27: 990,
        28: 1075,
        29: 1165,
        30: 1260,
        31: 1355,
        32: 1455,
        33: 1555,
        34: 1660,
        35: 1770,
        36: 1880,
        37: 1995,
        38: 2110,
        39: 2230,
        40: 2355,
        41: 2480,
        42: 2610,
        43: 2740,
        44: 2875,
        45: 3015,
        46: 3155,
        47: 3300,
        48: 3445,
        49: 3645,
        50: 3850,
        51: 4060,
        52: 4270,
        53: 4485,
        54: 4705,
        55: 4930,
        56: 5160,
        57: 5390,
        58: 5625,
        59: 5865,
        60: 6110, 
        61: 6360,
        62: 6610, 
        63: 6865, 
        64: 7125, 
        65: 7390, 
        66: 7660, 
        67: 7925, 
        68: 8205, 
        69: 8485, 
        70: 8770, 
        71: 9060, 
        72: 9350, 
        73: 9645, 
        74: 9945, 
        75: 10250,
        76: 10560,
        77: 10870,
        78: 11185,
        79: 11505,
        80: 11910,
        81: 12320,
        82: 12735,
        83: 13155,
        84: 13580,
        85: 14010,
        86: 14445,
        87: 14885,
        88: 15330,
        89: 15780,
        90: 16235,
        91: 16695,
        92: 17160,
        93: 17630,
        94: 18105,
        95: 18585,
        96: 19070,
        97: 19560,
        98: 20055,
        99: 20555,
        100: 0
    }

    def __init__(self, reference: str):
        # there are some other traits it would be worth it for the pokemon to have, but lots of them may be static and are probably just in the pokedex
        self.id: str = reference
        self.local_id: str = ""
        ref = pokedex.Pokedex.get_by_key(reference)
        self.ref = ref
        self.name = ref['name']
        self.level: int = 1
        self.tutor_points: int = Pokemon._base_tutor_points
        self.stat_points: int = Pokemon._base_stat_points + self.level
        self.xp: int = 0
        self.status = None
        # loyalty 3 is considered average
        self.loyalty: int = 3
        self.nickname: str = self.name
        self.number = ref['number']

        self.hp = ref['combat_stats']['HP']
        self.current_hp = self.level + (self.hp * 3) + 10
        self.atk = ref['combat_stats']['Attack']
        self.defense = ref['combat_stats']['Defense']
        self.sp_atk = ref['combat_stats']['Special Attack']
        self.sp_def = ref['combat_stats']['Special Defense']
        self.spd = ref['combat_stats']['Speed']
        

        self.learned_moves = []
        self.abilities = []
        self.forgotten_moves = []
    
    
    def save(self, folder='./saves/', subfolder='pokemon/'):
        if self.local_id == "":
            self.local_id = str(uuid.uuid4())
        
        # 'vars' is a very cool builtin that serializes an object into a dictionary
        filepath = folder + subfolder + self.nickname + '-' + self.local_id + '.mon'

        for filename in glob.glob(folder + subfolder + '*.mon'):
            if self.local_id in filename:
                os.remove(filename)

        # create the directories on the path in case they aren't there
        try:
            os.makedirs(os.path.dirname(filepath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                pass

        save = vars(self)
        json.dump(save, open(filepath, 'w'))

    @classmethod
    def load(cls, target_file: str):
        # read from saved dict
        # don't need to read immutable stats (TODO: remove them to begin with, easy enough to add them back)
        ref = json.load(open(target_file))
        poke = cls(ref['id'])
        poke.nickname = ref['nickname']
        poke.level = ref['level']
        poke.tutor_points = ref['tutor_points']
        poke.stat_points = ref['stat_points']
        poke.xp = ref['xp']
        poke.learned_moves = ref['learned_moves']
        poke.abilities = ref['abilities']
        poke.loyalty = ref['loyalty']
        poke.local_id = ref['local_id']

        poke.current_hp = ref['current_hp']
        poke.hp = ref['hp']
        poke.atk = ref['atk']
        poke.defense = ref['defense']
        poke.sp_atk = ref['sp_atk']
        poke.sp_def = ref['sp_def']
        poke.spd = ref['spd']
        poke.status = ref['status']

        return poke
    
    # should really only get called by give_xp however left public so it can be called in cases where you want to "force level"
    def level_up(self):
        if self.level >= Pokemon._max_level:
            return
        self.level += 1
        self.stat_points += 1
        self.current_hp += 1
        if self.level % 5 == 0:
            self.tutor_points += 1
        
    
    def give_xp(self, amt):
        if self.level >= Pokemon._max_level:
            self.xp = 0
            return
        
        # need to handle potential multiple level ups
        self.xp += amt
        while Pokemon._lvl_amts[self.level] <= self.xp and self.level < Pokemon._max_level:
            self.xp -= Pokemon._lvl_amts[self.level]
            self.level_up()


    # TODO: make sure the pokemon is actually allowed to learn the move
    # TODO: maybe add special checks for ditto/smeargle/mew?
    def learn_move(self, move):
        if len(self.learned_moves) >= Pokemon._max_moves:
            raise Exception('Attempted to learn more than the maximum number of moves. Max is at: ' + str(Pokemon._max_moves))

        possible_move = Pokemon._movedex.search_by_name(move)
        if len(possible_move) == 0:
            raise Exception('Move ' + str(move) + ' not found in movedex')

        self.learned_moves.append(possible_move[0][1])
    
    def forget_move(self, move):
        # error if move is not present
        self.learned_moves.remove(move)
    
    # atomic option (and not as in nuclear)
    # perform the lookup before attempting to learn to prevent a situation where you could forget without learning
    def replace_move(self, old, new):
        possible_move = movedex.Movedex.search_by_name(new)
        if len(possible_move) == 0:
            raise Exception('Move ' + str(new) + ' not found in movedex')
        self.forget_move(old)
        self.learn_move(possible_move)

    def learn_ability(self, ability):
        possible_ability = abilitydex.PokemonAbilities.search_by_name(ability)
        if len(possible_ability) == 0:
            raise Exception('Ability ' + str(ability) + ' not found in ability catalog')
        
    def apply_stat_point(self, stat):
        if type(stat) == tuple:
            stat = stat[0]
        
        if stat == 'HP':
            self.hp += 1
            self.current_hp += 3
        elif stat == 'ATK':
            self.atk += 1
        elif stat == 'DEF':
            self.defense += 1
        elif stat == 'SP. ATK':
            self.sp_atk += 1
        elif stat == 'SP. DEF':
            self.sp_def += 1
        elif stat == 'SPEED':
            self.spd += 1
        else:
            raise Exception('Stat point type invalid:' + str(stat))
        self.stat_points -= 1
    
    def roll_skill(self, skill):
        if type(skill) == tuple:
            stat = skill[0]
        


    
    # should be called for health calculation, NOT RAW HP
    def get_max_hitpoints(self):
        return self.level + (self.hp * 3) + 10

    def __repr__(self):
        return self.nickname + '\n' + self.name + '\n' + self.id + '\n'
