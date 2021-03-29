pragma solidity >=0.4.22 <0.9.0;

contract Bubblechain {

  struct VerificationKey{
    string verificationKey;
  //Add timing constraint
  }

  mapping(address => VerificationKey) keys;

  function addVerificationKey(string memory key_value) public {
    keys[msg.sender] = VerificationKey(key_value);

  }

  function retrieveVerificationKey(address identifier) view public returns (string memory){
    return(keys[identifier].verificationKey);

  }

  //function retrieveVerificationKey(address a) public view returns(VerificationKey){
  //  return keys[a];
  //}



}
