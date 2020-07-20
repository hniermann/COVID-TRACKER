import requests, bs4
import pandas as pd
import seaborn as sb
import matplotlib as mp
import csv
import numpy
#Author Henry Niermann
#The purpose of this program is to get data from CSV files and format it to the user's requested parameters
def extractAndFormat(state,daysNumber):
    colNumber = 0
    stateFile = open('data/dataStates.csv',newline='')
    stateFileReader = csv.reader(stateFile)
    states = list(stateFileReader)
    for curr in states:
        if str(state) == str(curr[0]):
            break
        colNumber = colNumber+1
    
    casesFile = open('data/dataCases.csv',newline='')
    casesFileReader = csv.reader(casesFile)
    cases = list(casesFileReader)
    stateCases = []
    i = len(cases)-daysNumber
    while i < len(cases):
        stateCases.append(int(cases[i][colNumber]))
        i = i+1
    
    datesFile = open('data/dataDates.csv',newline='')
    datesFileReader = csv.reader(datesFile)
    dates = list(datesFileReader)
    formattedDates = []
    j = len(dates)-daysNumber
    while j < len(dates):
        formattedDates.append(dates[j][0])
        j = j+1

    data = pd.DataFrame({'Date': formattedDates, str(state)+" Cases" : stateCases})
    return data

def display(d,state):
    sb.set(font_scale=0.8)
    plot = sb.relplot(x="Date", y=str(state)+" Cases", data=d)
    plot.set_xticklabels(rotation=90)
    mp.pyplot.show()
    



#MAIN PROGRAM
#Request state and number of days
print('What state?')
state = input()
print('Number of days?')
daysNumber = input()
daysNumber = int(daysNumber)
#Extract information from CSV files and merge into a data set
data = extractAndFormat(state,daysNumber)
#Display data into plot
display(data,state)

