import traceback

ez_feature_format = '''
    "{key}":{{
        "name": "{name}",
        "description": "{desc}",
        "frequency": "{freq}",
        "trigger": "{trigger}",
        "tags": [
            {tags}
        ],
        "prereqs": [
            {prereqs}
        ],
        "reference": "{ref}"
    }}'''

old_file = open('features_old.json','r')
new_file = open('features.json','w')

new_file.write('{')
key = ''
#count = 0
for line in old_file:
    line = line.strip()
    #count += 1
    #if count >= 37:
    #    break

    line = line.replace('\\\\u2014', '-')
    line = line.replace('\\\\u2013', '-')
    line = line.replace('\\\\u2015', '-')
    line = line.replace('\\\\u2019', "'")
    line = line.replace('\\\\\\/', '/')
    line = line.replace('\\\\n', '\\n')
    line = line.replace('\\\\u00e9', 'e')
    line = line.replace('\\u00e9', 'e')
    line = line.replace('\\\\u0301', '')
    line = line.replace('\\\\u00bb', '>')
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
        
        index = -1
        desc = 'null'
        for i in range(len(data)):
            if 'description' in data[i]:
                index = i
                break
        if index != -1:
            desc = data[index+2].strip()
        
        index = -1
        prereqs = 'null'
        for i in range(len(data)):
            if 'Prerequisites' in data[i]:
                index = i
                break
        if index != -1:
            prereqs = data[index+4].strip().split(', ')
            prereqs = list(map(lambda x: '"' + x + '"', prereqs))
            prereqs = ', '.join(prereqs)
        
        index = -1
        tags = 'null'
        for i in range(len(data)):
            if 'Tags' in data[i]:
                index = i
                break
        if index != -1:
            tags = data[index+4].strip().split('][')
            tags = list(map(lambda x: '"[' + x.lstrip('[').rstrip(']') + ']"', tags))
            tags = ', '.join(tags)
        
        index = -1
        freq = 'null'
        for i in range(len(data)):
            if 'Frequency' in data[i]:
                index = i
                break
        if index != -1:
            freq = data[index+4].strip()
        
        index = -1
        trigger = 'null'
        for i in range(len(data)):
            if 'Frequency' in data[i]:
                index = i
                break
        if index != -1:
            trigger = data[index+4].strip()
        
        

        feature = ez_feature_format.format(
            key = key,
            name = name,
            desc = desc,
            freq = freq,
            trigger = trigger,
            tags = tags,
            prereqs = prereqs,
            ref = ref
        )
        new_file.write(feature + ',\n')
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