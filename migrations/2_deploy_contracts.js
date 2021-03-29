const Bubblechain = artifacts.require('Bubblechain')
const BubblechainV2 = artifacts.require('BubblechainV2')
const MerkleProof = artifacts.require('MerkleProof')

module.exports = function (deployer) {
  deployer.deploy(Bubblechain)
  deployer.deploy(BubblechainV2)
  deployer.deploy(MerkleProof)
}
