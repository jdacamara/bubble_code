import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time

from web3 import Web3, HTTPProvider, WebsocketProvider
from merkletools import MerkleTools
from random import randrange, choice
from eth_account.messages import encode_defunct
from boxplot import sns_boxplot, create_box_plot_multiple, create_box_plot

#Initilisation of the connection
blockchain_address = "ws://127.0.0.1:9545"

web3 = Web3(WebsocketProvider(blockchain_address))

compiled_contract_path = "../build/contracts/BubblechainV5.json"
contractAddress = '0xa6CE0eB67024C3A6872feDb06d171Ef90C7A2F77';

#Parse ABI for interaction with the contract
with open(compiled_contract_path) as file :
    contract_json = json.load(file)
    contract_abi = contract_json['abi']

contract = web3.eth.contract(address = Web3.toChecksumAddress(contractAddress), abi = contract_abi)




########## Create a random root value and executes emitRootValue ##################################

def random_root_value():
    mt = MerkleTools(hash_type='sha3_256')
    value = randrange(0,100000)
    mt.add_leaf(str(value), True)
    mt.make_tree()
    return mt.get_merkle_root(), int(time.time() +50000)


def add_random_root_value(address):
    root, value = random_root_value()
    tx_hash = contract.functions.emitRootValue(root, value).transact({'from': address})
    root_value_transactions[address] = tx_hash
    rec = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(rec.gasUsed)
    return rec.gasUsed
    #root_value_transaction_gas.append( rec.gasUsed)
    #print("Gas used = ", rec.gasUsed)


########### Executes the storeRootLocation function from the smart contract #########################

def add_root_location(address):
    try:
        tx_hash = root_value_transactions[address]
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        block_number = receipt['blockNumber']
        tx_h =contract.functions.storeRootLocation(block_number).transact({'from': address})
        root_location_transactions[address] = tx_h
        rec = web3.eth.wait_for_transaction_receipt(tx_h)
        print(rec.gasUsed)
        return rec.gasUsed
        #print("Gas used", web3.eth.estimate_gas(tx_h))
        #print("Gas used = ", rec.gasUsed)
    except KeyError:
        print("Value isn't added")

###################### Executes the getBlockNumber from the smart contract ############################

def retrieve_location(from_address, searched_address):
    tx_hash  = contract.functions.getBlockNumber(searched_address).transact({'from': from_address})
    get_root_location_transactions[from_address] = tx_hash
    rec = web3.eth.wait_for_transaction_receipt(tx_hash)
    return rec.gasUsed

#######################################################################################################

#stores the transactions of the interactions
root_value_transactions = {}
root_location_transactions = {}
get_root_location_transactions = {}

#Store the number of gas emitted from each interaction
newly_added_root = []
newly_added_to_mapping = []
update_mapping = []
searched = []

print("Number of accounts = ", len(web3.eth.accounts))

#Generates random root value for each address
print("New emitted root value")
for account in web3.eth.accounts:
    newly_added_root.append(add_random_root_value(account))

print("First value in the mapping")
#Adds new block location to the mapping on the contract
for account in web3.eth.accounts:
    newly_added_to_mapping.append(add_root_location(account))
print("Refilling the values")
#Generates new random root values
for account in web3.eth.accounts:
    add_random_root_value(account)
print("Update value")
#Maintains the gas uses for updating the block number within the mapping
for account in web3.eth.accounts:
    update_mapping.append(add_root_location(account))

#Retrieves the gas for searching for the
for account in web3.eth.accounts:
    searched.append(retrieve_location(account, choice(web3.eth.accounts)))

t = time.time()
x_1 = ["Emit Root\nValue"]
sns_boxplot(newly_added_root, x_1, "images/"+ str(int(t))+ "emitRootValue")
print(len(newly_added_root))

x_2 = ["New Root\nLocation","Update Root\nLocation"]
mapping = [newly_added_to_mapping, update_mapping]
sns_boxplot(mapping, x_2, "images/" + str(int(t)) +"mapping")
print(len(newly_added_to_mapping))
print(len(update_mapping))

x_3 = ["Retrieve \nBlockNumber"]
sns_boxplot(searched, x_3, "images/" + str(int(t)) +"searched")
print(len(searched))

x = ["Emit Root\nValue", "New Root\nLocation","Update Root\nLocation", "Retrieve \nBlockNumber"]
df = [newly_added_root, newly_added_to_mapping, update_mapping, searched]
sns_boxplot(df, x,  "images/" + str(int(t)) +"All")
