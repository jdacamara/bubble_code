import json
import time
import asyncio
import websockets

from web3 import Web3, HTTPProvider, WebsocketProvider
from merkletools import MerkleTools
from events import fetch_events
from random import randrange
from follower import Follower


print("Hello")
compiled_contract_path = "../build/contracts/BubblechainV5.json"
contract_address = '0x1db5665a5b32A9AA8863BCdCe358e4b69e72d466';
blockchain_address = "ws://127.0.0.1:9545"

with open(compiled_contract_path) as file :
    contract_json = json.load(file)
    contract_abi = contract_json['abi']


'''
web3 = Web3(WebsocketProvider(blockchain_address))
array_contract = web3.eth.contract( address='0x1db5665a5b32A9AA8863BCdCe358e4b69e72d466', abi=contract_abi )


print(array_contract.functions.getBlockNumber(address).call())
'''
follower = Follower(blockchain_address, compiled_contract_path, contract_address)
address ='0x1830A6331A90F1253bda8517D764595238e3D102'
start = time.time()
print(follower.retreive_block('0x1830A6331A90F1253bda8517D764595238e3D102'))
end = time.time()
print(end - start)
