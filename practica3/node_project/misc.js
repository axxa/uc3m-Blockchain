const Web3 = require('web3');
const url = 'HTTP://127.0.0.1:7545';
//const MyContract = require('../truffle/build/contracts/ATM.json')
const MyContract = require('../truffle/build/contracts/MyContract.json')

const init = async() =>{
    const web3 = new Web3(url);
    const id = await web3.eth.net.getId();
    const deployedNetwork = MyContract.networks[id];
    const contract = new web3.eth.Contract(
        MyContract.abi,
        deployedNetwork.address
    );

    const addresses = await web3.eth.getAccounts();
    
    await contract.methods.sendEther().send({
        from: addresses[0],
        value: '10000000000000000000'
    })

}

npm run start:server

init();