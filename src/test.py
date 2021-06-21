from md import MD
from follower import Follower

import coincurve
from web3 import Web3, HTTPProvider
from codecs import encode


print("Hello")
compiled_contract_path = "../build/contracts/BubblechainV4.json"
contract_address = '0x744a6A380b8AC2d555b765804152d8F42fF047aa';
blockchain_address = "ws://127.0.0.1:9545"


md_test = MD(blockchain_address, compiled_contract_path, contract_address)

follower_1 = Follower(blockchain_address, compiled_contract_path, contract_address)
follower_2 = Follower(blockchain_address, compiled_contract_path, contract_address)
print("Hello")
###################how to format public Key ############################
te = follower_2.send_public_key().format()
str_key = str(te)
print(te)
print(encode(str_key[2:-1].encode().decode('unicode_escape'),"raw_unicode_escape"))
test = encode(str_key[2:-1].encode().decode('unicode_escape'),"raw_unicode_escape")
pub = coincurve.PublicKey(test)
print(follower_1.ecdh_handshake(te))

print(follower_1.ecdh_handshake(pub.public_key))
#######################################################
#md_test.create_IDoT(follower_1.send_public_key().format())

#md_test.

print(follower_1.ecdh_handshake(follower_2.send_public_key().public_key))
print(follower_2.ecdh_handshake(follower_1.send_public_key().public_key))

# generates idots for the followers
id_1 = md_test.create_IDoT(follower_1.send_public_key().format(), '1000')
id_2 = md_test.create_IDoT(follower_2.send_public_key().format(), '1000')

follower_1.set_idot(id_1)
follower_2.set_idot(id_2)

# updatess the root value
#md_test.update_root()

#md adding root value to blockchain
block_num  = md_test.set_root_value_on_blockchain(10000000)
print(block_num  == md_test.get_block_number())

#Generates Proof and asigns them
follower_1.set_proof(md_test.generate_proof(follower_1.get_idot()['id']))
follower_2.set_proof(md_test.generate_proof(follower_2.get_idot()['id']))

print(Follower.verify_proof_of_inclusion(md_test.get_root_value(), follower_1.get_idot(), follower_1.get_proof_of_inclusion()))
print("<ajor key",Follower.verify_proof_of_inclusion(md_test.get_root_value(), follower_2.get_idot(), follower_2.get_proof_of_inclusion()))
#follower_1.verify_signature_idot(id_1)


#Follower setting _block_number
follower_1.set_block_number(block_num)
follower_2.set_block_number(block_num)

#Verifying on bubble-level
print("Shit is real")
print(md_test.get_root_value())
print(follower_2.get_proof_of_inclusion())
print(follower_2.get_idot())

follower_1.authenticate(follower_2.get_idot(), follower_2.get_proof_of_inclusion(), follower_2.get_block_number(), md_test)

print("Here")
############################### Global Level authentication ###########################################
md_test_2 = MD(blockchain_address, compiled_contract_path, contract_address, account_number = 2)

follower_3 = Follower(blockchain_address, compiled_contract_path, contract_address)
id_3 = md_test_2.create_IDoT(str(follower_3.send_public_key().format()), '1000')
block_num_other  = md_test_2.set_root_value_on_blockchain(10000000)
#print("Kamidna koi konjo ta warda =", block_num_other)

follower_3.set_idot(id_3)
follower_3.set_proof(md_test_2.generate_proof(follower_3.get_idot()['id']))
follower_3.set_block_number(block_num_other)

print(str(follower_2.get_idot()))
print(follower_2.get_proof_of_inclusion())
print(follower_2.get_block_number())

follower_1.authenticate(follower_3.get_idot(), follower_3.get_proof_of_inclusion(), follower_3.get_block_number(), md_test)
print("Here2")
