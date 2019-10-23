# Watch Test Server video :)

# Find SetTimeout equivalent in Python

# Use Build Week algo to traverse the Island
# How do I want to save this?
# OPTIONS:
    # Write Node class, Array of Nodes, link them up as I go, write second algo to output to file in JSON?
        # How do I prevent infinite loops'
        # I could just put the ID of each Room in the N S E W values. Wouldn't even need classes, just array of objects
        # Change "Exits" to object that holds NSEW, null for a non-exit. Retroactively fill them with IDs after passing through.
            # Will allow me to halve cooldown
        


# Init room
# {"room_id": 0, "title": "A brightly lit room", "description": "You are standing in the center of a brightly lit room. You notice a shop to the west and exits to the north, south and east.", "coordinates": "(60,60)", "elevation": 0, "terrain": "NORMAL", "players": ["player251", "player260", "player280", "player237", "player239", "player246", "player255", "player247", "player248", "player267", "player250", "player242", "player243", "player244", "player253", "player254", "player265", "player258", "player259", "player263", "player264", "player266", "player268", "player270", "player271", "player274", "player238", "player293", "player295", "player277", "player298", "player292", "player286", "player299", "player245", "player272", "player249", "player241", "player261", "player262", "player257", "player276", "player278", "player275", "player279", "player281", "player283", "player282", "player285", "player284", "player287", "player288", "player289", "player296", "player297", "player300", "player291"], "items": [], "exits": ["n", "s", "e", "w"], "cooldown": 1.0, "errors": [], "messages": []}

# I might do this in JavaScript because I can mess with arrays in a way that I can't with Python. They'll just automagically extend.
# [{...res}, {...res}] 
# [{...res}, {...res}, undefined, undefined, undefined, undefined, undefined, undefined, {...res}]

# a = [1,2,3,4]

# for i in range(len(a), 51 + 1):
#     a.append(None)

# a[51] = 51

# print(a)
from decouple import config
import requests
import json
import time
#curl -X POST -H 'Authorization: Token a2a3fd507a34c14fde889a083fed721055e903b6' -H "Content-Type: application/json" -d '{"direction":"w"}' localhost:8000/api/adv/move/
# URL = "http://localhost:8000/api/adv/move/"
# data = {"direction": "w"}

# r = requests.post(url = URL, headers={'Authorization': "Token a2a3fd507a34c14fde889a083fed721055e903b6"}, json = data)
# res = json.loads(r.text)
# print(res)
# a = res.copy()
# time.sleep(res['cooldown'])

rooms = [None]*500

URL = "http://localhost:8000/api/adv/move/"
HEADERS = {'Authorization': f"Token {config('TEST_KEY')}"}

