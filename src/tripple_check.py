from md import MD
from follower import Follower

import coincurve
import time
from web3 import Web3, HTTPProvider
from codecs import encode


print("Hello")
compiled_contract_path = "../build/contracts/BubblechainV5.json"
contract_address = '0xa6CE0eB67024C3A6872feDb06d171Ef90C7A2F77';
blockchain_address = "ws://127.0.0.1:9545"


md_test = MD(blockchain_address, compiled_contract_path, contract_address)

follower_1 = Follower(blockchain_address, compiled_contract_path, contract_address)
follower_2 = Follower(blockchain_address, compiled_contract_path, contract_address)
follower_3 = Follower(blockchain_address, compiled_contract_path, contract_address)

follower_1.set_MD(md_test)


id_1 = md_test.create_IDoT(follower_1.send_public_key().format(), str(time.time() +50000))
id_2 = md_test.create_IDoT(follower_2.send_public_key().format(), str(time.time() +50000))
id_3 = md_test.create_IDoT(follower_3.send_public_key().format(), str(time.time() +50000))


block_num  = md_test.set_root_value_on_blockchain(int(time.time())+5000)


follower_1.set_complete_identity(id_1, block_num , md_test.generate_proof(id_1['id']))
follower_2.set_complete_identity(id_2, block_num , md_test.generate_proof(id_2['id']))
follower_3.set_complete_identity(id_3, block_num , md_test.generate_proof(id_3['id']))



#print(follower_1.request(follower_3.get_block_number(), follower_3.get_idot(), follower_3.get_proof_of_inclusion()))
'''
follower_1.set_MD(md_test)

md_test_2 = MD(blockchain_address, compiled_contract_path, contract_address, account_number =3)

follower_3 = Follower(blockchain_address, compiled_contract_path, contract_address)
id_3 = md_test_2.create_IDoT(follower_3.send_public_key().format(), str(time.time() +50000))
block_num  = md_test_2.set_root_value_on_blockchain(int(time.time())+5000)

follower_3.set_complete_identity(id_3, block_num ,md_test_2.generate_proof(id_3['id']))

print(Follower.verify_proof_of_inclusion(follower_3.root, follower_3.get_idot(), follower_3.get_proof_of_inclusion()))
#print(follower_3.get_proof_of_inclusion())
print(follower_1.request(follower_3.get_block_number(), follower_3.get_idot(), follower_3.get_proof_of_inclusion()))
'''

md_nobo = MD(blockchain_address, compiled_contract_path, contract_address, account_number =9)

follower_4 = Follower(blockchain_address, compiled_contract_path, contract_address)
follower_5 = Follower(blockchain_address, compiled_contract_path, contract_address)

id_4 = md_nobo.create_IDoT(follower_4.send_public_key().format(), str(time.time() +50000))
id_5 = md_nobo.create_IDoT(follower_5.send_public_key().format(), str(time.time() +50000))

block_num_nobo  = md_nobo.set_root_value_on_blockchain(int(time.time())+5000)

follower_4.set_complete_identity(id_4, block_num_nobo ,md_nobo.generate_proof(id_4['id']))
follower_5.set_complete_identity(id_5, block_num_nobo ,md_nobo.generate_proof(id_5['id']))

#print(Follower.verify_proof_of_inclusion(follower_5.root, follower_5.get_idot(), follower_5.get_proof_of_inclusion()))
print( follower_5.get_block_number())
print(follower_1.request(follower_5.get_idot(), follower_5.get_proof_of_inclusion()))
