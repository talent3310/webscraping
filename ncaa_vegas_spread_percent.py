# coding=utf-8
#
# Script to srap data of final conesnsus values
# Opens page for one week of a season - soup_url
# Than in sequence of methods find some nested cells with data - g get_games_links get_game_info
# And finaly write table data from link to csv

import requests
import datetime
from bs4 import BeautifulSoup

domain = 'http://www.vegasinsider.com'
errors = []


# def soup_url_prev(tdate,year):
#     url = domain + '/college-basketball/matchups/matchups.cfm/week/' + str(tdate) + '/season/' + year
#     print(url)
#     soup_big = BeautifulSoup(requests.get(url).text, 'html.parser')
#     soup = soup_big.find_all('table',width="100%")
#     return soup
def soup_url(date):

    day = ('0' if len(str(date.day)) == 1 else '') + str(date.day)
    month = ('0' if len(str(date.month)) == 1 else '') + str(date.month)
    year = ('0' if len(str(date.year)) == 1 else '') + str(date.year)

    url = domain + '/college-basketball/matchups/matchups.cfm/date/' + month + '-' + day + '-' + year
    print(url)
    soup_big = BeautifulSoup(requests.get(url).text, 'html.parser')
    soup = soup_big.find_all('table',width="100%")
    return soup

# Finding all games tables
def g(soup):
    return soup.find_all('td',attrs={'class':'viBodyBorderNorm'})

# Get all rows from games tables
def get_games_links(soup):
    return soup.find_all('tr')

# Get cells with data
def get_game_info(o):
    return o.find_all('td',attrs={'class': "cellTextNorm"})

# def parse_to_csv_prev(tdate,year):
#     sp = BeautifulSoup(str(soup_url(tdate,year)), 'html.parser')
#     # Result list
#     a = []
#     for uis in g(sp):
#         for bt_mouvment_page in get_games_links(uis):
#             # array to fill with data of each row
#             d = [str(year), str(tdate)]
#             if get_game_info(bt_mouvment_page) != None:

#                 for i in get_game_info(bt_mouvment_page):
#                     # team name
#                     if i.a:
#                         d.append(i.a.string.strip())
#                     elif i.string == None:
#                         d.append('NaN')
#                     elif i.string.strip() == '' :
#                         d.append('NaN')
#                     # Data
#                     else:
#                         d.append(i.string.strip())
#             if len(d) > 2:
#                 a.append(','.join(d) + '\n')
#                 with open('vegasinsider.csv', 'a') as t:
#                     t.write(','.join(d) + '\n')

def parse_to_csv(date):
    sp = BeautifulSoup(str(soup_url(date)), 'html.parser')
    # Result list
    a = []
    for uis in g(sp):
        for bt_mouvment_page in get_games_links(uis):
            # array to fill with data of each row
            day = ('0' if len(str(date.day)) == 1 else '') + str(date.day)
            month = ('0' if len(str(date.month)) == 1 else '') + str(date.month)
            year = ('0' if len(str(date.year)) == 1 else '') + str(date.year)            

            d = [year, month + day]
            if get_game_info(bt_mouvment_page) != None:

                for i in get_game_info(bt_mouvment_page):
                    # team name
                    if i.a:
                        d.append(i.a.string.strip())
                    elif i.string == None:
                        d.append('NaN')
                    elif i.string.strip() == '' :
                        d.append('NaN')
                    # Data
                    else:
                        d.append(i.string.strip())
            if len(d) > 2:
                a.append(','.join(d) + '\n')
                with open('vegasinsider.csv', 'a') as t:
                    t.write(','.join(d) + '\n')


if __name__ == '__main__':
    #seasons = ['2008','2009','2010','2011','2012','2013','2014','2015']
    #for season in seasons:

    # season = '2015'
    # mois = range(1,23)
    # # mois = range(1,2)
    # for week in mois:
    #     try:
    #         parse_to_csv(week,season)
    #     except:
    #         print(week,season)

    start_year = input("Please type the year for which you would like to pull data (yyyy):")
    start_month = input("Please type the starting month for which you would like to pull data (1-12):")
    start_day = input("Please type the starting month for which you would like to pull data (1-31):")
    numdays = input("Please type the last month for which you would like to pull data (1-365):")

    # numdays = 130
    base = datetime.datetime(int(start_year), int(start_month), int(start_day))
    date_list = [base + datetime.timedelta(days=x) for x in range(0, int(numdays))]


    for date_object in date_list:
        try:
            parse_to_csv(date_object)
        except AttributeError:
            print('wrong date'+str(date_object))
            pass

