pragma solidity >=0.8.0 <0.9.0;

import "@openzeppelin/contracts/utils/math/SafeMath.sol";
import "./token.sol";
import "./oracle.sol";

contract PredictionMarket {
    using SafeMath for uint256;

    Token token;
    Oracle public oracle;
    uint256 constant PRECISION = 10 ** 18;
    uint256 outcomeCount;
    uint256[] quantities;
    uint256 alpha;
    uint256 beta;
    string msr;

    struct Trader {
        uint256[] payouts;
    }

    mapping(address => Trader) internal traders;

    event Bet(address indexed trader, uint indexed index, uint shares);

    constructor(
        uint256 _outcomeCount,
        uint256 _alpha,
        uint256 _beta,
        Oracle _oracle,
        string memory _msr,
        Token _token
    ) public {
        outcomeCount = _outcomeCount;
        alpha = _alpha;
        beta = _beta;
        oracle = _oracle;
        msr = _msr;
        token = _token;

        quantities = new uint[](_outcomeCount);
        for (uint256 i = 0; i < outcomeCount; i++) {
            quantities[i] = 100 * PRECISION; // initialize to 100
        }
    }

    function get_price_vector() public view returns (uint256[] memory) {
        uint256[] memory prices = new uint256[](outcomeCount);
        for (uint256 i = 0; i < outcomeCount; i++) {
            prices[i] = get_price(i, quantities);
        }
        return prices;
    }

    function get_price(
        uint256 i,
        uint256[] memory q
    ) public view returns (uint256) {
        if (msr == "LMSR") {
            uint256 numerator = SafeMath.exp(q[i]) / PRECISION;
            uint256 denominator = 0;
            for (uint256 j = 0; j < outcomeCount; j++) {
                denominator = denominator.add(SafeMath.exp(q[j]) / PRECISION);
            }
            return numerator.mul(PRECISION).div(denominator);
        } else {
            // "LS-LMSR"

            uint256 totalShares = 0;
            for (uint j = 0; i < outcomeCount; j++) {
                totalShares += q[i];
            }
            uint256 b = alpha.mul(totalShares);
            uint256 sumTerm = 0;
            for (uint256 j = 0; j < outcomeCount; j++) {
                sumTerm = sumTerm.add(SafeMath.exp(q[j].div(b)));
            }
            uint256 term1 = alpha.mul(sumTerm.log());
            uint256 term2Num = totalShares.mul(q[i].div(b).exp()).sub(
                sumExponential(q, b)
            );
            uint256 term2Denom = totalShares.mul(sumTerm);
            return term1.add(term2Num.mul(PRECISION).div(term2Denom));
        }
    }

    function sumExponential(
        uint256[] memory q,
        uint256 b
    ) internal pure returns (uint256) {
        uint256 sum = 0;
        for (uint256 j = 0; j < q.length; j++) {
            sum = sum.add(SafeMath.exp(q[j].mul(q[j].div(b))));
        }
        return sum;
    }

    function cost_LMSR(
        uint256 b,
        uint256[] memory q
    ) internal pure returns (uint256) {
        uint256 totalExp = 0;
        for (uint256 i = 0; i < outcomeCount; i++) {
            totalExp = totalExp.add(
                SafeMath.exp(quantities[i].mul(PRECISION).div(b)).div(PRECISION)
            );
        }
        return b.mul(totalExp.ln().mul(PRECISION)).div(PRECISION);
    }

    function cost(uint256[] memory q) public view returns (uint256) {
        if (msr == "LMSR") {
            return cost_LMSR(beta, q);
        } else {
            // "LS-LMSR"
            uint256 qTotal = 0;
            for (uint256 i = 0; i < outcomeCount; i++) {
                qTotal += quantities[i];
            }
            uint256 b = alpha.mul(qTotal);
            return cost_LMSR(b, q);
        }
    }

    function submitBet(uint i, uint shares) public payable {
        uint256[] memory delta = new uint[](outcomeCount);
        delta[i] = shares;

        uint256[] memory oldQ = quantities;
        uint256[] memory newQ = new uint[](outcomeCount);
        for (uint j = 0; j < outcomeCount; j++) {
            newQ[j] = oldQ[j] + delta[j];
        }

        uint256 oldCost = cost(oldQ);
        uint256 newCost = cost(newQ);
        uint256 costDiff = newCost.sub(oldCost);

        // Transfer funds from user's wallet to contract's wallet
        require(
            token.transferFrom(msg.sender, address(this), costDiff),
            "Transfer failed"
        );

        quantities = newQ;

        // Transfer outcome tokens from contract's wallet to user's wallet
        //  require(outcomeTokens[i].transfer(msg.sender, shares), "Transfer failed");
    }

    function redeem_winnings() public {
        uint256[] memory payouts = traders[msg.sender].payouts;
        uint256 totalPayout = 0;
        for (uint256 i = 0; i < outcomeCount; i++) {
            totalPayout = totalPayout.add(payouts[i]);
        }
        require(totalPayout > 0, "No winnings to redeem");
        traders[msg.sender].payouts = new uint256[](outcomeCount);
        msg.sender.transfer(totalPayout);
    }
}
