pragma solidity >=0.4.22 <0.9.0;

contract BubblechainV4 {

  mapping(address => uint256) rootLocations;

  event RootLocationEvent(
    address indexed owner,
    uint256 block
  );

  event RootEvent(
    address indexed owner,
    string root,
    uint256 expDate
  );

  function getBlockNumber(address _address) public {
    uint256 blocklocation = rootLocations[_address];
    emit RootLocationEvent(_address, blocklocation);
  }

  function storeRootLocation(uint256 blocklocation) public {
    // Assert that only wallets can execute this transaction.
    require( msg.sender == tx.origin );
    rootLocations[msg.sender] = blocklocation;
  }

  function emitRootValue(string memory root, uint256 timeAdded) public returns(uint) {
    // Assert that only wallets can execute this transaction.
    require( msg.sender == tx.origin);
    emit RootEvent(msg.sender, root, timeAdded);
  }

}
