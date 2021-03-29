var Bubblechain = artifacts.require("./Bubblechain.sol");

contract("Bubblechain", function(accounts){

  before(async() =>{
    accounts.forEach((item) => {
      console.log(item)

    });


  })


  it("Addition of verification key", async  function(){
    return Bubblechain.deployed().then( async function(instance){
      bubble_db = instance;
      //console.log(accounts[0]);
      bubble_db.addVerificationKey("Testing addition", {from: accounts[1]});
      //console.log(bubble_db.retrieveVerificationKey(accounts[0]).toString());
      let result = await bubble_db.retrieveVerificationKey(accounts[1]);
      console.log(result);


    }).then(function(){

      console.log('insert uses approx');
    });
  });

  it("Value is still there", async  function(){
    return Bubblechain.deployed().then( async function(instance){
      bubble_db = instance;
      //console.log(accounts[0]);
      //console.log(bubble_db.retrieveVerificationKey(accounts[0]).toString());
      let result = await bubble_db.retrieveVerificationKey(accounts[0]);
      console.log(result);


    }).then(function(){

      console.log('insert uses approx');
    });
  });

  it("Update value", async  function(){
    return Bubblechain.deployed().then( async function(instance){
      bubble_db = instance;
      //console.log(accounts[0]);
      bubble_db.addVerificationKey("Testing addition2");
      //console.log(bubble_db.retrieveVerificationKey(accounts[0]).toString());
      let result = await bubble_db.retrieveVerificationKey(accounts[2]);
      console.log(result);


    }).then(function(){

      console.log('insert uses approx');
    });
  });


});
