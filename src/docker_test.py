from follower import Follower

compiled_contract_path = "BubblechainV4.json"
contract_address = '0x744a6A380b8AC2d555b765804152d8F42fF047aa';
blockchain_address = "ws://172.27.80.1:9545"

print("Hello")

f = Follower(blockchain_address, compiled_contract_path, contract_address)

print (f.read_block_number_location_from_blockchain(659,"0x0FB95f4Df97307BB5D6614430ca6F03Ba83Fc184"))
ls
