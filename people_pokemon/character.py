import json
import os
import errno
from people_pokemon import featuredex


class Character():

    _featuredex = featuredex.Featuredex('./people_pokemon/featuredex.json')
    _max_level = 100
    _max_xp = 10
    _max_evasion = 6

    _skill_ranks = {
        1: 'Pathetic',
        2: 'Untrained',
        3: 'Novice',
        4: 'Adept',
        5: 'Expert',
        6: 'Master'
    }

    _base_ap = 5
    _base_power = 4
    _base_high_jump = 0
    _base_long_jump = 0
    _base_overland_speed = 3
    _base_swim_speed = 0
    _base_throw_range = 4

    _base_hp = 10
    _base_defense = 5
    _base_atk = 5
    _base_sp_def = 5
    _base_sp_atk = 5
    _base_spd = 5

    def __init__(self, name):
        self.name = name
        self.level = 1
        self.gender = ''
        self.age = 0
        self.background = ''
        self.physical_description = ''
        self.stat_points = 10
        self.xp = 0
        self.status = None
        self.exact_weight = 0
        self.exact_height = 0

        #Body Skills
        self.acrobatics = 2
        self.athletics = 2
        self.combat = 2
        self.intimidate = 2
        self.stealth = 2
        self.survival = 2

        #Mind Skills
        self.general_edu = 2
        self.medicine_edu = 2
        self.occult_edu = 2
        self.pokemon_edu = 2
        self.technology_edu = 2
        self.guile = 2
        self.perception = 2

        #Spirit Skills
        self.charm = 2
        self.command = 2
        self.focus = 2
        self.intuition = 2

        self.hp = Character._base_hp
        self.current_hp = (self.level * 2) + (self.hp * 3) + 10
        self.atk = Character._base_atk
        self.defense = Character._base_defense
        self.sp_atk = Character._base_sp_atk
        self.sp_def = Character._base_sp_atk
        self.spd = Character._base_spd
    
    def save(self, folder='./saves/', subfolder='characters/'):
        # 'vars' is a very cool builtin that serializes an object into a dictionary
        filepath = folder + subfolder + self.name + '.chr'

        #create the directories on the path in case they aren't there
        try:
            os.makedirs(os.path.dirname(filepath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                pass

        save = vars(self)
        json.dump(save, open(filepath, 'w'))
    
    @classmethod
    def load(cls, target_file):
        # read from saved dict
        ref = json.load(open(target_file))
        char = cls(ref['name'])

        return char
    
    # should be called for health calculation, NOT RAW HP
    def get_max_hitpoints(self):
        return (self.level * 2) + (self.hp * 3) + 10
    
    def get_power(self):
        power = Character._base_power
        if self.athletics >= 3:
            power += 1
        if self.combat >= 4:
            power += 1
        return power
    
    def get_high_jump(self):
        hj = Character._base_high_jump
        if self.acrobatics >= 4:
            hj += 1
        if self.acrobatics >= 6:
            hj += 1
        return hj
    
    def get_long_jump(self):
        return Character._base_long_jump + float(self.acrobatics)/2.0
    
    def get_overland_speed(self):
        return Character._base_overland_speed + float(self.acrobatics+self.athletics)/2.0
    
    def get_swim_speed(self):
        return Character._base_swim_speed + self.get_overland_speed()/2.0
    
    def get_throw_range(self):
        return Character._base_throw_range + self.athletics
    
