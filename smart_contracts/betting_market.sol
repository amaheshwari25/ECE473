pragma solidity >=0.7.0 <0.9.0;
import { SD59x18, sd, exp, ln, intoInt256} from "./SD59x18.sol";

import "./token.sol";
import "./oracle.sol";

contract PredictionMarket {

    Token token;
    Oracle public oracle;

    uint256 outcomeCount;
    SD59x18[] quantities;
    SD59x18 alpha;
    SD59x18 beta;
    string msr;

    struct Trader {
        SD59x18[] payouts;
    }

    mapping(address => Trader) internal traders;

    event Bet(address indexed trader, uint indexed index, uint shares);

    constructor(
        uint256 _outcomeCount,
        SD59x18 _alpha,
        SD59x18 _beta,
       // Oracle _oracle,
        string memory _msr,
        Token _token
    )  {
        outcomeCount = _outcomeCount;
        alpha = _alpha / sd(1e5);
        beta = _beta / sd(1e5);
      //  oracle = _oracle;
        msr = _msr;
        token = _token;

        quantities = new SD59x18[](_outcomeCount);
        for (uint256 i = 0; i < outcomeCount; i++) {
            quantities[i] = sd(100) ; // initialize to 100
        }
    }

    function get_price_vector() public view returns (int256[] memory) {
        int256[] memory prices = new int[](outcomeCount);
        for (uint256 i = 0; i < outcomeCount; i++) {
            prices[i] = get_price(i, quantities);
        }
       
        return prices;
    }

    function sum(SD59x18[] memory array) private pure returns (SD59x18) {
        SD59x18 s = sd(0);
        for(uint i = 0; i < array.length; i++) {
            s = s + array[i];
        }
        return s;
    }

    function get_price(
        uint256 i,
        SD59x18[] memory q
    ) public view returns (int256) {
        if (keccak256(abi.encodePacked(msr)) == keccak256(abi.encodePacked("LMSR"))) {
            return intoInt256(((q[i] / beta).exp()) / sum(q));
            
        } else {
            // "LS-LMSR"
            SD59x18 b = alpha * sum(q);
            SD59x18[] memory q_temp = new SD59x18[](q.length);
            for(uint j = 0; j < outcomeCount; j++) {
                q_temp[j] = (q[j] / b).exp();
            }
            SD59x18 sum_term = sum(q_temp);
            SD59x18 term1 = alpha * sum_term.ln();
            for(uint j = 0; j < outcomeCount; j++) {
                q_temp[j] = q[j] * (q[j]/b).exp();
            }
            SD59x18 term2_num = sum(q) * (q[i] / b).exp() - sum(q_temp);
            SD59x18 term2_denom = sum(q) * sum_term;

            return intoInt256(term1 + (term2_num / term2_denom));
        }
    }


    function cost_LMSR(
        SD59x18 b,
        SD59x18[] memory q
    ) internal view returns (SD59x18) {
        SD59x18 totalExp = sd(0);
        for (uint256 i = 0; i < outcomeCount; i++) {
            totalExp = totalExp + (q[i] / b).exp();
        }
        return b * totalExp.ln();
    }

    function cost(SD59x18[] memory q) public view returns (SD59x18) {
        if (keccak256(abi.encodePacked(msr)) == keccak256(abi.encodePacked("LMSR"))) {
            return cost_LMSR(beta, q);
        } else {
            // "LS-LMSR"          
            SD59x18 b = alpha * sum(q);
            return cost_LMSR(b, q);
        }
    }

    function submitBet(uint i, SD59x18 shares) public payable {
        SD59x18[] memory delta = new SD59x18[](outcomeCount);
        delta[i] = shares;

        SD59x18[] memory oldQ = quantities;
        SD59x18[] memory newQ = new SD59x18[](outcomeCount);
        for (uint j = 0; j < outcomeCount; j++) {
            newQ[j] = oldQ[j] + delta[j];
        }

        SD59x18 oldCost = cost(oldQ);
        SD59x18 newCost = cost(newQ);
        int256 costDiff = intoInt256(newCost - oldCost);

        // Transfer funds from user's wallet to contract's wallet
        require(
            token.transferFrom(msg.sender, address(this), uint(costDiff)),
            "Transfer failed"
        );

        quantities = newQ;

        // Transfer outcome tokens from contract's wallet to user's wallet
        //  require(outcomeTokens[i].transfer(msg.sender, shares), "Transfer failed");
    }

    function redeem_winnings() public payable {
        SD59x18[] memory payouts = traders[msg.sender].payouts;
        SD59x18 totalPayout = sd(0);
        for (uint256 i = 0; i < outcomeCount; i++) {
            totalPayout = totalPayout + payouts[i];
        }
        int256 payout = intoInt256(totalPayout);
        require(intoInt256(totalPayout) > 0, "No winnings to redeem");
        traders[msg.sender].payouts = new SD59x18[](outcomeCount);
        token.transferFrom(address(this), msg.sender, uint(payout));
    }
}
