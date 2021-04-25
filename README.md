# Value-Investing-Stock-Picker
Python Personal Project
Uses Yahoo Finance API

The program removes any ticker from the list that is not found in the API.

The excel folder is for reference only and should not be used in the algorithm.

The .txt folder can be used for the algorithm they contain stocks from the same sector.

Results are more accurate when comparing stocks from the same sector.

columns for the excel document represent the following:
A = Ticker Symbol
B = PEG_RATIO
C = PB_RATIO
D = D/E_RATIO
E = cachflow/MarketCap 
F = recommendation key
G = Average of shord mid and long term trend predictions
H = number of metrics analysed for that specific stock
I = Total (The higher the total the more undervalued the stock is)

Feel free to create your own account and get an API key:

https://rapidapi.com/apidojo/api/yahoo-finance1 

The API key can be copy pasted in the get metrics functions.
