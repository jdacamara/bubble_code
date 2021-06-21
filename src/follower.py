import sha3
import coincurve
import json
import time

from web3 import Web3, HTTPProvider, WebsocketProvider
from merkletools import MerkleTools
from events import fetch_events, hashfunc
from eth_account.messages import encode_defunct
from codecs import encode
from hexbytes import HexBytes


class Follower:

    def __init__(self, node_ip, contract_abi_path, contract_address):
        self.web3 = Web3(WebsocketProvider(node_ip))
        self.private_key = coincurve.PrivateKey()
        self.contract = self.web3.eth.contract(address = Web3.toChecksumAddress(contract_address), abi = Follower.get_abi(contract_abi_path))

    def retreive_block(self, addres):
        try:
            return self.contract.functions.getBlockNumber(addres).call()
        except Exception as e:
            return 0

    def request(self, idot, proof_of_inclusion ):
        if (self.idot['bubble_id'] == idot['bubble_id']):
            root = self.root
            exp_date = self.exp_date
            #own_block_number = self.get_block_number()
            isValid = self.authentication(root, exp_date, idot, proof_of_inclusion)
            return True, isValid
        else:
            block_number_fetch_location  = self.retreive_block(idot['bubble_id'])
            isValid = self.global_level(block_number_fetch_location, idot, proof_of_inclusion)
            return False, isValid

    def authentication(self, root, exp_date, idot, proof):
        if (time.time() < float(exp_date)):
            if (self.verify_idot(idot)):
                return Follower.verify_proof_of_inclusion(root, idot, proof)
        return False

    def global_level(self, block_containing_root, idot, proof_of_inclusion):

        result = self.read_root_from_blockchain(block_containing_root, idot['bubble_id'])

        if( result ):
            root_value = result[0]
            exp_date = result[1]

            return self.authentication(root_value, exp_date, idot, proof_of_inclusion)

        return False

    def verify_idot(self, idot):
        now = time.time()
        if(now < float(idot['expDate'])):
            sig = idot.pop('sig')

            message = encode_defunct(text=str(idot))
            st = sig.hex()
            si = HexBytes(st)

            bubble_id  = self.web3.eth.account.recover_message(message, signature = si)

            idot['sig'] = sig

            if (bubble_id == idot['bubble_id']):
                return True
        return False




    # TODO: Move to helper functions
    def verify_proof_of_inclusion(root, idot, proof_of_inclusion):
        mt = MerkleTools(hash_type='sha3_256')
        target_hash = hashfunc(bytes(str(idot), encoding="ascii"))
        return mt.validate_proof(proof_of_inclusion, target_hash , root)

    def verify_signature_idot(self, idot):
        sig = idot.pop('sig')

        message = encode_defunct(text=str(idot))
        st = sig.hex()
        si = HexBytes(st)

        bubble_id  = self.web3.eth.account.recover_message(message, signature = si)

        idot['sig'] = sig

        if (bubble_id == idot['bubble_id']):
            return True

        return False

    # Read from the blockchain
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
        #print("Len = ", len(events))
        try:
            last_event = events[-1:]
            block_num = last_event[0]['args']['block']
            return block_num
        except:
            return None

    # Establish connection
    def ecdh_handshake(self, public_key):
        return self.private_key.ecdh(public_key)

    def send_public_key(self):
        return self.private_key.public_key
        #return str(key)

    # Setters
    def set_complete_identity(self, id, block_number, proof_of_inclusion):
        #print(id['bubble_id'])
        self.set_block_number(block_number)
        self.set_proof(proof_of_inclusion)
        self.set_idot(id)

        result = self.read_root_from_blockchain(block_number, id['bubble_id'])
        if (result):
            #print(result[0])
            #print("SHould be printed 5 times")
            self.set_root(result[0])
            self.set_exp_date(result[1])


    def set_proof(self, proof_of_inclusion):
        self.proof_of_inclusion = proof_of_inclusion

    def set_block_number(self, block_number):
        self.block_number = block_number

    def set_root(self, root):
        self.root = root

    def set_exp_date(self, date):
        self.exp_date = date

    def set_idot(self, idot):
            self.idot = idot

    def set_MD(self, MD):
        self.md = MD

    #Getters
    def get_abi(contract_abi_path):
        with open(contract_abi_path) as file :
            contract_json = json.load(file)
            contract_abi = contract_json['abi']
            return contract_abi

    def get_idot(self):
        return self.idot

    def get_proof_of_inclusion(self):
        return self.proof_of_inclusion

    def get_block_number(self):
        return self.block_number
