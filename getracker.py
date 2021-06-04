import requests, json, re, signal, sys, time
from datetime import datetime

headers = {
    'User-Agent': 'learning programming/data management -@Lejo#9386'
}

def signal_handler(sig, frame):
    print(' You pressed Ctrl+C!')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)



pattern_id = re.compile(r' \d+\d*') #pattern to find id
pattern_name = re.compile(r'\w+[a-zA-Z]') # pattern to find name



with open('items2.txt', 'r') as f: #names and ids
    data_items = f.readlines()



data_ge = requests.get('https://prices.runescape.wiki/api/v1/osrs/latest') #newest prices

if data_ge.status_code != 200: #check if http response is aight
    print(data_ge.status_code)
    print('http response was bad')
    sys.exit(0)

with open('ge1hr.json', 'r') as f:
    data_ge_1hr = json.load(f)

if int(time.time()) - data_ge_1hr['timestamp'] > 3000: #suffecient time to update 1hr prices
    data_ge_1hr1 = requests.get('https://prices.runescape.wiki/api/v1/osrs/1h')
    if data_ge_1hr1.status_code == 200:
        data_ge_1hr = data_ge_1hr1
        with open('ge1hr.json', 'w') as f:
            json.dump(data_ge_1hr.json(), f)


data_ge = list(data_ge.json().values())[0] #newest prices formated as a dictionary, removes timestamp and what not
data_ge_1hr = list(data_ge_1hr.json().values())[0] #pices and volume over last hour


class Item:
    def __init__(self, item_name, item_id, high_price, low_price, margin, high_volume, low_volume, time):
        self.item_name = item_name
        self.item_id = item_id
        self.high_price = high_price
        self.low_price = low_price
        self.margin = margin
        self.high_volume = high_volume
        self.low_volume = low_volume
        self.time = time

    def ROI(self) -> float:
        return (self.margin/self.low_price)*100
    
    def __repr__(self):
        return f''' 
        item name: {self.item_name}
        item id: {self.item_id}
        item high price: {self.high_price}
        item low price: {self.low_price}
        margin: {self.margin}
        high volume {self.high_volume}
        low volume {self.low_volume}
        ROI: {self.ROI()}
        item time: {datetime.utcfromtimestamp(self.time).strftime('%Y-%m-%d %H:%M:%S')}
        '''
    
    def __str__(self):
        return f''' 
        item name: {self.item_name}
        item id: {self.item_id}
        item high price: {self.high_price}
        item low price: {self.low_price}
        margin: {self.margin}
        high volume {self.high_volume}
        low volume {self.low_volume}
        ROI: {self.ROI()}
        item time: {datetime.utcfromtimestamp(self.time).strftime('%Y-%m-%d %H:%M:%S')}
        '''



def find_id(x : list) -> str:
    return re.findall(pattern_id, x)[::-1][0]

def top20_margin(topmargins : list = []) -> list:
    """20 items with the highest margin

    Args:
        topmargins (list, optional): [description]. Defaults to [].

    Returns:
        list: [list with dictionaries with the highest margin]
    """
    for items_ids, data in data_ge.items():
        try:
            topmargins.append({
                'id' : items_ids,
                'high' : data['high'], 
                'low' : data['low'],
                'margin' : data['high'] - data['low'],
                'time' : data['highTime'],
                'High Price Volume' : data_ge_1hr[items_ids]['highPriceVolume'],
                'Low Price Volume' : data_ge_1hr[items_ids]['lowPriceVolume']
            })
        except:
            continue


    topmargins.sort(reverse = True, key = lambda x: x['margin'])
    topmargins = topmargins[:21]

    return topmargins[:21]


def top20Volume(topvolume : list = []) -> list:
    """loops through the items and sorts them based on volume returning an new shorter list
    """ 
    for item_id, data in data_ge_1hr.items():
        try:
            topvolume.append({
                'id' : item_id,
                'high' : data_ge[item_id]['high'],
                'low' : data_ge[item_id]['low'],
                'margin' : data_ge[item_id]['high'] - data_ge[item_id]['low'],
                'time' : data_ge[item_id]['highTime'],
                'High Price Volume' : data['highPriceVolume'],
                'Low Price Volume' : data['lowPriceVolume']
            })
        except:
            continue
    topvolume.sort(reverse = True, key = lambda x : (['High Price Volume']+['Low Price Volume']))
    return topvolume[:21]



def match_id(list_of_data : list) -> list:
    """cartesian product then match if ID is the same so we find the name

    Args:
        list_of_data (list, optional): The top items with the highest margin or the highest volume. Defaults to [].

    Returns:
        [type]: list of item objects
    """
    newlist = []
    for i in data_items: #find the name of item ids
        for item in list_of_data:
            if int(item['id']) == int(find_id(i)):
                item_data = Item(' '.join(re.findall(pattern_name, i)), 
                item['id'], 
                item['high'], 
                item['low'], 
                item['margin'],
                item['High Price Volume'],
                item['Low Price Volume'],
                item['time'])
                newlist.append(item_data)
    return newlist


menu = '''
-----------------
0 - show menu again
1 - high volume
2 - high margin
3 - refresh prices
4 - quit
-----------------
'''
def interactive_menu():
    print(menu)
    choice = ''
    while choice != '4':
        choice = input('pick a choice: ')
        if choice == '0':
            print(menu)
        elif choice == '1':
            print(match_id(top20Volume()))
        elif choice == '2':
            print(match_id(top20_margin()))
        elif choice == '4':
            print('thanks for coming')
        else:
            print('inlvalid input try again \n')


if __name__ == '__main__':
    interactive_menu()
