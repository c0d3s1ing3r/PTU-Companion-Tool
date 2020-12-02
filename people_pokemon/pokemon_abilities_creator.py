import traceback

ez_ability_format = '''
    "{key}":{{
        "name": "{name}",
        "description": "{desc}",
        "frequency": "{freq}",
        "trigger": {trigger},
        "reference": "{ref}"
    }}'''

old_file = open('pokemon_abilities_old.json','r')
new_file = open('pokemon_abilities.json','w')

new_file.write('{')
key = ''
#count = 0
for line in old_file:
    line = line.strip()
    #count += 1
    #if count >= 37:
    #    break

    line = line.replace('\\\\u2014', '-')
    line = line.replace('\\\\\\/', '/')
    line = line.replace('\\\\n', ' - ')
    line = line.replace('\\\\u00e9', 'e')
    data = line.split('\\"')

    if len(data) < 6:
        if '"' in line:
            key = line[line.index('"')+1:-3]
        continue
    #print(data)
    #index = 0
    #print()
    #for element in data:
    #    print(str(index) + ': ' + element)
    #    index += 1
    
    name = data[3].strip()
    try:
        desc = data[7].strip()
        freq = data[17].strip()
        trigger = 'null'
        if data[21].strip() == 'Trigger':
            ref = data[31].strip()
            trigger = '"' + data[25].strip() + '"'
        else:
            ref = data[23].strip()
        ability = ez_ability_format.format(
            key = key,
            name = name,
            desc = desc,
            freq = freq,
            trigger = trigger,
            ref = ref
        )
        new_file.write(ability + ',\n')
    except:
        index = 0
        for element in data:
            print(str(index) + ': ' + element)
            index += 1
        traceback.print_exc()
        print(name)
        exit()

new_file.write('}')
new_file.close()