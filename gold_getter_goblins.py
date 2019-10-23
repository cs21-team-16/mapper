import json

map = []
with open("test-rooms.txt", "r") as f:
    for line in f:
        map = json.loads(line)

print(f"first room: {map[0]}")

init = requests.get(url = 'http://localhost:8000/api/adv/init/',  headers = HEADERS)
# init = requests.get(url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/init/',  headers = HEADERS)
init_res = json.loads(init.text)

def look_for_shop():
    # starting where we are do a BFS to find and move to shop
    queue = []
    # set shop as "Home base"
    # if we have treasures, sell em
    pass


def look_for_treasure():
    # wander around randomly forward, checking each room for treasure
    # if treasure, get it
    # if emcumbered is full, run look for shop
    pass

def change_name():
    # if gold >= 1000 stop looking for treasure, find name changer, change name
    pass
