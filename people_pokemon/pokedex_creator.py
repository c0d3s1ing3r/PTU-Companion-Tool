import traceback

ez_poke_format = '''
    "{key}":{{
        "name": "{name}", 
        "number": {number}, 
        "page_reference": "Pokedex Page:{page}", 
        "primary_type": "{type1}",
        "secondary_type": "{type2}",
        "weight": {{
            "true_weight": "{flavor_weight}",
            "weight_class": {weight}
        }},
        "height": {{
            "true_height": "{flavor_height}",
            "height_class": "{height}"
        }},
        "breeding": {{
            "male_rate": {male},
            "female_rate": {female},
            "egg_group": [
                {egg}
            ],
            "hatch_rate_in_days": {hatch}
        }},
        "capabilities": {{
            "overland": {overland},
            "swim": {swim},
            "jump_l": {jump_l},
            "jump_h": {jump_h},
            "power": {power},
            "sky": {sky},
            "burrow": {burrow},
            "levitate": {levitate},
            "teleporter": {teleporter},
            "additional_capabilities": [
                {capabilities}
            ]
        }},
        "skills": {{
            "athl": "{athl}",
            "acro": "{acro}",
            "combat": "{combat}",
            "stealth": "{stealth}",
            "percep": "{percep}",
            "focus": "{focus}"
        }},
        "combat_stats": {{
            "HP": {hp},
            "Attack": {atk},
            "Defense": {defense},
            "Special Attack": {spatk},
            "Special Defense": {spdef},
            "Speed": {spd}
        }},
        "basic_abilities": [
            {basic}
        ],
        "advanced_abilities": [
            {advanced}
        ],
        "high_abilities": [
            {high}
        ],
        "evolutions": [
            {evos}
        ],
        "diet": [
            {diets}
        ],
        "habitats": [
            {habitats}
        ],
        "learned_moves": [
            {learned_moves}
        ],
        "tm_moves": [
            {tm_moves}
        ],
        "hm_moves": [
            {hm_moves}
        ],
        "egg_moves": [
            {egg_moves}
        ],
        "tutor_moves": [
            {tutor_moves}
        ]
    }}'''

#"mega_evolution": {mega}
ez_move_format = '''
            {{
                "level_req": {level},
                "move_name": "{name}",
                "move_type": "{typ}"
            }}'''

ez_tm_format = '''
            {{
                "tm_num": {num},
                "move_name": "{name}",
                "move_type": "{typ}"
            }}'''

ez_evo_format = '''
            {{
                "level_req": {level},
                "alt_req": "{alt}",
                "pokemon": "{name}"
            }}'''

old_file = open('pokemon_old.json','r')
new_file = open('pokedex.json','w')

