import sha3
import coincurve

from web3 import Web3, HTTPProvider
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
        self.web3 = Web3(HTTPProvider(node_ip))
        self.private_key = coincurve.PrivateKey()
        #self.mt = MerkleTools(hash_type='sha3_256')

    def get_abi(abi_path):
        with open(compiled_contract_path) as file :
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

    def get_idot(self):
        return self.idot

    def get_proof_of_inclusion(self):
        return self.proof_of_inclusion

    def verify(self, idot, proof_of_inclusion, block_number):
        pass

    #TODO: move to helper
    def verify_proof_of_inclusion(root, idot, proof_of_inclusion):
        mt = MerkleTools(hash_type='sha3_256')
        target_hash = hashfunc(bytes(str(idot), encoding="ascii"))
        return mt.validate_proof(proof_of_inclusion, target_hash , root)

    def verify_signature_idot(self, idot):
        sig = idot.pop('sig')

        message = encode_defunct(text=str(idot))
        bubble_id  = self.web3.eth.account.recover_message(message, signature = sig)
        if (bubble_id == idot['bubble_id']):
            return True

        return False
