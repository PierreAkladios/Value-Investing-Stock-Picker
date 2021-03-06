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
    #insert API key here
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
    
#Smaller than 1 is good so we inverse it to et the highest score
def pb(pb_ratio): 
    return 1/pb_ratio

#The lower the better in debt equity but algorithm is based on high score
def debtEquity(debtEquity_ratio):
    return 1/debtEquity_ratio

#look at short mid and long term prediction of trends
def trends(shortT, midT, longT):
    total = 0
    number = 0 #number of non null arguments
    #checking short Term potential
    if shortT != None:
        number+=1
        if(shortT == "UP"):
            total+=0.5
    #checking mid Term potential
    if midT != None:
        number+=1
        if(midT == "UP"):
            total+=0.5   
    #checking long Term potential
    if longT != None:
        number+=1
        if(longT == "UP"):
            total+=0.5    
    if number!= 0:
        return total/number
    else:
        return 0
    

def algo_picker(peg_ratio, pb_ratio, debtEquity_ratio, cachCap_ratio, recommendationKey, trend):
    total = 0
    number_of_metrics = null_checker(peg_ratio, pb_ratio, debtEquity_ratio, cachCap_ratio, recommendationKey, trend)
     #call helper functions for the first 3 metrics
    if peg_ratio!=0 and peg_ratio!=None :
        total += peg(peg_ratio)
    if pb_ratio !=None and pb_ratio!=0:
        total+=pb(pb_ratio)
    if debtEquity_ratio != None and debtEquity_ratio != 0:
        total += debtEquity(debtEquity_ratio)
    #check Freecachflow:
    if cachCap_ratio != None:
        total += cachCap_ratio
    #check recommendation key
    if recommendationKey == True:
        total +=0.5
    #adding trend to the total    
    if trend !=None:
        total+= trend

    #adding all the data for excel
    listOfMetrics.append(peg_ratio)
    listOfMetrics.append(pb_ratio)
    listOfMetrics.append(debtEquity_ratio)
    listOfMetrics.append(cachCap_ratio)
    listOfMetrics.append(recommendationKey)
    listOfMetrics.append(trend)
    listOfMetrics.append(number_of_metrics)
    return total/number_of_metrics
# metrics come from this article 
# https://www.investopedia.com/articles/fundamental-analysis/09/five-must-have-metrics-value-investors.asp

#file reader
def file_reader(fileName):
    file1 = open(fileName, "r")
    Lines = file1.readlines()
    #adding all the ticker symbol in the file in a list
    for line in Lines:
        Names.append(line)

def json_reader(json_object):
    #global variables
    global debtEquity_ratio 
    global pb_ratio
    global freeCachFlow 
    global peg_ratio 
    global marketCap
    global recommendationKey 
    global cachCap_ratio 
    global shortT 
    global midT 
    global longT 
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

#reseting global variables to 0 after each iteration
def clear_metrics():
     #global variables
    global debtEquity_ratio 
    global pb_ratio
    global freeCachFlow 
    global peg_ratio 
    global marketCap
    global recommendationKey 
    global cachCap_ratio 
    global shortT 
    global midT 
    global longT 
    #clearing global variables
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
    json_object = None
    response = None
    listOfMetrics.clear()


#Global variables
Names = []       
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
listOfMetrics = []


#printing the data for texts
#print(response.text)

#NAME OF ERROR JSONDecodeError
#use this to do the try catch statment to get the calues
#Like a loop that keeps asking for the two inputs then calls the API function 
json_object = None
response = None
#used for 1 ticker only
'''
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
'''

#Test
""" print(peg_ratio)
print(pb_ratio)
print(debtEquity_ratio)
print(json_object["financialData"]["recommendationKey"])
print(recommendationKey)
print(shortT)
print(midT)
print(longT) """

#print(result)

#make the input a .txt file containing a long list of stocks
#making the excel part and the rest of the program able to iterate

#making it work for many stocks at the same time

#getting the list of all ticker symbols
isInvalid = True
fileName = input("Enter the name of the .txt file: ").strip().upper()
while isInvalid: 
    try:
        file_reader(fileName)
        isInvalid = False
        sheetName = fileName.replace(".txt","")
    except FileNotFoundError:
        fileName = input("File name is invalid. Please Enter the Name of a valid .txt file: ").strip().upper()

# Create an new Excel file and add a worksheet.
book = xlsxwriter.Workbook(sheetName+".xlsx")
sheet = book.add_worksheet()
i = 0
for name in Names:
    ticker = name.strip()
    listOfMetrics.append(ticker)
    response = getMetrics(ticker, "CA")
    try:
        json_object = json.loads(response.text)
    except json.JSONDecodeError: #Find a way to import this error
        clear_metrics()
        i+=1
        continue
    #catching key errors in json
    try:
        json_reader(json_object)
    except KeyError:
        clear_metrics()
        i+=1
        continue
    trend = trends(shortT,midT,longT)
    cachCap_ratio = cachCap(freeCachFlow,marketCap)
    result = algo_picker(peg_ratio, pb_ratio,debtEquity_ratio,cachCap_ratio, recommendationKey, trend)
    #adding result for excel
    listOfMetrics.append(result)
    #Printing all the metrics on a row in excel
    for col_num, data in enumerate(listOfMetrics):
        sheet.write(i, col_num, data)
    clear_metrics()
    i+=1
book.close()

