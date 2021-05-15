pragma solidity >=0.4.22 <0.9.0;

contract BubblechainV4 {

  mapping(address => uint256) rootLocations;

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
    require( msg.sender == tx.origin );
    rootLocations[msg.sender] = blocklocation;
    emit RootLocationEvent(msg.sender, blocklocation);
  }

  function emitRootValue(bytes32 root, uint256 timeAdded) public returns(uint) {
    require( msg.sender == tx.origin);
    uint256 timeStamp = block.timestamp + 900 + timeAdded;
    //roots[msg.sender] = RootStruct(root, timeStamp);
    emit RootEvent(msg.sender, root, timeStamp);
    return block.number;
  }

}
