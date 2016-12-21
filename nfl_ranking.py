import requests
from bs4 import BeautifulSoup
from splinter import Browser
from datetime import date
import time
from pandas import DataFrame
from selenium import webdriver
import re
import os

import datetime
import os.path
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.ui import Select

url = "http://www.usatoday.com/sports/nfl/rankings/"

namesListFromSite = [
	'Arizona', 
	'Atlanta', 
	'Baltimore', 
	'Buffalo', 
	'Carolina', 
	'Chicago', 
	'Cincinnati', 
	'Cleveland', 
	'Dallas', 
	'Denver', 
	'Detroit', 
	'Green Bay', 
	'Houston', 
	'Indianapolis', 
	'Jacksonville', 
	'Kansas City', 
	'Los Angeles', 
	'Miami', 
	'Minnesota', 
	'New England', 
	'New Orleans', 
	'New York', 
	'New York', 
	'Oakland', 
	'Philadelphia', 
	'Pittsburgh', 
	'San Diego', 
	'San Francisco', 
	'Seattle', 
	'Tampa Bay', 
	'Tennessee', 
	'Washington']
result_rankings = []
#     return soup
def getSoup(url):

    soup_big = BeautifulSoup(requests.get(url).text, 'html.parser')
    soup_table = soup_big.find('table',attrs={'class':'rankings'})
    soup_rows = soup_table.find_all('tr')
    return soup_rows

def table_tds(soup):
	return soup.find_all('td')



def main():
	row = ['rank', 'team', 'record', 'change', 'hi/low']
	with open('result/nflTeamsRanking.csv', 'a') as t:
                            t.write(','.join(row) + '\n')
	soupRows = getSoup(url)
	count = 0
	for row in soupRows :
		if count == 0:
			count += 1
		else  :
			tds = table_tds(row)
			oneRow = []
			for td in tds :
				item = td.attrs['class'][0]
				if item == 'ranking' :
					oneRow.append(td.contents[0].split()[0])
			
				if item == 'team_slug' :
					team_name = td.find('span', attrs={'class':'first_name'})
					temp = team_name.contents
					if temp[0] == 'New York' :
						team_last_name = td.find('span', attrs={'class':'last_name'})
						name = temp[0] + ' ' + team_last_name.contents[0]
						oneRow.append(name)
					else :
						oneRow.append(temp[0])

				if item == 'record' :
					oneRow.append(td.contents[0].split()[0])

				if item == 'ranking_diff' :
					item_span = td.find('span')
					temp = item_span.attrs['class'][0]
					if temp == 'rank-sm-no' :
						oneRow.append('0')
					if temp == 'rank-sm-up' :
						oneRow.append(item_span.contents[0])
					if temp == 'rank-sm-dn' :
						tt = '-' + item_span.contents[0]
						oneRow.append(tt)	
				if item == 'ranking_hilo' :
					tt = td.contents[0].split()[0] + td.contents[0].split()[1] + td.contents[0].split()[2]
					oneRow.append(tt)

			result_rankings.append(oneRow)
			print('row=>\n', oneRow)
			with open('result/nflTeamsRanking.csv', 'a') as t:
                            t.write(','.join(oneRow) + '\n')

	toWriteData = []
	toWriteData.append(row)
	toWriteData.append(result_rankings)
	# print(toWriteData)
main()

