pragma solidity >=0.4.22 <0.9.0;

contract BubblechainV2 {

  struct Root{
    bytes32 root;
  //Add timing constraint
  }

  mapping(address => Root) roots;

  function addVerificationKey(bytes32 root) public {
    roots[msg.sender] = Root(root);

  }

  function verifyMembership(address bubbleID,bytes32 leaf,bytes32[] memory proof) public view returns (bool){
    Root memory value = roots[bubbleID];
    bytes32 root = value.root;
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
