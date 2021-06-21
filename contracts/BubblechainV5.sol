pragma solidity >=0.4.22 <0.9.0;

contract BubblechainV5 {

  mapping(address => uint256) public rootLocations;

  event RootEvent(
    address indexed owner,
    string root,
    uint256 expDate
  );

  function getBlockNumber(address _address) public view returns (uint256) {
    uint256 blocklocation = rootLocations[_address];
    return blocklocation;
  }

  function storeRootLocation(uint256 blocklocation) public {
    // Assert that only wallets can execute this transaction.
    require( msg.sender == tx.origin );
    rootLocations[msg.sender] = blocklocation;
  }

  function emitRootValue(string memory root, uint256 timeAdded) public {
    // Assert that only wallets can execute this transaction.
    require( msg.sender == tx.origin);
    emit RootEvent(msg.sender, root, timeAdded);
  }

}
