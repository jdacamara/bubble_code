import sha3
import coincurve
import json

from web3 import Web3, HTTPProvider, WebsocketProvider
from merkletools import MerkleTools
from events import fetch_events, hashfunc
from eth_account.messages import encode_defunct


'''
blockchain_address = "http://127.0.0.1:9545"

web3 = Web3(HTTPProvider(blockchain_address))
compiled_contract_path = "../build/contracts/BubblechainV3.json"
contractAddress = '0x5864b991688eb3280cfe2840da0c9d74e3c9e4cf';
md = "127.0.0.1"
mt = MerkleTools(hash_type='sha3_256')

with open(compiled_contract_path) as file :
    contract_json = json.load(file)
    contract_abi = contract_json['abi']

contract = web3.eth.contract(address = Web3.toChecksumAddress(contractAddress), abi = contract_abi)
'''
def get_root_value(address, blocknumber):
    events = list(fetch_events(contract.events.RootEvent, from_block=blocknumber,to_block = blocknumber, argument_filters={"owner":account}))
    last_event = events[-1:]
    if last_event:
        result = last_event[0]['args']
        return (result['root'], result['expDate'])
    else:
        return (0,0)

def verify_memberschip(address, value, proof, _block_number = None):
    if _block_number:
        root, exp_date = get_root_value(address, _block_number)

    else:
        return False
        '''
        Request this from MD
        block_number = get_root_value_location(address)
        if block_number:
            root, exp_date = get_root_value(address, block_number)
        else:
            return False
        '''

    if( exp_date < int(time.time())):
        return False

    target_hash = hashfunc(bytes(temp, encoding="ascii"))
    return mt.validate_proof(proof, target_hash, root)

class Follower:

    def __init__(self, node_ip, contract_abi_path, contract_address):
        self.web3 = Web3(WebsocketProvider(node_ip))
        self.private_key = coincurve.PrivateKey()

        self.contract = self.web3.eth.contract(address = Web3.toChecksumAddress(contract_address), abi = Follower.get_abi(contract_abi_path))


    # TODO: General method
    def get_abi(contract_abi_path):
        with open(contract_abi_path) as file :
            contract_json = json.load(file)
            contract_abi = contract_json['abi']
            return contract_abi

    def ecdh_handshake(self, public_key):
        return self.private_key.ecdh(public_key)

    def set_idot(self, idot):
        self.idot = idot

    def send_public_key(self):
        return self.private_key.public_key

    def set_proof(self, proof_of_inclusion):
        self.proof_of_inclusion = proof_of_inclusion

    def set_block_number(self, block_number):
        self.block_number = block_number

    def get_idot(self):
        return self.idot

    def get_proof_of_inclusion(self):
        return self.proof_of_inclusion

    def get_block_number(self):
        return self.block_number

    def authenticate(self, idot, proof_of_inclusion, block_number, MD):
        if self.verify_signature_idot(idot):

            if (self.idot['bubble_id'] == idot['bubble_id']):
                self.bubble_level_authentication(idot, proof_of_inclusion, block_number)
            else:
                #print("Different Bubble")
                self.global_level_authentication(idot, proof_of_inclusion, block_number, MD)
        else:
            return "Malicious IDoT"

    def bubble_level_authentication(self, idot, proof_of_inclusion, block_num):
        if (self.get_block_number() == block_num):
            # TODO: Add timing constraint
            result = self.read_root_from_blockchain(block_num, idot['bubble_id'])
            if (result):
                root = result[0]
                #print("Root = ", root)
                #print("Proof = ", proof_of_inclusion)
                #print("IDOT = ", idot)
                print("Ow shit", Follower.verify_proof_of_inclusion(root, idot, proof_of_inclusion))
            else:
                return "Not root value for that Bubble ID at that block"
        else:
            return "Outdated block number"

    def global_level_authentication(self, idot,proof_of_inclusion, block_num, MD):
        result = self.read_root_from_blockchain(block_num, idot['bubble_id'])

        if(result):
            block_number_fetch_locaiton  = MD.get_root_value_location(idot['bubble_id'])
            print("Info needed", type(idot['bubble_id']))
            print("Info needed", idot['bubble_id'])
            print("Info needed", type(block_number_fetch_locaiton))
            print("Info needed", block_number_fetch_locaiton)
            block_containng_root = self.read_block_number_location_from_blockchain(block_number_fetch_locaiton, idot['bubble_id'])
            #print("Containing ===", block_containng_root)
            #print("Given block ==", block_num )
            print("Check")
            if (block_containng_root == block_num):
                root = result[0]
                print("Ow shit -Global", Follower.verify_proof_of_inclusion(root, idot, proof_of_inclusion))

            else:
                #print('Outdate IDoT')
                return 'Outdate IDoT'
        else:
            return "No root value at assigned location"


    # TODO: Move to helper functions
    def read_root_from_blockchain(self,block_num, address):
        events = list(fetch_events(self.contract.events.RootEvent, from_block=block_num,to_block = block_num, argument_filters={"owner": address}))
        try :
            #print("Len = ", len(events))
            last_event = events[-1:]
            #print(last_event)

            root = last_event[0]['args']['root']
            exp_date = last_event[0]['args']['expDate']

            return (root, exp_date)
        except :
            return None

    def read_block_number_location_from_blockchain(self, block_num, address):
        events = list(fetch_events(self.contract.events.RootLocationEvent, from_block=block_num,to_block = block_num, argument_filters={"owner": address}))
        print("Len = ", len(events))
        try:
            last_event = events[-1:]
            block_num = last_event[0]['args']['block']
            return block_num
        except:
            return None


    # TODO: Move to helper functions
    def verify_proof_of_inclusion(root, idot, proof_of_inclusion):
        mt = MerkleTools(hash_type='sha3_256')
        target_hash = hashfunc(bytes(str(idot), encoding="ascii"))
        return mt.validate_proof(proof_of_inclusion, target_hash , root)

    def verify_signature_idot(self, idot):
        sig = idot.pop('sig')

        message = encode_defunct(text=str(idot))
        bubble_id  = self.web3.eth.account.recover_message(message, signature = sig)

        idot['sig'] = sig

        if (bubble_id == idot['bubble_id']):
            return True

        return False
