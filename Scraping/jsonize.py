import json

list_tablets = []

with open('Pylos.txt', 'r', encoding="utf8") as f:
    list_tablets = f.read().split('------------------------------')

list_tablets = list_tablets[:-1]

dict_tablets = {}

for tablet in list_tablets:
    tablet = tablet.split('\n')

    tablet = [line for line in tablet if line != '']
    
    tablet_id = tablet[0].split(') ', 1)[1]
    
    tablet_content = tablet[1:]

    dict_tablets[tablet_id] = tablet_content

with open('./Pylos.json', 'w') as fp:
    json.dump(dict_tablets, fp)