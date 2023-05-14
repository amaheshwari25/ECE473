
var BettingMarket = artifacts.require("PredictionMarket");
var outcome_count = 2
var zero = '0'
alpha = 3
beta = 15027
var msr = "LSLMSR"


module.exports = function(deployer) {
  deployer.deploy(BettingMarket, outcome_count, alpha, beta, msr);
};