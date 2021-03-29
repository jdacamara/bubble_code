pragma solidity >=0.4.22 <0.9.0;

contract BubblechainV2 {

  struct Root{
    string verificationKey;
  //Add timing constraint
  }

  mapping(address => Root) roots;

  function addVerificationKey(string memory root) public {
    roots[msg.sender] = Root(root);

  }

  function checkMemberschip(address identifier, string memory path) view public returns (bool){
    //return(keys[identifier].verificationKey);

  }

  function verify(bytes32 root,bytes32 leaf,bytes32[] memory proof) public pure returns (bool){
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

}
