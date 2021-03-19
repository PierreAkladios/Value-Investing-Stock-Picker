import numpy as np #numerical computing library
import pandas as pd #tabular data
import xlsxwriter #writting to excel
import requests #http requests
from scipy import stats 
import math
import json

#input from user
ticker = input("Enter the ticker symbol you would like to analyse: ")
country = input("Enter the country of the company: ")

# metrics come from this article 
# https://www.investopedia.com/articles/fundamental-analysis/09/five-must-have-metrics-value-investors.asp
price = 0
earning = 0
book = 0
debt = 0
equity = 0 
debtEquity_ratio = 0 # not too high but not too low
pe_ratio = 0 # good for compagnies in same industry lower = better
pb_ratio = 0 #<1 is good
freeCachFlow = 0 #the higher the better
peg_ratio = 0 # than 1 is good
marketCap = 0
recommendationKey = False
cachCap_ratio = 0

""" try:
    #API code
catch(not equal 200) """

#Api Code
#make this into a method 
url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-statistics"

querystring = {"symbol":ticker,"region":country}

headers = {
    'x-rapidapi-key': "4e08668ab1mshd05172b533fcfb5p1809a2jsnd750a952af5e",
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

#printing the data for texts
#print(response.text)
#changing Jason

#NAME OF ERROR JSONDecodeError
#use this to do the try catch statment to get the calues
#Like a loop that keeps asking for the two inputs then calls the API function 
json_object = json.loads(response.text)

#setting values
if int(json_object["defaultKeyStatistics"]["pegRatio"]["raw"]) != None:
    peg_ratio = int(json_object["defaultKeyStatistics"]["pegRatio"]["raw"])
if int(json_object["defaultKeyStatistics"]["priceToBook"]["raw"]) != None:
    pb_ratio = int(json_object["defaultKeyStatistics"]["priceToBook"]["raw"])
if int(json_object["financialData"]["debtToEquity"]["raw"]) != None:
    debtEquity_ratio = int(json_object["financialData"]["debtToEquity"]["raw"])
if int(json_object["financialData"]["freeCashflow"]["raw"]) != None:
    freeCachFlow = int(json_object["financialData"]["freeCashflow"]["raw"])
if int(json_object["quoteData"][str(ticker).upper()]["marketCap"]["raw"]) != None:
    marketCap = int(json_object["quoteData"][str(ticker).upper()]["marketCap"]["raw"])    
if json_object["financialData"]["recommendationKey"] != None:
    if str(json_object["financialData"]["recommendationKey"]) == "buy":
        recommendationKey = True

def cachCap_ratio(freeCachFlow, marketCap):
    if freeCachFlow != 0 and marketCap != 0:
       return freeCachFlow/marketCap
    return 0

def algo_picker(peg_ratio, pb_ratio, debtEquity_ratio, cachCap_ratio, recommendationKey):
    pass

print(peg_ratio)
print(pb_ratio)
print(debtEquity_ratio)
print(json_object["financialData"]["recommendationKey"])
print(recommendationKey)
#search for target low and high prices
#go through financial data and prices to see if there is any more usefull metrics
#get market cap
#long term trend
#Recomendation key