new_file.write('{')
key = ''
#count = 0
for line in old_file:
    line = line.strip()
    #count += 1
    #if count >= 5:
    #    break
    data = line.split('\\"')
    if len(data) < 6:
        if '"' in line:
            key = line[line.index('"')+1:-3]
        continue
    #print(data)
    #index = 0
    #for element in data:
    #    print(str(index) + ': ' + element)
    #    index += 1
    
    poke = data[5].split(' ')[1]
    number = int(data[5].split(' ')[0][1:4])
    try:
        page = data[11].split('.')[1]
        base_stats = data[23].split('\\\\n')
        hp = int(base_stats[0].split(' ')[-1])
        atk = int(base_stats[1].split(' ')[-1])
        defense = int(base_stats[2].split(' ')[-1])
        sp_atk = int(base_stats[3].split(' ')[-1])
        sp_def = int(base_stats[4].split(' ')[-1])
        speed = int(base_stats[5].split(' ')[-1])

        type_abilities = data[33].split('\\\\n')

        poke_type = type_abilities[0]
        type1 = poke_type.split('\\\\\\/')[0][len('Type: '):]
        type2 = poke_type.split('\\\\\\/')[1] if len(poke_type.split('\\\\\\/')) == 2 else 'null'

        basic_abilities = []
        adv_abilities = []
        high_abilities = []
        for ability in type_abilities[1:]:
            if 'high' in ability.lower():
                high_abilities.append(ability[14:])
            if 'adv' in ability.lower():
                adv_abilities.append(ability[15:])
            if 'basic' in ability.lower():
                basic_abilities.append(ability[17:])
        if len(basic_abilities) == 0:
            basic_abilities = ''
        else:
            basic_abilities = '"'  + '", "'.join(basic_abilities) + '"'
        
        if len(adv_abilities) == 0:
            adv_abilities = ''
        else:
            adv_abilities = '"'  + '", "'.join(adv_abilities) + '"'
        
        if len(high_abilities) == 0:
            high_abilities = ''
        else:
            high_abilities = '"'  + '", "'.join(high_abilities) + '"'
        
        evos = data[43].split('\\\\n')
        evo_elements = []
        alt = 'null'
        for evo in evos:
            if len(evo.split(' ')) > 4:
                if evo.split(' ')[-1].isnumeric():
                    level_req = int(evo.split(' ')[-1])
                else:
                    level_req = 0
                    alt = ' '.join(evo.split(' ')[3:])
            else:
                level_req = 0
            pokemon = evo.split(' ')[2]
            evo_elements.append(
                ez_evo_format.format(level = level_req, name = pokemon, alt = alt)
            )
        evos = ',\n'.join(evo_elements)

        height = ' '.join(data[53].rstrip('\\').split(' ')[1:])
        vital_stats = data[54].split('\\\\n')
        height += ' / ' + vital_stats[0].split(' ')[1].lstrip('\\/')
        height_class = vital_stats[0].split(' ')[2].strip('()')

        weight = ' '.join(vital_stats[1].split(' ')[1:3])
        weight += ' / ' + ' '.join(vital_stats[1].split(' ')[3:5]).lstrip('\\/')
        weight_class = int(vital_stats[1].split(' ')[5].strip('()'))

        #print(height)
        #print(height_class)
        #print(weight)
        #print(weight_class)

        breeding_info = data[64].split('\\\\n')
        if breeding_info[0] == 'Gender Ratio: No Gender':
            male_rate = 'null'
            female_rate = 'null'
        else:
            male_rate = float(breeding_info[0].split(' ')[2].rstrip('%'))
            female_rate = float(breeding_info[0].split(' ')[5].rstrip('%'))
        eggs = breeding_info[1][10:].split('\\\\\\/')
        eggs = list(map(lambda x: x.strip(), eggs))
        eggs = '"' + '", "'.join(eggs) + '"'
        if len(breeding_info) > 2 and breeding_info[2].split(' ')[3].isnumeric():
            hatch_rate = int(breeding_info[2].split(' ')[3])
        else:
            hatch_rate = 'null'

        living_info = data[74].split('\\\\n')
        diet = living_info[0].split(' ')[1:]
        diet = list(map(lambda x: x.rstrip(','), diet))
        diet = '"' + '", "'.join(diet) + '"'

        habitat = living_info[1].split(' ')[1:]
        habitat = list(map(lambda x: x.rstrip(','), habitat))
        habitat = '"' + '", "'.join(habitat) + '"'

        # this is fucking stupid
        capabilities = data[84].split(', ')
        overland = 'null'
        swim = 'null'
        sky = 'null'
        burrow = 'null'
        jump_l = 'null'
        jump_h = 'null'
        power = 'null'
        levitate = 'null'
        teleporter = 'null'
        for capability in capabilities:
            if 'overland' in capability.lower():
                overland = int(capability.split(' ')[1])
            if 'swim' in capability.lower():
                swim = int(capability.split(' ')[1])
            if 'sky' in capability.lower():
                sky = int(capability.split(' ')[1]) if capability.split(' ')[1].isnumeric() else 'null'
            if 'burrow' in capability.lower():
                burrow = int(capability.split(' ')[1])
            if 'jump' in capability.lower():
                jump_l = int(capability.split(' ')[1].split('\\\\\\/')[0])
                jump_h = int(capability.split(' ')[1].split('\\\\\\/')[1])
            if 'power' in capability.lower():
                power = int(capability.split(' ')[1])
            if 'levitate' in capability.lower():
                levitate = int(capability.split(' ')[1])
            if 'teleporter' in capability.lower():
                teleporter = int(capability.split(' ')[1])
        # use the last index of a digit to tell when to start the additional_capabilities offset
        index = -1
        for string in capabilities:
            if not string[-1].isdigit():
                index = capabilities.index(string)
                break
        if index == -1:
            additional_capabilities = ''
        else:
            additional_capabilities = '"' + ', '.join(capabilities[index:]) + '"'

        skills = list(map(lambda x: x.split(' ')[1], data[94].split(', ')))
        athl = skills[0]
        acro = skills[1]
        combat = skills[2]
        stealth = skills[3]
        percep = skills[4]
        focus = skills[5]

        level_up_moves = list(map(lambda x: x.strip('*_'), data[104].split('\\\\n')))
        level_up_elements = []
        for move in level_up_moves:
            if move.split(' ')[0] == 'Evo':
                level = 0
            else:
                level = int(move.split(' ')[0])
            name = ' '.join(move.split(' ')[1:move.split(' ').index('-')])
            typ = move.split(' ')[-1]
            level_up_elements.append(
                ez_move_format.format(
                    level = level,
                    name = name,
                    typ = typ
                )
            )
        level_up_elements = ','.join(level_up_elements)

        if 'No TM' in data[110]:
            tm_elements = ''
            hm_elements = ''
        elif 'any' in data[114].lower():
            hm_elements = '"ALL"'
            tm_elements = '"ALL"'
        else:
            tm_hm_moves = list(map(lambda x: x.strip('*_'), data[114].split(', ')))
            tm_elements = []
            hm_elements = []
            for move in tm_hm_moves:
                if 'A' in move.split(' ')[0]:
                    level = int(move.split(' ')[0][1:])
                    typ = 'null'
                    name = ' '.join(move.split(' ')[1:])
                    hm_elements.append(
                        ez_tm_format.format(
                            num = level,
                            name = name,
                            typ = typ
                        )
                    )
                else:
                    level = int(move.split(' ')[0])
                    name = ' '.join(move.split(' ')[1:])
                    typ = 'null'
                    tm_elements.append(
                        ez_tm_format.format(
                            num = level,
                            name = name,
                            typ = typ
                        )
                    )
            tm_elements = ','.join(tm_elements)
            hm_elements = ','.join(hm_elements)

        if data[120] == 'No Egg Moves':
            egg_elements = ''
        elif 'any' in data[124].lower():
            egg_elements = '"ALL"'
        else:
            egg_moves = list(map(lambda x: x.strip('*_'), data[124].split(', ')))
            egg_elements = []
            for move in egg_moves:
                level = 0
                name = move
                typ = 'null'
                egg_elements.append(
                    ez_move_format.format(
                        level = level,
                        name = name,
                        typ = typ
                    )
                )
            egg_elements = ','.join(egg_elements)
        
        if 'any' in data[134]:
            tutor_elements = '"ALL"'
        else:
            tutor_moves = list(map(lambda x: x.strip('*_'), data[134].split(', ')))
            tutor_elements = []
            for move in tutor_moves:
                level = 0
                name = move
                typ = 'null'
                tutor_elements.append(
                    ez_move_format.format(
                        level = level,
                        name = name,
                        typ = typ
                    )
                )
            tutor_elements = ','.join(tutor_elements)

        pokemon = ez_poke_format.format(
            key = key,
            number = number,
            name = poke,
            page = page,
            type1 = type1,
            type2 = type2,
            flavor_weight = weight,
            weight = weight_class,
            flavor_height = height,
            height = height_class,
            male = male_rate,
            female = female_rate,
            egg = eggs,
            hatch = hatch_rate,
            overland = overland,
            swim = swim,
            sky = sky,
            burrow = burrow,
            jump_l = jump_l,
            jump_h = jump_h,
            power = power,
            levitate = levitate,
            teleporter = teleporter,
            capabilities = additional_capabilities,
            athl = athl,
            acro = acro,
            combat = combat,
            stealth = stealth,
            percep = percep,
            focus = focus,
            hp = hp,
            atk = atk,
            defense = defense,
            spatk = sp_atk,
            spdef = sp_def,
            spd = speed,
            basic = basic_abilities,
            advanced = adv_abilities,
            high = high_abilities,
            evos = evos,
            diets = diet,
            habitats = habitat,
            learned_moves = level_up_elements,
            tutor_moves = tutor_elements,
            tm_moves = tm_elements,
            hm_moves = hm_elements,
            egg_moves = egg_elements
        )
        #print(pokemon)
        new_file.write(pokemon + ',\n')
    except:
        index = 0
        for element in data:
            print(str(index) + ': ' + element)
            index += 1
        traceback.print_exc()
        print(poke)
        print(number)
        exit()

new_file.write('}')
new_file.close()