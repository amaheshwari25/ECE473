pragma solidity >=0.7.0 <0.9.0;
import "./SD59x18.sol";

import "./token.sol";
import "./oracle.sol";

contract PredictionMarket {
    uint256 outcomeCount;
    SD59x18[] quantities;
    SD59x18 alpha;
    SD59x18 beta;
    string msr;
    uint256 winning_index;

    struct Trader {
        SD59x18[] payouts;
    }

    mapping(address => Trader) internal traders;

    constructor(
        uint256 _outcomeCount,
        int256 _alpha,
        int256 _beta,
        string memory _msr
    ) {
        outcomeCount = _outcomeCount;
        alpha = sd(0.03e18);
        beta = sd(150.27e18);
        //  oracle = _oracle;
        msr = _msr;
        winning_index = 0;
        quantities = new SD59x18[](_outcomeCount);
        for (uint256 i = 0; i < outcomeCount; i++) {
            quantities[i] = sd(100e18); // initialize to 100
        }
    }

    function get_beta() public view returns (int256) {
        return intoInt256(beta);
    }

    function fund() public payable {}

    function get_price_vector() public view returns (int256[] memory) {
        int256[] memory prices = new int[](outcomeCount);
        for (uint256 i = 0; i < outcomeCount; i++) {
            prices[i] = get_price(i);
        }

        return prices;
    }

    function get_shares() public view returns (int256[] memory) {
        require(
            traders[msg.sender].payouts.length == outcomeCount,
            "You have no shares!"
        );

        int256[] memory converted_payouts = new int256[](outcomeCount);
        for (uint i = 0; i < outcomeCount; i++) {
            converted_payouts[i] = convert(traders[msg.sender].payouts[i]);
        }

        return converted_payouts;
    }

    function sum(SD59x18[] memory array) private pure returns (SD59x18) {
        SD59x18 s = sd(0);
        for (uint i = 0; i < array.length; i++) {
            s = s + array[i];
        }
        return s;
    }

    function get_price(uint256 i) public view returns (int256) {
        if (
            keccak256(abi.encodePacked(msr)) ==
            keccak256(abi.encodePacked("LMSR"))
        ) {
            return intoInt256(((quantities[i] / beta).exp()) / sum(quantities));
        } else {
            // "LS-LMSR"
            SD59x18 b = alpha * sum(quantities);
            SD59x18[] memory q_temp = new SD59x18[](quantities.length);
            for (uint j = 0; j < outcomeCount; j++) {
                q_temp[j] = (quantities[j] / b).exp();
            }
            SD59x18 sum_term = sum(q_temp);
            SD59x18 term1 = alpha * sum_term.ln();
            for (uint j = 0; j < outcomeCount; j++) {
                q_temp[j] = quantities[j] * (quantities[j] / b).exp();
            }
            SD59x18 term2_num = sum(quantities) *
                (quantities[i] / b).exp() -
                sum(q_temp);
            SD59x18 term2_denom = sum(quantities) * sum_term;

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

    function get_quantity_vector() public view returns (SD59x18[] memory) {
        return quantities;
    }

    function cost(SD59x18[] memory q) internal view returns (SD59x18) {
        if (
            keccak256(abi.encodePacked(msr)) ==
            keccak256(abi.encodePacked("LMSR"))
        ) {
            return cost_LMSR(beta, q);
        } else {
            // "LS-LMSR"
            SD59x18 b = alpha * sum(q);
            return cost_LMSR(b, q);
        }
    }

    function submitBet(uint i, int256 shares) public payable {
        SD59x18 cost = cost_of_bet(i, shares);
        SD59x18 converted_shares = convert(shares);
        int256 costDiff = intoInt256(cost);

        // Transfer funds from user's wallet to contract's wallet
        require(
            msg.value >= uint(costDiff),
            "Please pay the proper amount to submit bet; Check using cost of bet!"
        );

        quantities[i] = quantities[i] + converted_shares;

        if (traders[msg.sender].payouts.length < outcomeCount) {
            traders[msg.sender].payouts = new SD59x18[](outcomeCount);
        }
        traders[msg.sender].payouts[i] =
            traders[msg.sender].payouts[i] +
            converted_shares;

        // Transfer outcome tokens from contract's wallet to user's wallet
        //  require(outcomeTokens[i].transfer(msg.sender, shares), "Transfer failed");
    }

    function cost_of_bet(
        uint256 i,
        int256 shares
    ) public view returns (SD59x18) {
        SD59x18[] memory delta = new SD59x18[](outcomeCount);
        delta[i] = convert(shares);

        SD59x18[] memory oldQ = quantities;
        SD59x18[] memory newQ = new SD59x18[](outcomeCount);
        for (uint j = 0; j < outcomeCount; j++) {
            newQ[j] = oldQ[j] + delta[j];
        }

        SD59x18 oldCost = cost(oldQ);
        SD59x18 newCost = cost(newQ);
        SD59x18 costDiff = newCost - oldCost;
        return (costDiff / sd(1000));
    }

    function redeem_winnings() public payable {
        SD59x18[] memory payouts = traders[msg.sender].payouts;
        SD59x18 totalPayout = payouts[winning_index];
        totalPayout = totalPayout / sd(1000);

        int256 payout = intoInt256(totalPayout);
        require(intoInt256(totalPayout) > 0, "No winnings to redeem");
        traders[msg.sender].payouts = new SD59x18[](outcomeCount);
        payable(msg.sender).transfer(uint(payout));
    }
}
