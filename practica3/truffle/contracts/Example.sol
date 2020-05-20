pragma solidity >=0.4.0 <0.7.0;
contract Example {
	 uint storedData;
	 function set(uint x) public {
		storedData = x;
	 }
	 function get() public view returns (uint) {
		return storedData;
	 }
}