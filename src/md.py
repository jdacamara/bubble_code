import json
import time
import asyncio
import websockets

from web3 import Web3, HTTPProvider, WebsocketProvider
from merkletools import MerkleTools
from events import fetch_events
from random import randrange

class MD:


    def __init__(self,node_ip, contract_abi_path, contract_address, account_number = 0):
        self.web3 = Web3(WebsocketProvider(node_ip))
        self.account = self.web3.eth.accounts[account_number]
        # TODO: update get_abi method
        self.contract = self.web3.eth.contract(address = Web3.toChecksumAddress(contract_address), abi = MD.get_abi(contract_abi_path))
        self.mt = MerkleTools(hash_type='sha3_256')
        self.idots = {}
        self.last_id = 0

    # TODO: General method
    def get_abi(contract_abi_path):
        with open(contract_abi_path) as file :
            contract_json = json.load(file)
            contract_abi = contract_json['abi']
            return contract_abi


    def create_IDoT(self, public_key, expiration_date):
        id = self.last_id + 1

        '''
        id = randrange(65536)
        while(id in self.idots.keys()):
            id = randrange(5000)
        '''
        idot = {
            'bubble_id': self.account,
            'id': id,
            'public_key' : public_key,
            'expDate': expiration_date
        }

        sig = self.web3.eth.sign( self.account, text = str(idot))

        idot['sig'] = sig

        self.idots[id] = idot
        self.last_id = id

        return idot

    def update_root(self):
        self.mt.reset_tree()
        ids = list(self.idots.values())
        for id in ids:
            self.mt.add_leaf(str(id), True)
        self.mt.make_tree()
        self.root_value = self.mt.get_merkle_root()

    ## TODO: Fix generate_proof
    def generate_proof(self, device_num):
        value = self.idots[device_num]
        ids = list(self.idots.values())
        #index = ids.index(value)
        try:
            index = ids.index(value)
            return self.mt.get_proof(index)
        except:
            return "Value not part of tree"

    def testing_shit(self, exp = 1000):
        self.contract.functions.emitRootValue("Test", exp)

    def set_root_value_on_blockchain(self, experation_date):
        '''
        temp = 1001
        tx_hash =self.contract.functions.emitRootValue(root,temp).transact({'from': self.account})
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        block_num = receipt['blockNumber']
        events = list(fetch_events(self.contract.events.RootLocationEvent, from_block=block_num,to_block = block_num, argument_filters={"owner":self.account}))
        print("This = ", len(events) )
        last_event = events[-1:]
        #print(last_event[0]['args']['block'] == temp)

        '''
        self.update_root()
        self.exp_date = experation_date
        root = self.get_root_value()
        tx_hash = self.contract.functions.emitRootValue(root, experation_date).transact({'from': self.account})
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        #processed = self.contract.events.RootEvent().processReceipt(receipt)
        block_num = receipt['blockNumber']
        self.block_num = block_num
        #print("Block NUmber =====", block_num)
        self.set_root_location_on_blockchain()
        return block_num


        '''
        events = list(fetch_events(self.contract.events.RootEvent, from_block=block_num,to_block = block_num, argument_filters={"owner":self.account}))
        #events = list(fetch_events(self.contract.events.RootEvent, from_block=block_num, to_block = block_num))#, argument_filters={"owner":self.account}))
        print("This = ", len(events) )
        last_event = events[-1:]


        print(last_event[0]['args']['root'])
        print(root)
        #print(receipt)
        '''

    def set_root_location_on_blockchain(self):
        block_num = self.block_num
        tx_hash = self.contract.functions.storeRootLocation(block_num).transact({'from': self.account})
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        block_number =receipt['blockNumber']
        print("This is what needed to be searched =", block_number)
        return block_number


    def get_root_value_location(self, address):
        tx_hash = self.contract.functions.getBlockNumber(address).transact({'from': self.account})
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        block_number = receipt['blockNumber']
        #print(block_number)
        return block_number

    def get_root_value(self):
        return self.root_value

    def get_block_number(self):
        return self.block_num

'''
blockchain_address = "http://127.0.0.1:9545"

web3 = Web3(HTTPProvider(blockchain_address))

compiled_contract_path = "../build/contracts/BubblechainV3.json"
contractAddress = '0x5864b991688eb3280cfe2840da0c9d74e3c9e4cf';
web3.eth.defaultAccount = web3.eth.accounts[0]

with open(compiled_contract_path) as file :
    contract_json = json.load(file)
    contract_abi = contract_json['abi']

contract = web3.eth.contract(address = Web3.toChecksumAddress(contractAddress), abi = contract_abi)



identities = {}
mt = MerkleTools(hash_type='sha3_256')


'''
'''
def createIDoT(public_key, experation_date):
    id = randrange(5000)
    while(id in identities):
        id = randrange(5000)

    idot = {
        'id': id,
        'bubble_id': web3.defaultAccount,
        'public_key' : publicKey,
        'expDate': experation_date
    }

    web3.eth.sign(idot)
    identities[id] = idot
    return idot

def updateIDoT(id, public_key, experation_date):
    idot = {
        'id': id,
        'bubble_id': web3.defaultAccount,
        'public_key' : publicKey,
        'expDate': experation_date
    }

    web3.eth.sign(idot)
    identities[id] = idot
    return idot

def update_root_value():
    mt.reset_tree()
    ids = identities.items()
    mt.add_leaf(ids, True)
    mt = make_tree()
    root_value = mt.get_merkle_root()

    tx_hash = contract.functions.emitRootValue(root_value, 10000)
    return tx_hash

def generate_proof(value):
    ids = identities.items()
    try:
        index = ids.index(value)
        return mt.get_proof(index)
    except:
        return "Value not part of tree"

def get_root_value(address, blocknumber):
    events = list(fetch_events(contract.events.RootEvent, from_block=blocknumber,to_block = blocknumber, argument_filters={"owner":account}))
    last_event = events[-1:]
    if last_event:
        result = last_event[0]['args']
        return (result['root'], result['expDate'])
    else:
        return (0,0)

def get_block_number_from_transaction(receipt):
    processed = contract.events.RootLocationEvent().processReceipt(receipt)
    return processed[0]['args']['block']

def get_root_value_location(address):
    tx_hash = contract.functions.getBlockNumber(address).transact()
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    block_number = get_block_number_from_transaction(receipt)
    return block_number


def verify_memberschip(address, value, proof, _block_number = None):
    if _block_number:
        root, exp_date = get_root_value(address, _block_number)
    else:
        block_number = get_root_value_location(address)
        if block_number:
            root, exp_date = get_root_value(address, block_number)
        else:
            return False

    if( exp_date < int(time.time())):
        return False

    target_hash = hashfunc(bytes(temp, encoding="ascii"))
    return mt.validate_proof(proof, target_hash, root)

def set_root_value():
    pass

def set_root_location():
    pass

'''
