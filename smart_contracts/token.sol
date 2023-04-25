pragma solidity >=0.7.0 <0.9.0;

contract Token {
    string public name;
    string public symbol;
    uint public totalSupply;
    uint public payout;

    mapping(address => uint) public balances;

    constructor(
        string memory _name,
        string memory _symbol,
        uint _totalSupply,
        uint _payout
    ) {
        name = _name;
        symbol = _symbol;
        totalSupply = _totalSupply;
        payout = _payout;
        balances[msg.sender] = _totalSupply;
    }

    function transfer(address _to, uint _amount) public returns (bool) {
        require(_to != address(0));
        require(balances[msg.sender] >= _amount);
        balances[msg.sender] -= _amount;
        balances[_to] += _amount;
        return true;
    }

    function transferFrom(
        address _from,
        address _to,
        uint _amount
    ) public returns (bool) {
        require(_to != address(0));
        require(balances[_from] >= _amount);
        balances[_from] -= _amount;
        balances[_to] += _amount;
        return true;
    }
}
