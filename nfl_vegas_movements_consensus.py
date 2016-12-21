# coding=utf-8
#
# Script to srap data of consensus movemetns from vegasinsider
# Opens page for one week of a season - soup_url
# Than finds all BT Movemetns links - get_games_links
# And finaly write table data from link to csv - link_to_csv
#

import requests
from bs4 import BeautifulSoup
from requests.exceptions import ChunkedEncodingError
from requests.packages.urllib3.exceptions import ProtocolError

domain = 'http://www.vegasinsider.com'
# Blank list for repeating scraping on errors
errors = []

def soup_url(tdate,year):
    url = domain + '/nfl/matchups/matchups.cfm/week/' + str(tdate) + '/season/' + year
    soup_big = BeautifulSoup(requests.get(url).text, 'html.parser')
    soup = soup_big.find_all('table',width="100%")
    return soup

# Get all BT Movements links
def get_games_links(soup):
    return soup.find_all('a',text = 'BT Movements')


def link_to_csv(tdate,link):
        i = requests.get(link)

        bq = BeautifulSoup(i.text, 'html.parser')
        title = bq.find('td', attrs={'class': "page_title"})
        teams = title.font.string.split('@')
        btable = bq.find('table', attrs={'class': 'rt_railbox_border2'})
        rows = btable.find_all('tr')
        print(len(rows))
        table_rows = []
        # in each row find by css class
        for row in rows:
            row_values = []
            for td in row.find_all('td', attrs={'class': 'bg2'}):
                if (td.string):
                    row_values.append(u''.join(td.string.split()))
                elif (td.font and td.font.string):
                    row_values.append(u''.join(td.font.string.split()))
                else:
                    row_values.append(u'none')
            table_rows.append(row_values)

        with open('sbr/nfl_vegas_consensus_TrendsOnly_' + str(tdate) + '.csv', 'a') as f:
            header = ['home_team', 'away_team', 'date', 'time', 'ml_home_line', 'ml_away_line',
                      'rl_home_line', 'rl_away_line',
                      'tt_home_line', 'tt_away_line']
            f.write(','.join(header) + '\n')
            for table_row in table_rows:
                f.write(','.join(teams) + ',' + ','.join(table_row) + '\n')

        # Find table
        o = bq.find('strong', text='Trend Movement vs. Line').find_parent()

        req = requests.get(o.get('href'))
        bq = BeautifulSoup(req.text, 'html.parser')
        title = bq.find('td', attrs={'class': "page_title"})
        teams = title.font.string.split('@')
        btable = bq.find('table', attrs={'class': 'rt_railbox_border2'})
        rows = btable.find_all('tr')
        print(len(rows))
        table_rows = []
        for row in rows:
            row_values = []
            for td in row.find_all('td', attrs={'class': 'bg2'}):
                if (td.string):
                    row_values.append(u''.join(td.string.split()))
                elif (td.font and td.font.string):
                    row_values.append(u''.join(td.font.string.split()))
                else:
                    row_values.append(u'none')
            table_rows.append(row_values)

        with open('sbr/nfl_vegas_consensus_' + str(tdate) + '.csv', 'a') as f:
            header = ['home_team', 'away_team', 'date', 'time', 'ml_home_line', 'ml_home_trend', 'ml_away_line',
                       'ml_away_trend',
                       'rl_home_line', 'rl_home_trend', 'rl_away_line', 'rl_away_trend',
                      'tt_home_line', 'tt_home_trend', 'tt_away_line', 'tt_away_trend']
            f.write(','.join(header) + '\n')
            for table_row in table_rows:
                f.write(','.join(teams) + ',' + ','.join(table_row) + '\n')

def parse_to_csv(tdate,year):
    sp = BeautifulSoup(str(soup_url(tdate,year)), 'html.parser')

    for bt_mouvment_page in get_games_links(sp):
        try:
            link = domain+bt_mouvment_page.get('href')
            print(link)
            link_to_csv(tdate,link)
        except ProtocolError as e:
            print("ProtocolError")
            link_to_csv(tdate, link)
            print(link)
        except ChunkedEncodingError:
            print("ChunkedEncodingError")
            link_to_csv(tdate, link)
            print(link)

    for i in errors:
        try:
            print("One More time\n")
            link_to_csv(tdate,i)
        except AttributeError as e:
            print("Again Wrong Page\n")
            print(link)

if __name__ == '__main__':
    #season = '2015'
    season = '2016'
    mois = range(0,23)
    for week in mois:
        parse_to_csv(week,season)