def room_mapper():
    visited = set()

    # Keep track of:
    # Current Room
    # Previous Room
    # Current Path as a Stack <--

    opposites = {
        "n": "s",
        "s": "n",
        "e": "w",
        "w": "e"
    }

    init = requests.get(url = 'http://localhost:8000/api/adv/init/',  headers = HEADERS)
    # init = requests.get(url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/init/',  headers = HEADERS)
    init_res = json.loads(init.text)
    print(init_res['messages'])
    # time.sleep(init_res['cooldown'])

    current_room = init_res['room_id']
    previous_room = None

    init_exits = {
                'n': None,
                's': None,
                'e': None,
                'w': None,
            }
    for i in init_res['exits']:
        init_exits[i] = i
    rooms[current_room] = init_res.copy()
    rooms[current_room]['exits'] = init_exits.copy()

    # directions_stack = [{"room_id": 11, "direction": "s"}]
    directions_stack = []
    # path_stack = ['e', 'w', 'n'] -- Use opposites to reverse
    path_stack = []

    
    for i in init_res['exits']:
        directions_stack.append({'room_id': current_room, 'direction': i})

    #TODO: Foolish Explorer bug? Path Stack is wrong sometimes
    its_happened=False
    while len(directions_stack) > 0:
        went_back = False
        if its_happened:
            print("IT HAPPENED********")

        visited.add(current_room)
        previous_room = current_room
        direction = directions_stack.pop()

        # print(path_stack)
        # print(directions_stack)

        # Returns to last room with stuff in the directions stack, this will execute on dead ends
        while current_room != direction['room_id'] and len(path_stack) > 0:
            went_back = True
            # print(f"GOING BACK: {path_stack}")
            print(f"Going back... {len(path_stack)}")
            back = path_stack.pop()
            if rooms[current_room]:
                print(rooms[current_room]['exits'][opposites[back]])
                r = requests.post(url = URL, headers = HEADERS, json = {"direction": opposites[back], "next_room_id": f"{rooms[current_room]['exits'][opposites[back]]}"})
                res = json.loads(r.text)
                # time.sleep(res['cooldown'])
                print(res)
            else:
                r = requests.post(url = URL, headers = HEADERS, json = {"direction": opposites[back]})
                res = json.loads(r.text)
            print(res['messages'])
            print(res['errors'])
            print(res['cooldown'])
            current_room = res['room_id']
            previous_room = current_room
            # time.sleep(res['cooldown'])
        
        if len(path_stack) == 0 and current_room != direction['room_id']:
            print(previous_room)
            print(direction)
            print(current_room)
            with open("error.txt", "w") as f:
                f.write(f"{init_res}")
                f.write("\n")
                f.write(f"{previous_room}")
                f.write("\n")
                f.write(f"{direction}")
                f.write("\n")
                f.write(f"{current_room}")
                f.write("\n")
                f.write(f"{rooms}")
                f.write("\n")
            print("EXITING")
            exit()

        print(f"Progressing... {len(visited)}")
        path_stack.append(direction['direction'])
        r = requests.post(url = URL, headers = HEADERS, json = {"direction": direction['direction']})
        res = json.loads(r.text)

        print(f"Room ID: {res['room_id']}")
        print(res['messages'])
        print(res['errors'])
        print(res['cooldown'])

        # time.sleep(res['cooldown'])

        current_room = res['room_id']

        if res['room_id'] not in visited:
            #TODO set up exits properly before adding to rooms
            exits = {
                'n': None,
                's': None,
                'e': None,
                'w': None,
            }
            for i in res['exits']:
                exits[i] = i
            rooms[res['room_id']] = res.copy()
            rooms[res['room_id']]['exits'] = exits.copy()

            # res is new room, direction['direction'] is direction I just travelled
            for i in res['exits']:
                if opposites[i] != direction['direction']:
                    directions_stack.append({"room_id": res['room_id'], "direction": i})
        
        # print(rooms[previous_room])

        rooms[int(previous_room)]['exits'][direction['direction']] = current_room
        rooms[int(current_room)]['exits'][opposites[direction['direction']]] = previous_room

        if current_room in visited and went_back is False:
            its_happened=True
            print("In Visited, Error incoming?")
            print(f"cur: {rooms[current_room]}")
            print(f"prev: {rooms[previous_room]}")
            print("I'm going to try going back one step")
            print(f"Going back... {len(path_stack)}")
            back = path_stack.pop()
            if rooms[current_room]:
                print(rooms[current_room]['exits'][opposites[back]])
                r = requests.post(url = URL, headers = HEADERS, json = {"direction": opposites[back], "next_room_id": f"{rooms[current_room]['exits'][opposites[back]]}"})
                res = json.loads(r.text)
                print(res)
            else:
                r = requests.post(url = URL, headers = HEADERS, json = {"direction": opposites[back]})
                res = json.loads(r.text)
            print(res['messages'])
            print(res['errors'])
            print(res['cooldown'])
            current_room = res['room_id']
            previous_room = current_room
            # time.sleep(res['cooldown'])

with open("room.txt", "w") as f:
    f.write(rooms.__str__())

room_mapper()