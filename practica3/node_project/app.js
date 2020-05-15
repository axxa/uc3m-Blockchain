const express = require("express");
const bodyParser = require("body-parser");

const Web3 = require('web3');
const url = 'HTTP://127.0.0.1:7545';
const MyContract = require('../truffle/build/contracts/ATM.json')
const web3 = new Web3(url);

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false}));

/*Access to XMLHttpRequest at 'http://localhost:3000/api/ibex35volatilitypred' from origin 'http://localhost:8080' has
been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.*/
app.use((req, res, next) => {
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader(
      "Access-Control-Allow-Headers",
      "Origin, X-Requested-With, Content-Type, Accept"
    );
    res.setHeader(
      "Access-Control-Allow-Methods",
      "GET, POST, PATCH, DELETE, OPTIONS"
    );
    next();
});

const init = async() =>{
    const id = await web3.eth.net.getId();
    const deployedNetwork = MyContract.networks[id];
    contract = new web3.eth.Contract(
        MyContract.abi,
        deployedNetwork.address
    );
    return contract;

}

app.get('/getAddresses', (req, res, next) => {

    web3.eth.getAccounts().then(function(results){
        res.status(201).json({
            addresses: results
        });
    });
});

app.get('/depositFunds/:from/:wei', (req, res, next) => {

    const from = req.params.from;
    const wei = req.params.wei;
    init().then(function(result__){
        try {
            result__.methods.deposit().send({
                from: from,
                value: wei
            })
            .on('transactionHash', function(hash){
                //console.log('transactionHash');
            })
            .on('receipt', function(receipt){
                //console.log('receipt');
            })
            .on('confirmation', function(confirmationNumber, receipt){
                res.status(201).json({
                    log: "deposito exitoso"
                });
            })
            .on('error', console.error);
        } catch (ex) {
            res.status(201).json({
                error : ex.message
            });
        }
    });
    
});

app.get('/transferFunds/:from/:receiver/:wei', (req, res, next) => {

    const receiver = req.params.receiver;
    const wei = req.params.wei;
    const from = req.params.from;
    init().then(function(result__){
        try {
            result__.methods.transfer(receiver, wei).send({from: from})
            .on('transactionHash', function(hash){
                //console.log('transactionHash');
            })
            .on('receipt', function(receipt){
                //console.log('receipt');
            })
            .on('confirmation', function(confirmationNumber, receipt){
                res.status(201).json({
                    log: "transeferencia exitosa"
                });
            })
            .on('error', console.error);
        } catch (ex) {
            res.status(201).json({
                error : ex.message
            });
        }
    });
    
});

app.get('/withdrawFunds/:from/:wei', (req, res, next) => {

    const wei = req.params.wei;
    const from = req.params.from;
    init().then(function(result__){
        try {
            result__.methods.withdraw(wei).send({from: from})
            .on('transactionHash', function(hash){
                //console.log('transactionHash');
            })
            .on('receipt', function(receipt){
                //console.log('receipt');
            })
            .on('confirmation', function(confirmationNumber, receipt){
                res.status(201).json({
                    log: "retiro exitoso"
                });
            })
            .on('error', console.error);
        } catch (ex) {
            res.status(201).json({
                error : ex.message
            });
        }

    });
    
});



app.get('/getBalance/:from/', (req, res, next) => {

    const receiver = req.params.receiver;
    const wei = req.params.wei;
    const from = req.params.from;
    init().then(function(result__){
        result__.methods.balances(from).call((err, result) => {
            res.status(201).json({
                balance : result
            });
        });
    
    });
});

module.exports = app;