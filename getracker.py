import requests, json, re, signal, sys, time
from datetime import datetime


headers = {
    'User-Agent': 'learning programming/data management -@Lejo#9386'
}

def signal_handler(sig, frame):
    print(' You pressed Ctrl+C!')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)



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


def update_data() -> list:
    data_ge = requests.get('https://prices.runescape.wiki/api/v1/osrs/latest') #newest prices
    data_ge_1hr = requests.get('https://prices.runescape.wiki/api/v1/osrs/1h') #1hr prices
    item_data = requests.get('https://prices.runescape.wiki/api/v1/osrs/mapping') #all data

    if data_ge.status_code != 200 and data_ge_1hr.status_code != 200 and item_data.status_code != 200: #check if http response is aight
        print(data_ge.status_code, data_ge_1hr.status_code, item_data.status_code)
        print('http response was bad')
        sys.exit(0)
    data_ge_1hr = data_ge_1hr.json()
    item_data = item_data.json()

     #newest prices formated as a dictionary, pices and volume over last hour, item names and info
    return list(data_ge.json().values())[0], list(data_ge_1hr.values())[0], item_data


def make_dict(data_ge : dict, data_ge_1hr : dict, data_items : dict) -> list:
    all_items = []

    for item in data_items:
        item_id = str(item['id'])
        try:
            all_items.append({
            'name' : item['name'],
            'id' : item_id,
            'high' : data_ge[item_id]['high'], 
            'low' : data_ge[item_id]['low'], 
            'margin' : data_ge[item_id]['high'] - data_ge[item_id]['low'],
            'time' : (data_ge[item_id]['highTime']+data_ge[item_id]['highTime'])/2,
            'High Price Volume' : data_ge_1hr[item_id]['highPriceVolume'],
            'Low Price Volume' : data_ge_1hr[item_id]['lowPriceVolume'],
            'highalch' : item['highalch'],
            'limit' : item['limit']
            })
        except:
            continue
    return all_items



def top20_margin(all_items : list) -> list:
    """

    Args:
        all_items (list): dict with all items

    Returns:
        list: the items with the higest margin this hour
    """
    all_items.sort(reverse = True, key = lambda x: x['margin'])
    return all_items[:21]



def top20Volume(all_items : list) -> list:
    """top 20 items this hour in terms of volume
    """ 

    all_items.sort(reverse = True, key = lambda x : (x['High Price Volume']+x['Low Price Volume']))
    return all_items[:21]



def highalchs(all_items : list, data_ge : list):
    highalcs =[i for i in all_items if (i['highalch'] - i['High Price Volume'] - 5*data_ge['561']["high"]) > 0]
    highalcs.sort(reverse = True, key = lambda x : x['limit'])
    return highalcs[:21]





def search_for_item(all_items : list, item : str) -> list:
    item = [i for i in all_items if i['name'].upper()[:len(item)-3] == item.upper()[:len(item)-3]]
    return item







def create_item(chosen_items : list) -> list:
    """
    Args:
        chosen_items (list): [the list of data]

    Returns:
        list: list of objects
    """
    pattern_name = re.compile(r'\w+[a-zA-Z]') # pattern to find name
    newlist = []
    for item in chosen_items: #find the name of item ids
        newlist.append(
        Item(
        item['name'], 
        item['id'], 
        item['high'], 
        item['low'], 
        item['margin'],
        item['High Price Volume'],
        item['Low Price Volume'],
        item['time']
        ))
    return newlist







def interactive_menu():
    data_ge, data_ge_1hr, data_items  = update_data()
    everything = make_dict(data_ge, data_ge_1hr, data_items)
    menu = '''
    -----------------
    0 - show menu again
    1 - high volume
    2 - high margin
    3 - refresh prices
    4 - high alcs
    5 - search
    6 - quit
    -----------------
    '''
    print(menu)
    
    choice = ''
    while choice != '6':
        print('pick a choice, 0 to show menu again')
        choice = input()
        if choice == '0':
            print(menu)
        elif choice == '1':
            [print(i) for i in create_item(top20Volume(everything)) if i.ROI() > 0]
        elif choice == '2':
            [print(i) for i in create_item(top20_margin(everything)) if i.ROI() > 0]
        elif choice == '3':
            data_ge, data_ge_1hr, data_items = update_data()
            everything = make_dict(data_ge, data_ge_1hr, data_items)
        elif choice == '4':
            print(highalchs(everything, data_ge))
        elif choice == '5':
            print('what item?')
            search = input()
            print(search_for_item(everything, search))
        elif choice == '6':
            print('thanks for coming')
        else:
            print('inlvalid input try again \n')


if __name__ == '__main__':
    interactive_menu()

