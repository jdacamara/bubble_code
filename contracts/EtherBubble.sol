pragma solidity >=0.4.22 <0.9.0;

contract EtherBubble {

  function recover_already_split(address identifier, bytes32 msgHash, uint8 v, bytes32 r,bytes32 s) pure public returns(bool){
      return identifier == ecrecover(msgHash, v, r,s);
  }

  function recover(address identifier, bytes32 hash, bytes memory signature) public pure returns (bool){
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
}
