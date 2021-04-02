import numpy as np #numerical computing library
import pandas as pd #tabular data
import xlsxwriter #writting to excel
import requests #http requests
#from scipy import stats 
import math
import json

## Global yf api
url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-statistics"


def getMetrics(ticker, country):
    #Api Code
    querystring = {"symbol":ticker,"region":country}

    headers = {
    'x-rapidapi-key': "4e08668ab1mshd05172b533fcfb5p1809a2jsnd750a952af5e",
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
 
    response = requests.request("GET", url, headers=headers, params=querystring)

    return response

def cachCap(freeCachFlow, marketCap):
    if freeCachFlow != None and marketCap != None:
       return freeCachFlow/marketCap
    return 0

def null_checker(peg_ratio, pb_ratio, debtEquity_ratio, cachCap_ratio, recommendationKey, trend):
    non_null_metrics = 0 #number of non null arguments
    if peg_ratio != None:
        non_null_metrics+=1
    if pb_ratio != None:
        non_null_metrics+=1
    if debtEquity_ratio != None:
        non_null_metrics+=1
    if cachCap_ratio != None:
        non_null_metrics +=1 
    if recommendationKey != None:
        non_null_metrics +=1
    if trend != None:
        non_null_metrics+=1
    return non_null_metrics
    

#returns the inverted peg ratio because a low peg is good and the algorith will try to get the highest score possible
def peg(peg_ratio):
    return 1/peg_ratio
    
#not sure
def pb(pb_ratio): 
    pass

#not sure
def debtEquity(debtEquity_ratio):
    pass

#look at short mid and long term prediction of trends
def trends(shortT, midT, longT):
    total = 0
    number = 0 #number of non null arguments
    #checking short Term potential
    if shortT != None:
        number+=1
        if(shortT == "UP"):
            total+=1
        elif (shortT == "DOWN"):
            total +=1
    #checking mid Term potential
    if midT != None:
        number+=1
        if(midT == "UP"):
            total+=1
        elif (midT == "DOWN"):
            total +=1
    #checking long Term potential
    if longT != None:
        number+=1
        if(longT == "UP"):
            total+=1
        elif (longT == "DOWN"):
            total +=1
    if number!= 0:
        return total/number
    else:
        return 0
    

def algo_picker(peg_ratio, pb_ratio, debtEquity_ratio, cachCap_ratio, recommendationKey, trend):
    total = 0
    number_of_metrics = null_checker(peg_ratio, pb_ratio, debtEquity_ratio, cachCap_ratio, recommendationKey, trend)
    #check recommendation key
    if recommendationKey == True:
        total +=1
    #check Freecachflow:
    if cachCap_ratio != None:
        total += cachCap_ratio
    #call helper functions for the other 3 methods
    if peg_ratio!=0:
        peg(peg_ratio)
    if trend !=None:
        total+= trend
    if peg_ratio !=None:
        pass
    if pb_ratio !=None:
        pass
    return total/number_of_metrics
# metrics come from this article 
# https://www.investopedia.com/articles/fundamental-analysis/09/five-must-have-metrics-value-investors.asp
price = None
debtEquity_ratio = None # not too high but not too low
pb_ratio = None #<1 is good
freeCachFlow = None #the higher the better
peg_ratio = None # than 1 is good
marketCap = None
recommendationKey = None
cachCap_ratio = None
shortT = None
midT = None
longT = None
trend = None

""" try:
    #API code
catch(not equal 200) """

#printing the data for texts
#print(response.text)
#changing Jason

#NAME OF ERROR JSONDecodeError
#use this to do the try catch statment to get the calues
#Like a loop that keeps asking for the two inputs then calls the API function 
json_object = None
response = None

isInvalid = True
while (isInvalid):
    
    #input from user
    ticker = input("Enter the ticker symbol you would like to analyse: ").strip().upper()
    country = input("Enter the country of the company: ").strip().upper()

    response = getMetrics(ticker, country)

    try:
        json_object = json.loads(response.text)
        isInvalid = False
    except(json.decoder.JSONDecodeError):
        print("ERROR")
        isInvalid = True

#Extracting metrics from json
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
#Extracting trends from json
if json_object["pageViews"]["shortTermTrend"]!=None:
    shortT = str(json_object["pageViews"]["shortTermTrend"])
if json_object["pageViews"]["midTermTrend"]!=None:
    midT = str(json_object["pageViews"]["midTermTrend"])
if json_object["pageViews"]["longTermTrend"]!=None:
    longT = str(json_object["pageViews"]["longTermTrend"])

trend = trends(shortT,midT,longT)
cachCap_ratio = cachCap(freeCachFlow,marketCap)
result = algo_picker(peg(peg_ratio), pb(pb_ratio),debtEquity(debtEquity_ratio),cachCap_ratio, recommendationKey, trend)

""" print(peg_ratio)
print(pb_ratio)
print(debtEquity_ratio)
print(json_object["financialData"]["recommendationKey"])
print(recommendationKey)
print(shortT)
print(midT)
print(longT) """

print(result)
#go through financial data and prices to see if there is any more usefull metrics