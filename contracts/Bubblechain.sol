pragma solidity >=0.4.22 <0.9.0;

contract Bubblechain {

  struct VerificationKey{
    string verificationKey;
    uint256 expDate;
  //Add timing constraint
  }

  mapping(address => VerificationKey) keys;

  function addVerificationKey(string memory key_value, uint256 timeAdded) public {
    uint256 timeStamp = block.timestamp + 900 + timeAdded;
    //timeStamp = now +1
    keys[msg.sender] = VerificationKey(key_value, timeStamp);

  }

  function retrieveVerificationKey(address identifier) view public returns (string memory, uint256){
    VerificationKey memory v = keys[identifier];
    //return v
    if(v.expDate <= now){
      string memory a = v.verificationKey;
      uint256 b = v.expDate;
      return (a,b);
    }else{
      return ("0",0);
    }

  }

  //function retrieveVerificationKey(address a) public view returns(VerificationKey){
  //  return keys[a];
  //}



}
