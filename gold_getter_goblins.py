import json
import time
import random
import requests
from decouple import config

# TEST_URL = "http://localhost:8000/api/adv"
BASE_URL = "https://lambda-treasure-hunt.herokuapp.com/api/adv"
HEADERS = {'Authorization': f"Token {config('TEST_KEY')}"}

map = []
with open("production-rooms.txt", "r") as f:
    for line in f:
        map = json.loads(line)

print(f"first room: {map[0]}")



def look_for_shop(gold):
    queue = []
    visited = set()
    init = requests.get(url = f"{BASE_URL}/init/",  headers = HEADERS)
    init_res = json.loads(init.text)
    time.sleep(init_res["cooldown"])
    current_room = init_res['room_id']
    queue.append([map[current_room]])
    while len(queue) > 0:
        path = queue.pop()
        vertex = path[-1]
        if vertex["room_id"] not in visited:
            print(vertex["title"])
            visited.add(vertex["room_id"])
            if vertex["title"] == "Shop":
                directions = []
                for i in range(0, len(path)-1):
                    for d in path[i]["exits"]:
                        if path[i]["exits"][d] == path[i + 1]["room_id"]:
                            directions.append({"direction": d, "id": path[i + 1]["room_id"]})
                for i in directions:
                    r = requests.post(url = f"{BASE_URL}/move/", headers = HEADERS, json = {"direction": i["direction"], "next_room_id": f"{i['id']}"})
                    res = json.loads(r.text)
                    print(res)
                    time.sleep(res["cooldown"])
                break
            for i in vertex["exits"]:
                if vertex["exits"][i] is not None and vertex["exits"][i] not in visited:
                    new_path = list(path)
                    new_path.append(map[vertex["exits"][i]])
                    queue.insert(0, new_path)
    r = requests.post(url = f"{BASE_URL}/status/", headers = HEADERS)
    res = json.loads(r.text)
    gold = res['gold']
    print(res)
    time.sleep(res["cooldown"])
    if len(res["inventory"]) > 0:
        for i in range(0, len(res["inventory"])):
            # if "treasure" in res["inventory"][i]:
            if "treasure" in res["inventory"][i]:
                req = requests.post(url = f"{BASE_URL}/sell/", headers = HEADERS, json = {"name": res["inventory"][i]})
                result = json.loads(req.text)
                print(f"LOOK HERE: {result}")
                time.sleep(result["cooldown"])

                req = requests.post(url = f"{BASE_URL}/sell/", headers = HEADERS, json = {"name": res["inventory"][i], "confirm":"yes"})
                result = json.loads(req.text)
                # global gold
                # gold += #Some value here that 
                print(f"LOOK HERE: {result}")
                time.sleep(result["cooldown"])
                # This might need to be edited for confirmation of sale
    



def look_for_treasure():
    # wander around randomly forward, checking each room for treasure
    # if treasure, examine it for weight,
    # if won't be overemcombered, get treasure
    # check status after each treasure
    # if emcumbered is full, run look for shop
    opposites = {
        "n": "s",
        "s": "n",
        "e": "w",
        "w": "e"
    }
    init = requests.get(url = f"{BASE_URL}/init/",  headers = HEADERS)
    init_res = json.loads(init.text)
    time.sleep(init_res["cooldown"])
    current_room_ID = init_res['room_id']
    current_room = init_res
    
    status = requests.post(url = f"{BASE_URL}/status/", headers = HEADERS)
    status_res = json.loads(status.text)
    strength = status_res["strength"]
    encumbrance = status_res["encumbrance"]
    time.sleep(status_res["cooldown"])
    
    ready_to_sell = False
    last_move = None
    while ready_to_sell is False:
        directions = []
        for i in map[current_room_ID]["exits"]:
            if map[current_room_ID]["exits"][i] is not None:
                if last_move is None or i not in opposites[last_move]:
                    directions.append(i)
        if len(directions) == 0:
            break
        print(directions)
        choice = random.randrange(0,len(directions))
        last_move = directions[choice]
        if len(current_room["items"]) > 0:
            for i in current_room["items"]:
                if "treasure" in i:
                    item = requests.post(url = f"{BASE_URL}/examine/", headers = HEADERS, json = {"name":i})
                    item_res = json.loads(item.text)
                    print(item_res)
                    weight = item_res["weight"]
                    time.sleep(item_res["cooldown"])

                    if weight <= strength - encumbrance:
                        encumbrance += weight
                        grab = requests.post(url = f"{BASE_URL}/take/", headers = HEADERS, json = {"name": i})
                        grab_res = json.loads(grab.text)
                        time.sleep(grab_res["cooldown"])
                        if encumbrance == strength:
                            ready_to_sell = True
                            break
                    else:
                        ready_to_sell = True
        r = requests.post(url = f"{BASE_URL}/move/", headers = HEADERS, json = {"direction": last_move, "next_room_id": f"{map[current_room_ID]['exits'][last_move]}"})
        r_res = json.loads(r.text)
        print(r_res)
        current_room = r_res
        current_room_ID = r_res["room_id"]
        time.sleep(r_res["cooldown"])
                
            
                    


def change_name():
    # if gold >= 1000 stop looking for treasure, find name changer, change name
    queue = []
    visited = set()
    init = requests.get(url = f"{BASE_URL}/init/",  headers = HEADERS)
    init_res = json.loads(init.text)
    time.sleep(init_res["cooldown"])
    current_room = init_res['room_id']
    queue.append([map[current_room]])
    while len(queue) > 0:
        path = queue.pop()
        vertex = path[-1]
        if vertex["room_id"] not in visited:
            print(vertex["title"])
            visited.add(vertex["room_id"])
            if vertex["title"] == "Pirate Ry's":
                directions = []
                for i in range(0, len(path)-1):
                    for d in path[i]["exits"]:
                        if path[i]["exits"][d] == path[i + 1]["room_id"]:
                            directions.append({"direction": d, "id": path[i + 1]["room_id"]})
                for i in directions:
                    r = requests.post(url = f"{BASE_URL}/move/", headers = HEADERS, json = {"direction": i["direction"], "next_room_id": f"{i['id']}"})
                    res = json.loads(r.text)
                    print(res)
                    time.sleep(res["cooldown"])
                break
            for i in vertex["exits"]:
                if vertex["exits"][i] is not None and vertex["exits"][i] not in visited:
                    new_path = list(path)
                    new_path.append(map[vertex["exits"][i]])
                    queue.insert(0, new_path)
    r = requests.post(url = f"{BASE_URL}/status/", headers = HEADERS)
    res = json.loads(r.text)
    print(res)
    time.sleep(res["cooldown"])
    if res["gold"] >= 1000:
        req = requests.post(url = f"{BASE_URL}/change_name/", headers = HEADERS, json = {"name": f"{config('NEW_NAME')}", "confirm": "aye"})
        result = json.loads(req.text)
        print(result)
        time.sleep(res["cooldown"])
    else:
        print("We don't have enough gold.  What do?")






stats = requests.post(url = f"{BASE_URL}/status/",  headers = HEADERS)
stats_res = json.loads(stats.text)
print(stats_res)
gold = stats_res["gold"]
time.sleep(stats_res["cooldown"])
while gold < 1000:
    look_for_treasure()
    look_for_shop(gold)
change_name()
