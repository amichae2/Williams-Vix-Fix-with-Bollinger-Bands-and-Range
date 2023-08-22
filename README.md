# Williams-Vix-Fix-with-Bollinger-Bands-and-STD
This code mimics the code of ChrisMoody's Williams Vix Fix with Bollinger Bands and STD on TradingView

This code is based on the code for this Community Script: https://www.tradingview.com/script/og7JPrRA-CM-Williams-Vix-Fix-Finds-Market-Bottoms/

WARNING: The Standard Deviation (STD) Calculation touches the Williams VIX Fix (WVF) at the correct time but does not yield the exact same STD as the one on TradingView. I do not understand why this is but it appears to mirror the one on TradingView better the farther back you go. The upper and lower range, WVF and SMAs are correct.

WARNING: If you adjust the lookback periods in this code you need to adjust the number of Nones hard coded in the other funtions.

The reason the get_sum function is custom is because it is based on the SUM function in TradingViews example which is biased.

This code needs a Pandas Dataframe that has both "Close" and "Low" columns. It needs a period of 71 closes and lows or greater.

Anyone can use this code for anything they want.
