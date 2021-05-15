const Bubblechain = artifacts.require('Bubblechain')
const BubblechainV2 = artifacts.require('BubblechainV2')
const MerkleProof = artifacts.require('MerkleProof')
const BubblechainV3 = artifacts.require('BubblechainV3')
const BubblechainV4 = artifacts.require('BubblechainV4')

module.exports = function (deployer) {
  /*deployer.deploy(Bubblechain)
  deployer.deploy(BubblechainV2)
  deployer.deploy(MerkleProof)
  deployer.deploy(BubblechainV3)*/
  deployer.deploy(BubblechainV4)
}
