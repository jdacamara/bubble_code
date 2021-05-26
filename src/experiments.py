from web3 import Web3, HTTPProvider
import json
#import matplotlib.pyplot as plt
from merkletools import MerkleTools
from random import randrange, choice
from eth_account.messages import encode_defunct




blockchain_address = "http://127.0.0.1:8545"

web3 = Web3(HTTPProvider(blockchain_address))

compiled_contract_path = "../build/contracts/BubblechainV4.json"
contractAddress = '0x58B9E9c230CE0dc92cF7eaEAbFc5e9868314A7D1';

with open(compiled_contract_path) as file :
    contract_json = json.load(file)
    contract_abi = contract_json['abi']

contract = web3.eth.contract(address = Web3.toChecksumAddress(contractAddress), abi = contract_abi)
root_value_transactions = {}
root_location_transactions = {}
get_root_location_transactions = {}

acc1 = web3.eth.accounts[0]


#########################SIGN message
temp = {'1': 'testing'}
print(str(temp))
sig = web3.eth.sign(acc1, text = 'Testing')

message = encode_defunct(text='Testing')
acc2 = web3.eth.account.recover_message(message, signature = sig)
print(acc1)
print(acc2 ==acc1)
print(sig)

##############################################
######################## Alternative verification of message ###############################
'''
>>> from web3.auto import w3
>>> from eth_account.messages import defunct_hash_message
>>> message_hash = defunct_hash_message(text='Testing')
>>> signer = w3.eth.account.recoverHash(message_hash, signature=signature)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'signature' is not defined
>>> signature = b')\xbc7\x13\xdb\xe0z^\xc6uP\xb2V*)\x86)*%\xbe\x19L4\x87\x99`\x98\xd2&\xaf\xb6gm\xe4\x82+\xad\xa8\x14\xcbf\x86\xd5\x95\x17,d\x0e_\xbc*h\x12B\xa8\xf8JUQ\x0c(T\x04\xf0\x01'
>>> signer = w3.eth.account.recoverHash(message_hash, signature=signature)
>>> signer
'0xAf47FB531be196288BdE1E0Acf1a53F3F9FC1cf3'
'''
###################################################################################################


########## Add random root value
'''
def random_root_value():
    mt = MerkleTools(hash_type='sha3_256')
    value = randrange(0,100000)
    mt.add_leaf(str(value), True)
    mt.make_tree()
    return mt.get_merkle_root(), value

def add_random_root_value(address):
    root, value = random_root_value()
    tx_hash = contract.functions.emitRootValue(root, value).transact({'from': address})
    root_value_transactions[address] = tx_hash
    rec = web3.eth.wait_for_transaction_receipt(tx_hash)
    print("Gas used = ", rec.gasUsed)

########### Retrieve block location from mapping

def add_root_location(address):
    try:
        tx_hash = root_value_transactions[address]
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        block_number = receipt['blockNumber']
        tx_h =contract.functions.emitRootLocation(block_number).transact({'from': address})
        root_location_transactions[address] = tx_h
        rec = web3.eth.wait_for_transaction_receipt(tx_h)
        #print("Gas used", web3.eth.estimate_gas(tx_h))
        print("Gas used = ", rec.gasUsed)
    except KeyError:
        print("Value isn't added")

###################### Retrieve location

def retrieve_location(from_address, searched_address):
    tx_hash  = contract.functions.getBlockNumber(searched_address).transact({'from': from_address})
    get_root_location_transactions[from_address] = tx_hash
    rec = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(rec.gasUsed)


########################## Create plots

def create_plots(values):
    pass




################################

print(len(web3.eth.accounts))

for account in web3.eth.accounts:
    add_random_root_value(account)

print("Done with the old one")
for account in web3.eth.accounts:
    add_root_location(account)

print("Done with the old one")
for account in web3.eth.accounts:
    # TODO: change method
    retrieve_location(account, choice(web3.eth.accounts))
    #add_root_location(account)

'''
'''
acc = web3.eth.accounts[0]
contract.functions.emitRootLocation(10).transact({'from': acc})
tx_hash = contract.functions.getBlockNumber(acc).transact({'from': acc})
receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
prossed = contract.events.RootLocationEvent().processReceipt(receipt)
print(prossed)

contract.functions.emitRootLocation(9).transact({'from': acc})
tx_hash = contract.functions.getBlockNumber(acc).transact({'from': acc})
receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
prossed = contract.events.RootLocationEvent().processReceipt(receipt)
print(prossed)
'''


#receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
#print(receipt.gasUsed)
