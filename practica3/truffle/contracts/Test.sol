pragma solidity >=0.4.0 <0.7.0;

/// @title An example contract that demonstrates making a payment via the send function
contract Test {
  /// @notice Logs the address of the sender and amounts paid to the contract
  event Paid(address indexed _from, uint _value);

  /// @notice Any funds sent to this function will be unrecoverable
  /// @dev This function receives funds, there is currently no way to send funds back
  function () external payable {
    emit Paid(msg.sender, msg.value);
  }
}