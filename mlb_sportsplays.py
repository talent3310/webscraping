# coding=utf-8
import requests
import datetime
import os.path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select

def send_request(date):
    try:
        driver = webdriver.PhantomJS("C:\\Users\\worri\\AppData\\Local\\Programs\\Python\\Python35-32\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")
        base_url = "http://www.sportsplays.com/consensus/MLB.html"
        driver.get(base_url)
        Select(driver.find_element_by_id("from_date_day")).select_by_value(str(date.day))
        Select(driver.find_element_by_id("from_date_month")).select_by_value(str(date.month))
        Select(driver.find_element_by_id("from_date_year")).select_by_value(str(date.year))
        driver.find_element_by_name("commit").click()
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        return soup
    except requests.exceptions.RequestException:
        print('HTTP Request failed')

def parse_to_csv(date):
    header = ['srap_datetime','game_date','game_time','home','away','rl_home_picks','rl_away_picks','rl_home_percentage','rl_away_percentage','ml_home_picks','ml_away_picks','ml_home_percentage','ml_away_percentage','tt_home_picks','tt_away_picks','tt_home_percentage','tt_away_percentage']
    soup = send_request(date)
    day_marker = str(datetime.datetime.today().month).zfill(2) + str(datetime.datetime.today().day)
    table = soup.find('table',attrs={'id':'consensus_events'})
    rows = table.find_all('tr')
    for row in rows:
        row_values = [str(datetime.datetime.today()),str(date.day)+'.'+str(date.month)+'.'+str(date.year)]
        for td in row.find_all('td'):
            for div in td.find_all('div'):
                if(div.string): row_values.append(''.join(div.string.split()))
                elif(div.font): row_values.append(''.join(div.font.string.split()))
        file_name = 'sportsplay/mlb_sportsplay_'+str(day_marker)+'.csv'
        with open(file_name,'a') as f:
            if(os.stat(file_name).st_size == 0):
                f.write(';'.join(header)+'\n')
            if(len(row_values[2:])>0): f.write(';'.join(row_values)+'\n')

if __name__ == '__main__':
    numdays = 2
    base = datetime.datetime.today()
    date_list = [base + datetime.timedelta(days=x) for x in range(0, numdays)]
    for date_object in date_list:
        try:
            parse_to_csv(date_object)
        except AttributeError:
            print('wrong date'+str(date_object))
            pass