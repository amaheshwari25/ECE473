pragma solidity >=0.8.0 <0.9.0;
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract OutcomeToken is ERC20 {
    mapping(address => uint256) balances;
    uint256 totalSupply_;
    mapping(address => mapping(address => uint256)) internal allowed;

    address internal eventContract;

    constructor() public {
        eventContract = msg.sender;
    }

    event Issuance(address indexed owner, uint amount);
    event Revocation(address indexed owner, uint amount);

    /*
     *  Storage
     */
    address public eventContract;

    modifier isEventContract() {
        // Only event contract is allowed to proceed
        require(msg.sender == eventContract);
        _;
    }

    function issue(
        address _for,
        uint outcomeTokenCount
    ) public isEventContract {
        _mint(_for, outcomeTokenCount);
        emit Issuance(_for, outcomeTokenCount);
    }

    function revoke(
        address _for,
        uint outcomeTokenCount
    ) public isEventContract {
        _burn(_for, outcomeTokenCount);
        emit Revocation(_for, outcomeTokenCount);
    }
}
