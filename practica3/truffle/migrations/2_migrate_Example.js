const Example = artifacts.require("Example");
const Test = artifacts.require("Test");
const MyContract = artifacts.require("MyContract");

module.exports = function(deployer) {
 deployer.deploy(Example);
 deployer.deploy(Test);
 deployer.deploy(MyContract);
};