import json
import time
import random

# TEST_URL = "http://localhost:8000/api/adv"
BASE_URL = "https://lambda-treasure-hunt.herokuapp.com/api/adv"
HEADERS = {'Authorization': f"Token {config('TEST_KEY')}"}

map = []
with open("test-rooms.txt", "r") as f:
    for line in f:
        map = json.loads(line)

print(f"first room: {map[0]}")



def look_for_shop(gold):
    queue = []
    visited = set()
    init = requests.get(url = f"{BASE_url}/init/",  headers = HEADERS)
    init_res = json.loads(init.text)
    time.sleep(init_res["cooldown"])
    current_room = init_res['room_id']
    queue.append([map[current_room]])
    while len(queue) > 0:
        path = queue.pop(0)
        vertex = path[-1]
        if vertex["room_id"] not in visited:
            if vertex["title"] == "Shop":
                directions = []
                for i in range(0, len(path)-1):
                    for d in path[i]["exits"]:
                        if path[i]["exits"][d] == path[i + 1]["room_id"]:
                            directions.append({"direction": d, "id": path[i + 1]["room_id"]})
                for i in directions:
                    r = requests.post(url = f"{BASE_URL}/move/", headers = HEADERS, json = {"direction": i["direction"], "next_room_id": f"{i["id"]}"})
                    res = json.loads(r.text)
                    print(res)
                    time.sleep(res["cooldown"])
                    break
            visited.add(vertex["room_id"])
            for i in vertex["exits"]:
                if vertex["exits"][i]:
                    new_path = list(path)
                    new_path.append(map[vertex["exits"][i]])
    r = requests.post(url = f"{BASE_URL}/status/", headers = HEADERS)
    res = json.loads(r.text)
    print(res)
    time.sleep(res["cooldown"])
    if len(res["inventory"]) > 0:
        for i in res["inventory"]:
            # if "treasure" in res["inventory"][i]:
            if "treasure" in i:
                req = requests.post(url = f"{BASE_URL}/sell/", headers = HEADERS, json = {"name": res["inventory"][i]})
                result = json.loads(req.text)
                print(result)
                time.sleep(res["cooldown"])

                req = requests.post(url = f"{BASE_URL}/sell/", headers = HEADERS, json = {"name": res["inventory"][i], "confirm":"yes"})
                result = json.loads(req.text)
                # global gold
                # gold += #Some value here that 
                print(result)
                time.sleep(res["cooldown"])
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
    init = requests.get(url = f"{BASE_url}/init/",  headers = HEADERS)
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
            if i is not opposites[last_move]:
                directions.append(i)
        if len(directions) == 0:
            break
        choice = random.randrange(0,len(directions))
        last_move = directions[choice]
        if len(current_room["items"]) > 0:
            for i in current_room["items"]:
                if "treasure" in i:
                    item = requests.post(url = f"{BASE_URL}/examine/", headers = HEADERS, json = {"name":i})
                    item_res = json.loads(item.text)
                    weight = item_res["weight or size or something"]
                    time.sleep(item_res["cooldown"])

                    if weight <= strength - encumbrance:
                        encumbrance += weight
                        requests.post(url = f"{BASE_URL}/take/", headers = HEADERS, json = {"name": i})
                        if encumbrance = strength:
                            ready_to_sell = True
                            break
                    else:
                        ready_to_sell = True
        r = requests.post(url = f"{BASE_URL}/move/", headers = HEADERS, json = {"direction": last_move})
        r_res = json.loads(r.text)
        time.sleep(r_res["cooldown"])
                
            
                    


def change_name():
    # if gold >= 1000 stop looking for treasure, find name changer, change name
    queue = []
    visited = set()
    init = requests.get(url = f"{BASE_url}/init/",  headers = HEADERS)
    init_res = json.loads(init.text)
    time.sleep(init_res["cooldown"])
    current_room = init_res['room_id']
    queue.append([map[current_room]])
    while len(queue) > 0:
        path = queue.pop(0)
        vertex = path[-1]
        if vertex["room_id"] not in visited:
            if vertex["title"] == "Pirate Ry's":
                directions = []
                for i in range(0, len(path)-1):
                    for d in path[i]["exits"]:
                        if path[i]["exits"][d] == path[i + 1]["room_id"]:
                            directions.append({"direction": d, "id": path[i + 1]["room_id"]})
                for i in directions:
                    r = requests.post(url = f"{BASE_URL}/move/", headers = HEADERS, json = {"direction": i["direction"], "next_room_id": f"{i["id"]}"})
                    res = json.loads(r.text)
                    print(res)
                    time.sleep(res["cooldown"])
                    break
            visited.add(vertex["room_id"])
            for i in vertex["exits"]:
                if vertex["exits"][i]:
                    new_path = list(path)
                    new_path.append(map[vertex["exits"][i]])
    r = requests.post(url = f"{BASE_URL}/status/", headers = HEADERS)
    res = json.loads(r.text)
    print(res)
    time.sleep(res["cooldown"])
    if res["gold"] >= 1000:
        req = requests.post(url = f"{BASE_URL}/change_name/", headers = HEADERS, json = {"name": f"{config('NEW_NAME')}"]})
        result = json.loads(req.text)
        print(result)
        time.sleep(res["cooldown"])
    else:
        print("We don't have enough gold.  What do?")






stats = requests.get(url = f"{BASE_url}/status/",  headers = HEADERS)
stats_res = json.loads(stats.text)
gold = stats_res["gold"]
time.sleep(stats_res["cooldown"])
while gold < 0:
    look_for_treasure()
    look_for_shop(gold)
change_name()
