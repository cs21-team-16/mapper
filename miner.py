import hashlib
import requests

import sys

from uuid import uuid4

from timeit import default_timer as timer

import random

import time

from decouple import config

HEADERS = {'Authorization': f"Token {config('TEST_KEY')}"}


# def proof_of_work(last_proof, difficulty):
#     """
#     Multi-Ouroboros of Work Algorithm
#     - Find a number p' such that the last six digits of hash(p) are equal
#     to the first six digits of hash(p')
#     - IE:  last_hash: ...AE9123456, new hash 123456888...
#     - p is the previous proof, and p' is the new proof
#     - Use the same method to generate SHA-256 hashes as the examples in class
#     - Note:  We are adding the hash of the last proof to a number/nonce for the new proof
#     """

#     start = timer()

#     print("Searching for next proof")
#     proof = 0
#     #  TODO: Your code here
#     proof = (random.randrange(0,10000000))

#     while valid_proof(last_proof, proof, difficulty) is False:
        
#         proof+=1

#     guess = f'{last_proof}{proof}'.encode()
#     new_hash = hashlib.sha256(f'{guess}'.encode()).hexdigest()
#     print(proof)
#     print(new_hash)
#     return proof


# def valid_proof(last_proof, proof, difficulty):
#     """
#     Validates the Proof:  Multi-ouroborus:  Do the last six characters of
#     the hash of the last proof match the first six characters of the proof?

#     IE:  last_hash: ...AE9123456, new hash 123456888...
#     """

#     # TODO: Your code here!
#     # new_hash = hashlib.sha256(f'{proof}'.encode()).hexdigest()
#     guess = f'{last_proof}{proof}'.encode()
#     new_hash = hashlib.sha256(f'{guess}'.encode()).hexdigest()

#     return new_hash[:6] == "0"*difficulty


def valid_proof(last_proof, proof, difficulty):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?  Return true if the proof is valid
    :param block_string: <string> The stringified block to use to
    check in combination with `proof`
    :param proof: <int?> The value that when combined with the
    stringified previous block results in a hash that has the
    correct number of leading zeroes.
    :return: True if the resulting hash is a valid proof, False otherwise
    """
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()

    #Change back to 6 zeroes
    return guess_hash[:difficulty] == "0"*difficulty


def proof_of_work(last_proof, difficulty):
    """
    Simple Proof of Work Algorithm
    Find a number p such that hash(last_block_string, p) contains 6 leading
    zeroes
    :return: A valid proof for the provided block
    """
    

    proof = random.randrange(0, 10000)
    while valid_proof(last_proof, proof, difficulty) is False:
        proof += 1
    print("Wow!")
    print(proof)
    return proof


if __name__ == '__main__':
    # What node are we interacting with?
    node = "https://lambda-treasure-hunt.herokuapp.com/api/bc"

    coins_mined = 0

    # Load or create ID
    # f = open("my_id.txt", "r")
    # id = f.read()
    # print("ID is", id)
    # f.close()

    if id == 'NONAME\n':
        print("ERROR: You must change your name in `my_id.txt`!")
        exit()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        #r = requests.post(url = f"{BASE_URL}/move/", headers = HEADERS, json = {"direction": i["direction"], "next_room_id": f"{i['id']}"})
        r = requests.get(url=node + "/last_proof/", headers = HEADERS)
        data = r.json()
        print(data)
        new_proof = proof_of_work(data.get('proof'), data.get('difficulty'))
        # new_proof = proof_of_work(20241298)
        time.sleep(data.get('cooldown'))

        post_data = {"proof": new_proof}

        r = requests.get(url=node + "/last_proof/", headers = HEADERS)
        data = r.json()
        print(data)
        time.sleep(data.get('cooldown'))

        r = requests.post(url=node + "/mine/", headers = HEADERS, json=post_data)
        data = r.json()
        print(data)
        time.sleep(data.get('cooldown'))
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))
