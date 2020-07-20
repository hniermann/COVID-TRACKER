import requests, bs4
import pandas as pd
import seaborn as sb
import matplotlib as mp
import csv

#Author Henry Niermann
#Program to scrape COVID data and display it for viewing

def getStates(page):
    states = []
    firstStateChild = page.find(title='COVID-19 pandemic in Alaska')
    states.append(firstStateChild.get_text())
    firstState = firstStateChild.find_parent('th')
    i = 0
    for state in firstState.find_next_siblings('th'):
        if i == 54:
            break
        states.append(state.find('a').get_text())
        i = i+1
    return states

def getDates(page):
    dates = []
    firstDateChild = page.find(title='January 21, 2020')
    dates.append(firstDateChild.get_text())
    firstDateChild2 = firstDateChild.find_parent('th')
    firstDate = firstDateChild2.find_parent('tr')
    for date in firstDate.find_next_siblings('tr'):
        childDate = date.find('abbr')
        if childDate is not None and childDate.get_text() != 'AK':
            dates.append(childDate.get_text())
    return dates

def getCases(page):
    cases = []
    firstCaseChild = page.find(title='January 21, 2020')
    firstCaseChild2 = firstCaseChild.find_parent('th')
    row = 0
    column = 0
    firstRow = []
    for case in firstCaseChild2.find_next_siblings('td'):
        if column == 55:
            break
        if case.get_text(strip=True) != '':
            firstRow.append(case.get_text(strip=True))
            column = column+1
        else:
            firstRow.append('0')
            column = column+1
    cases.append(firstRow)
    column = 0
    row = 1
    firstCase = firstCaseChild2.find_parent('tr')
    for caseRow in firstCase.find_next_siblings('tr'):
        if len(caseRow.find_all('td')) > 0:
            currRow = []
            for case in caseRow.find_all('td'):
                if column == 55:
                    break
                if case.get_text(strip=True) == '':
                    currRow.append('0')
                    column = column+1
                else:
                    currRow.append(case.get_text(strip=True))
                    column = column+1
            column = 0
            row = row+1
            cases.append(currRow)

    return cases

  
def sendData(states,dates,cases):
    dataCasesFile = open('data/dataCases.csv','w+',newline='')
    dataCasesWriter = csv.writer(dataCasesFile)
    for row in cases:
        dataCasesWriter.writerow(row)
    dataCasesFile.close()
    dataStatesFile = open('data/dataStates.csv','w+',newline='')
    dataStatesWriter = csv.writer(dataStatesFile)
    for state in states:
        dataStatesWriter.writerow([state])
    dataStatesFile.close()
    dataDatesFile = open('data/dataDates.csv','w+',newline='')
    dataDatesWriter = csv.writer(dataDatesFile)
    for date in dates:
        dataDatesWriter.writerow([date])
    dataDatesFile.close()


# MAIN PROGRAM
#Find page
res = requests.get('https://en.wikipedia.org/wiki/Template:COVID-19_pandemic_data/United_States_medical_cases')
numbersPage = bs4.BeautifulSoup(res.text,'html.parser')
# Get states, dates, and confirmed cases relating to those dates
states = getStates(numbersPage)
dates = getDates(numbersPage)
cases = getCases(numbersPage)
# Send data to CSV file
sendData(states,dates,cases)




