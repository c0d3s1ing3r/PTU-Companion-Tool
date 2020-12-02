import traceback

ez_move_format = '''
    "{key}":{{
        "name": "{name}",
        "type": "{typ}",
        "AC": {ac},
        "damage_base": {db},
        "class": "{ass}",
        "range": "{dist}",
        "target": "{target}",
        "frequency": "{freq}",
        "effect": "{effect}",
        "tags": [
            {tags}
        ],
        "reference": "{ref}"
    }}'''

old_file = open('pokemon_moves_old.json','r')
new_file = open('pokemon_moves.json','w')

new_file.write('{')
key = ''
#count = 0
for line in old_file:
    line = line.strip()
    #count += 1
    #if count >= 20:
    #    break

    line = line.replace('\\\\u2014', '-')
    line = line.replace('\\\\\\/', '/')
    line = line.replace('\\\\n', ' - ')
    line = line.replace('\\\\u00e9', 'e')
    line = line.replace('\\\\u2019', '\'')
    line = line.replace('\\\\u2013', '-')
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
        # this is a pain
        # use field names + offsets to determine some of these values
        # they're way too inconsistent otherwise

        ref = data[-2].strip()
        typ = data[13].strip()
        freq = data[21].strip()

        index = -1
        ac = 'null'
        for i in range(len(data)):
            if 'AC' in data[i]:
                index = i
                break
        if index != -1:
            try:
                ac = int(data[index+4])
            except:
                ac = '"'+ data[index+4] + '"'
        
        index = -1
        db = 'null'
        for i in range(len(data)):
            if 'DB' in data[i]:
                index = i
                break
        if index != -1:
            try:
                db = int(data[index+4])
            except:
                db = '"'+ data[index+4] + '"'
        
        index = -1
        effect = 'null'
        for i in range(len(data)):
            if 'Effect' in data[i]:
                index = i
                break
        if index != -1:
            effect = data[index+4].strip()
        
        index = -1
        ass = 'null'
        for i in range(len(data)):
            if 'Class' in data[i]:
                index = i
                break
        if index != -1:
            ass = data[index+4].strip()
        
        index = -1
        dist = 'null'
        target = 'null'
        tags = ''
        for i in range(len(data)):
            if 'Range' in data[i]:
                index = i
                break
        if index != -1:
            field = data[index+4]
            if field.find(',') != -1:
                dist = field[0:field.index(',')]
                field = field[field.index(',')+1:]
                if field.find(',') != -1:
                    target = field[0:field.index(',')]
                    field = field[field.index(',')+2:]
                    field = field.split(', ')
                    for tag in field:
                        tags += '"' + tag + '",'
                    tags = tags[0:-1]
                else:
                    target = field.strip()
        target = target.strip()

        ability = ez_move_format.format(
            key = key,
            name = name,
            typ = typ,
            ac = ac,
            db = db,
            ass = ass,
            tags = tags,
            ref = ref,
            dist = dist,
            target = target,
            effect = effect,
            freq = freq
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