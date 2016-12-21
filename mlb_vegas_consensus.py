# coding=utf-8
import requests
from bs4 import BeautifulSoup

domain = 'http://www.vegasinsider.com'

def soup_url(tdate):
    url = domain + '/mlb/matchups/matchups.cfm/date/' + tdate
    soup_big = BeautifulSoup(requests.get(url).text, 'html.parser')
    soup = soup_big.find_all('table',width="100%")
    return soup

def get_games_links(soup):
    return soup.find_all('a',text = 'BT Movements')

def parse_to_csv(tdate):
    sp = BeautifulSoup(str(soup_url(tdate)), 'html.parser')

    for bt_mouvment_page in get_games_links(sp):
        try:
            link = domain+bt_mouvment_page.get('href')
            i = requests.get(link)
            bn = BeautifulSoup(i.text,'html.parser')
            o = bn.find('strong',text='Trend Movement vs. Line').find_parent()

            req = requests.get(o.get('href'))
            bq = BeautifulSoup(req.text,'html.parser')
            title = bq.find('td',attrs = {'class':"page_title"})
            teams = title.font.string.split('@')
            btable = bq.find('table',attrs = {'class':'rt_railbox_border2'})
            rows = btable.find_all('tr')
            table_rows = []
            for row in rows:
                row_values = []
                for td in row.find_all('td',attrs = {'class':'bg2'}):
                    if(td.string): row_values.append(u''.join(td.string.split()))
                    elif(td.font): row_values.append(u''.join(td.font.string.split()))
                table_rows.append(row_values)
            with open('mlb_vegas_consensus_'+tdate+'.csv','a') as f:
                 header = ['home_team','away_team','date','time','ml_home_line','ml_home_trend','ml_away_line','ml_away_trend',
                                         'rl_home_line','rl_home_trend','rl_away_line','rl_away_trend',
                                         'tt_home_line','tt_home_trend','tt_away_line','tt_away_trend']
                 f.write(','.join(header)+'\n')
                 for table_row in table_rows:
                    f.write(','.join(teams)+','+','.join(table_row)+'\n')
        except AttributeError as e:
                print("Wrong Page\n")
                print(link)
if __name__ == '__main__':
    season = '2016'
    mois = range(4,12)
    for month in mois:
        for l in range(1,31):
            date = str(month).zfill(2)+'-'+str(l).zfill(2)+'-'+season
            parse_to_csv(date)