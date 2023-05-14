pragma solidity >=0.8.0 <0.9.0;

contract Oracle {
    uint public winning_outcome;

    constructor(uint _winning_outcome) {
        winning_outcome = _winning_outcome;
    }

    function getWinner() public view returns (uint) {
        return winning_outcome;
    }
}
