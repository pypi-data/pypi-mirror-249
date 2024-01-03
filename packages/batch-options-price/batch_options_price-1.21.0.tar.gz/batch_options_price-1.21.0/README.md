
# batch_options_price

Installation
-------------

pip install batch-options-price 

Documentation
-------------
BSB - Black-Scholes Used for pricing European options on stocks without dividends

BSB.option_price_batch(volatility, daysToExpiration, underlyingPrice, strikePrice, interestRate, side)

eg: 
prices = BSB.option_price_batch(pd.Series([0.31, 0.29]), pd.Series([125, 26]), pd.Series([25, 26]), pd.Series([25, 26]), 4, 'C')

Returns the put-call price series 

Contributions:
--------------
Please send suggestions, critics,
