pragma solidity >=0.4.0 <0.7.0;

contract MyContract {
  string public functionCalled;
  function sendEther() external payable {
	functionCalled = 'sendEther';
  }
  function() external payable {
	functionCalled = 'fallback';
  }
}