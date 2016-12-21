# coding=utf-8
# Script to scrap consensus data from sportsplays.com
# Uses site menu to choose date and after that grab consensus data for all games

import requests
import datetime
import os.path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.ui import Select
import time

def send_request():
    try:
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap[
            "phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 (KHTML, like Gecko) Chrome/15.0.87"
        service_args = [
            '--proxy=127.0.0.1:9050',
            '--proxy-type=socks5']
        # driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=service_args)
        driver = webdriver.PhantomJS("C:\\Users\\worri\\AppData\\Local\\Programs\\Python\\Python35-32\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")

        base_url = "https://www.sportsinteraction.com/football/nfl-betting-lines/"
        driver.get(base_url)

        # Choose date in menu
        # Select(driver.find_element_by_id("from_date_day")).select_by_value(str(date.day))
        # Select(driver.find_element_by_id("from_date_month")).select_by_value(str(date.month))
        # Select(driver.find_element_by_id("from_date_year")).select_by_value(str(date.year))
        # driver.find_element_by_name("commit").click()
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        return soup
    except requests.exceptions.RequestException:
        print('HTTP Request failed')

def parse_to_csv():

    soup = send_request()

    header = ['game_date', 'game_time', 'home', 'away', 'home_spread', 'away_spread']
    day_marker = time.strftime("%Y%m%d")
    file_name = 'sportsplay/nfl_sportsinteraction_'+ day_marker +'.csv'

    # get games
    gameDate = ""
    for gameHtml in soup.find_all('div', {'class': 'game'}):
        # get date
        if (gameHtml.find('h2', {'class': 'date'}).string != None):
            gameDate = gameHtml.find('h2', {'class': 'date'}).string.replace(",", "")

        print (gameDate)
        # get time
        gameTime = gameHtml.find('span', {'class', 'time'}).string
        gameTime = gameTime.replace("\n", "").replace(" ", "").replace("\t", "")
        print (gameTime)

        teamNames = gameHtml.find_all('span', {'class', 'name'})
        # get home name
        homeName = teamNames[0].string
        # get away name
        awayName = teamNames[1].string

        print(homeName)
        print(awayName)

        spreads = gameHtml.find_all('span', {'class', 'handicap'})
        spreads[0].string = spreads[0].string.encode("cp949", "ignore").decode()
        spreads[1].string = spreads[1].string.encode("cp949", "ignore").decode()
        # get home spread
        homeSpread = spreads[0].string.replace("\n", "").replace(" ", "").replace("\t", "")       
        if (homeSpread == ''):
            homeSpread = '0.0'
        # get away spread
        awaySpread = spreads[1].string.replace("\n", "").replace(" ", "").replace("\t", "")
        if (awaySpread == ''):
            awaySpread = '0.0'
        print(homeSpread)
        print(awaySpread)

        row_values = [gameDate, gameTime, homeName, awayName, homeSpread, awaySpread]
        with open(file_name,'a') as f:
            if(os.stat(file_name).st_size == 0):
                f.write(','.join(header)+'\n')
            f.write(','.join(row_values)+'\n')        

 



    # header = ['srap_datetime','game_date','game_time','home','away','rl_home_percentage','rl_away_percentage']
    # day_marker = str(datetime.datetime.today().month) + str(datetime.datetime.today().day)
    # table = soup.find('table',attrs={'id':'consensus_events'})
    # rows = table.find_all('tr')
    # # for each row find by cell all divs inside
    # for row in rows:

    #     day = ('0' if len(str(date.day)) == 1 else '') + str(date.day)
    #     month = ('0' if len(str(date.month)) == 1 else '') + str(date.month)
    #     year = ('0' if len(str(date.year)) == 1 else '') + str(date.year)

    #     row_values = [str(datetime.datetime.today()), year + month + day]
    #     for td in row.find_all('td'):
    #         for div in td.find_all('div'):
    #             if(div.string): 
    #                 row_values.append(' '.join(div.string.split()))
    #                 div.string.split()
    #             elif(div.font): 
    #                 row_values.append(' '.join(div.font.string.split()))
    #     if (len(row_values[2:])>0):
    #         # get home name
    #         splits = row_values[3].split()
    #         splits_name = []
    #         for k in range(1, len(splits)):
    #             splits_name.append(splits[k])
    #         row_values[3] = ' ' . join(splits_name)

    #         # get away name
    #         splits = row_values[4].split()
    #         splits_name = []
    #         for k in range(1, len(splits)):
    #             splits_name.append(splits[k])
    #         row_values[4] = ' ' . join(splits_name)

    #         row_values_home = [row_values[0], row_values[1], row_values[2], row_values[3],
    #                             row_values[4], row_values[7], row_values[8]]
    #         row_values_away = [row_values[0], row_values[1], row_values[2], row_values[4],
    #                             row_values[3], row_values[8], row_values[7]]
    #     file_name = 'sportsplay/nfl_sportsplay_'+str(day_marker)+'.csv'

    #     with open(file_name,'a') as f:
    #         if(os.stat(file_name).st_size == 0):
    #             f.write(','.join(header)+'\n')
    #         if(len(row_values[2:])>0): 
    #             f.write(','.join(row_values_home)+'\n')
    #             f.write(','.join(row_values_away)+'\n')

if __name__ == '__main__':
    # For realtime scraping it takes current and next 7 days
    # If needed get old historical data it's possible to modify date_list range

    try:
        parse_to_csv()
    except AttributeError:
        print('wrong ')
        pass