pragma solidity >=0.4.22 <0.9.0;

contract BubblechainV3 {

  struct RootStruct{
    bytes32 root;
    uint256 expDate;
  //Add timing constraint
  }

  mapping(address => RootStruct) roots;
  mapping(address => uint256) rootLocations;
  address[] public bubbleIDs;

  event RootLocationEvent(
    address indexed owner,
    uint256 block
    );

  event RootEvent(
    address indexed owner,
    bytes32 root,
    uint256 expDate
    );

  function getBlockNumber(address _address) public {
    uint256 blocklocation = rootLocations[_address];
    emit RootLocationEvent(_address, blocklocation);
  }

  function emitRootLocation(uint256 blocklocation) public {
    //Might have to assert tx.origin is equal to msg.sender
    rootLocations[msg.sender] = blocklocation;
    emit RootLocationEvent(msg.sender, blocklocation);
  }

  function emitRootValue(bytes32 root, uint256 timeAdded) public returns(uint) {
    uint256 timeStamp = block.timestamp + 900 + timeAdded;
    roots[msg.sender] = RootStruct(root, timeStamp);
    emit RootEvent(msg.sender, root, timeStamp);
    return block.number;
  }

  function recover_already_split(address identifier, bytes32 msgHash, uint8 v, bytes32 r,bytes32 s) pure public returns(bool){
      return identifier == ecrecover(msgHash, v, r,s);
  }

  function recover(address identifier, bytes32 hash, bytes memory signature) internal pure returns (bool){
    bytes32 r;
    bytes32 s;
    uint8 v;

    // Check the signature length
    if (signature.length != 65) {
      return (false);
    }
    // Divide the signature in r, s and v variables
    // ecrecover takes the signature parameters, and the only way to get them
    // currently is to use assembly.
    // solium-disable-next-line security/no-inline-assembly
    assembly {
      r := mload(add(signature, 0x20))
      s := mload(add(signature, 0x40))
      v := byte(0, mload(add(signature, 0x60)))
    }

    // Version of signature should be 27 or 28, but 0 and 1 are also possible versions
    if (v < 27) {
      v += 27;
    }

    // If the version is correct return the signer address
    if (v != 27 && v != 28) {
      return (false);
    } else {
      // solium-disable-next-line arg-overflow
      return identifier == ecrecover(hash, v, r, s);
    }
  }

  function checkTime(uint256 expirationDate)internal view returns (bool){
    return expirationDate >= now +900;
  }

  function verifyMembership(address bubbleID, bytes32 hash, bytes memory signature, bytes32 leaf, bytes32[] memory proof) public view returns (bool){
    if (recover(bubbleID, hash, signature)){

      RootStruct memory value = roots[bubbleID];
      bytes32 root = value.root;
      if (checkTime(value.expDate)){
        bytes32 computedHash = leaf;

        for (uint256 i = 0; i < proof.length; i++) {
          bytes32 proofElement = proof[i];

          if (computedHash < proofElement) {
            // Hash(current computed hash + current element of the proof)
            computedHash = keccak256(abi.encodePacked(computedHash, proofElement));
          } else {
            // Hash(current element of the proof + current computed hash)
            computedHash = keccak256(abi.encodePacked(proofElement, computedHash));
          }
        }

        // Check if the computed hash (root) is equal to the provided root
        return computedHash == root;
      }
      return false;
    }
    return false;
  }

}
