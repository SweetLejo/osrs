import re, requests, json, time
from datetime import datetime

pattern_id = re.compile(r' \d{1,9}') #pattern to find id
pattern_name = re.compile(r'\w+[a-zA-Z]') # pattern to find name

x = '["Ancient page 1"] = 12621,'
print(re.findall(pattern_id, x))


def find_id(x : list) -> str:
    no_comma = len(re.findall(pattern_id, x)[0])-1
    return re.findall(pattern_id, x)[0][1:no_comma]

z = find_id(x)

print(z)



# data_ge_1hr = requests.get('https://prices.runescape.wiki/api/v1/osrs/1h')


# with open('ge1hr.json', 'w') as f:
#     json.dump(data_ge_1hr.json(), f)




print(datetime.now())


print(int(time.time()))


data_ge_1hr = requests.get('https://prices.runescape.wiki/api/v1/osrs/1h')
with open('ge1hr.json', 'w') as f:
    json.dump(data_ge_1hr.json(), f)