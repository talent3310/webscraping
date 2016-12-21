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

result_sportsplay = []

def soup_url(type_of_line, tdate=str(date.today()).replace('-', ''), driver=''):
    ## get html code for odds based on desired line type and date
    line_types = [('ML', 'money-line/'), ('RL', ''), ('total', 'totals/'), ('1H', '1st-half/'),
                  ('1HRL', 'pointspread/1st-half/'), ('1Htotal', 'totals/1st-half/')]
    url_addon = [lt[1] for num, lt in enumerate(line_types) if lt[0] == type_of_line][0]

    # url = 'http://www.sportsbookreview.com/betting-odds/nfl-football/' + url_addon + '?date=' + tdate
    url = 'http://www.sportsbookreview.com/betting-odds/ncaa-basketball/?date=' + tdate

    timestamp = time.strftime("%H:%M:%S")

    print(url);
    ## needs to run through line_movement_soup to get
    driver.get(url)

    print("----- kk ----------");
    soup_big = BeautifulSoup(driver.page_source, 'html.parser')
    soup = soup_big.find_all('div', id='OddsGridModule_14')[0]
    
    # if type_of_line == 'ML':
    #     line_movement_soup(soup, tdate, driver, 'Full Game')
    #     # Added method to get consensus of game
    #     write_consensus(url,tdate)
    if type_of_line == 'ML':
        # Added method to get consensus of game
        write_allinfo(url,tdate)    
    return soup, timestamp

def line_movement_soup(soup, game_date, driver, game_half):
    ############ only pull once for 1h and for full game, not 3 times
    book_list = [('238', 'Pinnacle'), ('19', '5Dimes'), ('999996', 'Bovada'), ('1096', 'BetOnline'),
                 ('169', 'Heritage')]

    eventlines = soup.find_all('div', {'class': 'el-div eventLine-book'})

    if(not os.path.isfile('sbr/SBR_NCAA_' + season + '_' + game_date + '_line_moves.csv')):
        f = open('sbr/SBR_NCAA_' + season + '_' + game_date + '_line_moves.csv', 'a')
        f.write('Date,Team,Opp,Bet_Length,Bet_Type,Line_Move_Time,Over_Under,Line,Odds')
        f.write('\n')
        f.close()

    for num in range(len(eventlines)):
        try:
            eventcode = eventlines[num]
            eventid = eventcode['id']
            book_id = eventid[[m.start() for m in re.finditer(r"-", eventid)][1] + 1:]
            if book_id in [tup[0] for pos, tup in enumerate(book_list)]:
                book_name = [tup[1] for pos, tup in enumerate(book_list) if tup[0] == book_id][0]

            ## Open popup
            driver.find_element_by_xpath("//div[@id='" + eventid + "']").find_element_by_class_name('eventLine-book-value ').find_element_by_xpath('b').click()

            ## Timer to let popup load
            time.sleep(1)
            wait_for_popup = True
            start_timer = time.time()
            while (wait_for_popup == True and time.time() - start_timer <= 10):
                popup_soup = BeautifulSoup(driver.page_source, 'html.parser')
                if len(popup_soup.find_all('div', attrs={'class': 'info-box'})) > 0:
                    wait_for_popup = False
                    break
                else:
                    print('sleep 1 more second')
                    time.sleep(1)

            all_line_changes = get_line_move_data(popup_soup, game_date, game_half, book_name)
            # Print statement wont print all eventlines because of the if statement
            print('writing ' + game_half + ' line movement -- ' + str(num + 1) + ' / ' + str(len(eventlines)))

            with open('sbr/SBR_NCAA_' + season + '_' + game_date + '_line_moves.csv', 'a') as f:
                all_line_changes.to_csv(f, index=False, header=False)

            ## CLose popup
            driver.find_element_by_xpath("//span[@class='ui-button-icon-primary ui-icon ui-icon-closethick']").click()

            time.sleep(1)
        except:
            print('Error with provider' + eventid)
            pass


def get_line_move_data(soup, game_date, game_half, book_name,line_change_list=[]):
    def prettify_odds(r, ha):
        ## input should be one or 2, depending on if i want away or home data
        ## Appends lines and odds to list to write to DF
        if t != 1:  # to split up odds and line
            d = row_data[ha].get_text().replace(u'\xa0', ' ').replace(u'\xbd', '.5')
            line = d[:d.index(' ')]
            odds = d[d.index(' ') + 1:]
            line_change_list.extend([line, odds])
        else:  # to only grab moneyline
            line = ''
            odds = row_data[ha].get_text()
            odds_trimmed = odds[odds.find('+') if odds.find('+') > 0 else odds.find('-'):]
            line_change_list.extend([line, odds_trimmed])

    df_line_moves = DataFrame(columns=(
        'Date', 'Book', 'Team', 'Opponent',  'Full or Half Game?', 'Line Type',
        'Time of Line Change', 'over.under', 'Line', 'Odds'))
    stats_tables = soup.find_all('div', attrs={'class': 'info-box'})
    num_tables = len(stats_tables)

    away_team = team_name_check(stats_tables[0].find_all('table')[0].find_all('tr')[0].find_all('td')[1].get_text())
    home_team = team_name_check(stats_tables[0].find_all('table')[0].find_all('tr')[0].find_all('td')[2].get_text())

    for t in range(num_tables):
        stats_table_name = stats_tables[t].find_all('div')[0].get_text()
        row = stats_tables[t].find_all('table')[1].find_all('tr')
        for r in reversed(range(len(row))):
            row_data = row[r].find_all('td')
            time_of_move = row_data[0].get_text()
            for dub in range(1, 3):
                line_change_list = []
                line_change_list.extend([game_date])
                line_change_list.extend([book_name])

                if dub == 1:
                    o_u_checker = 'over' if t == 2 else ''
                    line_change_list.extend([away_team, home_team])
                else:
                    o_u_checker = 'under' if t == 2 else ''
                    line_change_list.extend([home_team, away_team])
                line_change_list.extend([game_half, stats_table_name, time_of_move, o_u_checker])
                prettify_odds(row_data, dub)
                df_line_moves.loc[len(df_line_moves) + 1] = (
                    [line_change_list[j].replace(u'\xa0', ' ').replace(u'\xbd', '.5') for j in
                     range(len(line_change_list))])
    return df_line_moves


def parse_and_write_data(soup, date, time_of_move, not_ML=True):
    ## Parse HTML to gather line data by book
    '''
    using ['238','19','999996','1096','169']
    BookID  BookName
    238     Pinnacle
    19      5Dimes
    999996  Bovada
    1096    BetOnline
    169     Heritage
    93      Bookmaker
    123     BetDSI
    139     Youwager
    999991  SIA
    '''

    def book_line(book_id, line_id, homeaway):
        ## Get Line info from book ID
        try:
            lo0 = \
                soup.find_all('div', attrs={'class': 'el-div eventLine-book', 'rel': book_id})[line_id].find_all('div')[
                    homeaway].get_text().strip()
            lo1 = lo0.replace(u'\xa0', ' ').replace(u'\xbd', '.5')
            line = lo1[:lo1.find(' ')]
            odds = lo1[lo1.find(' ') + 1:]
        except IndexError:
            line = ''
            odds = ''
        return line, odds

    if not_ML:
        df = DataFrame(
            columns=('key', 'date', 'time', 'H/A',
                     'team',
                     'opp_team',
                     'pinnacle_line', 'pinnacle_odds',
                     '5dimes_line', '5dimes_odds',
                     'heritage_line', 'heritage_odds',
                     'bovada_line', 'bovada_odds',
                     'betonline_line', 'betonline_odds'))
    else:
        df = DataFrame(
            columns=('key', 'date', 'time', 'H/A',
                     'team',
                     'opp_team', 'pinnacle', '5dimes',
                     'heritage', 'bovada', 'betonline'))

    counter = 0
    number_of_games = len(soup.find_all('div', attrs={'class': 'el-div eventLine-rotation'}))
    # print 'number of games:' + str(number_of_games)

    for i in range(0, number_of_games):
        A = []
        H = []
        print(str(i + 1) + '/' + str(number_of_games))

        team_A = soup.find_all('div', attrs={'class': 'el-div eventLine-team'})[i].find_all('div')[0].get_text().strip()
        team_H = soup.find_all('div', attrs={'class': 'el-div eventLine-team'})[i].find_all('div')[1].get_text().strip()

        pinnacle_A_lines, pinnacle_A_odds = book_line('238', i, 0)
        fivedimes_A_lines, fivedimes_A_odds = book_line('19', i, 0)
        heritage_A_lines, heritage_A_odds = book_line('169', i, 0)
        bovada_A_lines, bovada_A_odds = book_line('999996', i, 0)
        betonline_A_lines, betonline_A_odds = book_line('1096', i, 0)

        pinnacle_H_lines, pinnacle_H_odds = book_line('238', i, 1)
        fivedimes_H_lines, fivedimes_H_odds = book_line('19', i, 1)
        heritage_H_lines, heritage_H_odds = book_line('169', i, 1)
        bovada_H_lines, bovada_H_odds = book_line('999996', i, 1)
        betonline_H_lines, betonline_H_odds = book_line('1096', i, 1)

        ## Edit team names to match personal preference
        team_H = team_name_check(team_H)
        team_A = team_name_check(team_A)

        A.append(str(date) + '_' + team_A.replace(u'\xa0', ' ') + '_' + team_H.replace(u'\xa0', ' '))
        A.extend([date, time_of_move, 'away', team_A, team_H])

        ## Account for runline and totals. Usually come in format '7 -110' or '-0.5 -110'.
        ## Use these if statements to separate line from odds
        if not_ML:
            ## write pinnacle data in list
            A.extend([pinnacle_A_lines, pinnacle_A_odds
                         , fivedimes_A_lines, fivedimes_A_odds
                         , heritage_A_lines, heritage_A_odds
                         , bovada_A_lines, bovada_A_odds
                         , betonline_A_lines, betonline_A_odds])
        else:
            ## write ML book data in list
            A.extend([pinnacle_A_odds
                         , fivedimes_A_odds
                         , heritage_A_odds
                         , bovada_A_odds
                         , betonline_A_odds])

        H.append(str(date) + '_' + team_A.replace(u'\xa0', ' ') + '_' + team_H.replace(u'\xa0', ' '))
        H.extend([date, time_of_move, 'home', team_H, team_A])
        if not_ML:
            ## write pinnacle data in list
            H.extend([pinnacle_H_lines, pinnacle_H_odds
                         , fivedimes_H_lines, fivedimes_H_odds
                         , heritage_H_lines, heritage_H_odds
                         , bovada_H_lines, bovada_H_odds
                         , betonline_H_lines, betonline_H_odds])
        else:
            ## write ML book data in list
            H.extend([pinnacle_H_odds
                         , fivedimes_H_odds
                         , heritage_H_odds
                         , bovada_H_odds
                         , betonline_H_odds])

        ## Write List (A & H) into dataframe
        df.loc[counter] = ([A[j] for j in range(len(A))])
        df.loc[counter + 1] = ([H[j] for j in range(len(H))])
        counter += 2

    return df


def select_and_rename(df, text):
    ## Select only useful column names
    ## Rename column names so that when merged, each df will be unique
    if text[-2:] == 'ml':
        df = df[['key', 'time', 'team', 'opp_team',
                 'pinnacle', '5dimes', 'heritage', 'bovada', 'betonline']]
        ## Change column names to make them unique
        df.columns = ['key', text + '_time', 'team', 'opp_team',
                      text + '_PIN', text + '_FD', text + '_HER', text + '_BVD', text + '_BOL']
    else:
        df = df[['key', 'time', 'team', 'opp_team',
                 'pinnacle_line', 'pinnacle_odds',
                 '5dimes_line', '5dimes_odds',
                 'heritage_line', 'heritage_odds',
                 'bovada_line', 'bovada_odds',
                 'betonline_line', 'betonline_odds']]
        df.columns = ['key', text + '_time', 'team','opp_team',
                      text + '_PIN_line', text + '_PIN_odds',
                      text + '_FD_line', text + '_FD_odds',
                      text + '_HER_line', text + '_HER_odds',
                      text + '_BVD_line', text + '_BVD_odds',
                      text + '_BOL_line', text + '_BOL_odds']
    return df


def team_name_check(team_name):
    new_team_name = 'LAD' if team_name == 'LA' else \
        'SDG' if team_name == 'SD' else \
            'SFO' if team_name == 'SF' else \
                'NYM' if team_name == 'NY' else \
                    'KCA' if team_name == 'KC' else \
                        'TBA' if team_name == 'TB' else \
                            'CHW' if team_name == 'CWS' else \
                                'CHC' if team_name == 'CHI' else \
                                    'WAS' if team_name == 'WSH' else \
                                        team_name

    return new_team_name


def write_consensus(url,date):
    # with Browser('firefox',fullscreen=True) as browser:
    # with Browser('firefox') as browser:
    with Browser('chrome') as browser:
        #url = "http://www.sportsbookreview.com/betting-odds/mlb-baseball/?date=" + date
        print('write_consensus');
        print(url);
        browser.visit(url)

        closeButton = browser.find_by_xpath("//div[contains(@class, 'x-container') and contains(@class, 'close')]");
        closeButton.click()

        items = browser.find_by_xpath('//div[@itemtype="http://schema.org/SportsEvent"]')
        lines = 0
        for key, item in enumerate(items):
            try:
                eventline = item.find_by_xpath('..').html
                soup = BeautifulSoup(eventline, 'html.parser')
                title = soup.find("meta", attrs={'itemprop': "name"})



                teams = title["content"].split('vs')
                eventid = soup.div['id']
                item.mouse_over()
                # Get and click info button
                info = item.find_by_xpath('//div[@id="' + eventid + '"]/div/span[@class="info"]')
                while not info.visible:
                    time.sleep(1)
                info.click()
                time.sleep(2)
                event_box_header = browser.find_by_xpath("//div[@id='eventBox-" + eventid + "']/div/div/div[@class='event-menu-header']")
                time.sleep(1)


                if (len(event_box_header)>1): raise Exception
                while not event_box_header.first.visible:
                    time.sleep(1)
                consensus_link = browser.find_by_xpath("//div[@id='eventBox-" + eventid + "']/div/div/div[@class='event-menu-header']/a[contains(text(), 'Consensus')]").first
                time.sleep(1)
                # Finds consensus link
                while not consensus_link.visible:
                    time.sleep(1)


                consensus_link.click()
                consensus_data = browser.find_by_xpath('//*[@class="consensus"]')
                time.sleep(2)
                consensus_soup = BeautifulSoup(consensus_data.first.html, 'html.parser')
                consensus_types = consensus_soup.find_all('div', attrs={'class': "info-box"})
                for consensus_type in consensus_types:
                    header = consensus_type.find('div', attrs={'class': "header"}).text
                    data = consensus_type.find('table', attrs={'class': "data"})
                    rows = []
                    if (data):
                        for i in data.find_all('tr'):
                            row = [header, date,teams[0], teams[1]]
                            for j in i.find_all('td'):
                                if (j.strong):
                                    percent = ''.join(j.strong.text.split())
                                    text = ''.join(j.text.split()).replace(u'\xa0', ' ').replace(u'\xbd', '.5')
                                    row.append(text.replace(percent, ''))
                                    row.append(percent)
                                elif (j.text):
                                    row.append(j.text)
                            rows.append('\001'.join(row))
                        with open('sbr/ncaa_movement.csv', 'a') as f:
                            for i in rows:
                                f.write(i + '\n')
                time.sleep(1)

                lines += 1
                item.mouse_over()
                while not info.visible:
                    time.sleep(1)
                info.click()
                time.sleep(1)
                browser.execute_script("window.scrollBy(0, 40);")
            except:
                with open('sbr/ncaa_consensus_errors.csv','a') as f:
                    f.write(str(eventid) + " " + str(date))
                print("Consensus Error : " + str(eventid) + " " + str(date))


def write_allinfo(url,date):
    # with Browser('firefox',fullscreen=True) as browser:
    # with Browser('firefox') as browser:
    with Browser('chrome') as browser:
        #url = "http://www.sportsbookreview.com/betting-odds/mlb-baseball/?date=" + date
        print('write_consensus');
        print(url);
        browser.visit(url)

        closeButton = browser.find_by_xpath("//div[contains(@class, 'x-container') and contains(@class, 'close')]");
        closeButton.click()

        items = browser.find_by_xpath('//div[@itemtype="http://schema.org/SportsEvent"]')
        lines = 0

        number = len(items)
        # for key, item in enumerate(items):
        for key in range(number):
            try:
                items = browser.find_by_xpath('//div[@itemtype="http://schema.org/SportsEvent"]')
                item = items[key]
                print("k-1")
                eventline = item.find_by_xpath('..').html
                print("k-2")
                soup = BeautifulSoup(eventline, 'html.parser')
                print("k-3")
                title = soup.find("meta", attrs={'itemprop': "name"})
                print("k-4")



                teams = title["content"].split('vs')
                eventid = soup.div['id']
                item.mouse_over()

                # # Get info button
                # info = item.find_by_xpath('//div[@id="' + eventid + '"]/div/span[@class="info"]')

                # count = 0
                # while not info.visible:
                #     time.sleep(1)
                #     item.mouse_over()
                #     if (count >= 10):
                #         browser.execute_script("window.scrollBy(0, -40);")
                #     count += 1                

                # get score of home and away
                scoreHome = browser.find_by_xpath('//span[@id="score-' + eventid + '-o"]').html;
                print("scoreHome: " + scoreHome)
                scoreAway = browser.find_by_xpath('//span[@id="score-' + eventid + '-u"]').html;
                print("scoreAway: " + scoreAway)

                # get home original name
                count = 0
                for k in browser.find_by_xpath('//div[@id="' + eventid + '"]/div[contains(@class, "el-div") and contains(@class, "eventLine-team")]/div[@class="eventLine-value"]/span[@class="team-name"]'):
                    if (count == 0):
                        teamName_home_org = k.text
                    elif (count == 1):
                        teamName_away_org = k.text
                    count = count + 1

                # get time
                startTime = browser.find_by_xpath('//div[@id="time-' + eventid + '"]/div').html
                print(startTime)

                # get "-" button
                time.sleep(1)
                eventDiv = item.find_by_xpath('//div[@id="' + eventid + '"]')
                minusButton = eventDiv.first.find_by_css('.scoreboxToggle')
                print("k-11")

                count = 0
                find = 1
                while not minusButton.first.visible:
                    time.sleep(1)
                    item.mouse_over()
                    if (count >= 10):
                        browser.execute_script("window.scrollBy(0, -40);")
                    if (count >= 20):
                        find = 0
                        break
                    count += 1 
                print("k-12")
                if (find == 1):
                    print("k-13")
                    minusButton.first.click()
                    time.sleep(1)

                # time = timeDiv.find('div', attrs={'class': "eventLine-book-value"}).text;
                # print(time);
                # print("time: " + time);

                #######################################################
                #                 pinnacle

                # get and click "pinnacle" button
                infoDiv = item.find_by_xpath('//div[@id="eventLine-' + eventid + '-238"]')
                print("k-5")
                while not infoDiv.visible:
                    time.sleep(1)
                infoDiv.click()
                time.sleep(4)

                print("k-6")

                spread_data = browser.find_by_xpath('//div[@id="dialogPop"]')
                spread_soup = BeautifulSoup(spread_data.last.html, 'html.parser')
                spread_types = spread_soup.find('div', attrs={'class': "info-box"})
                # get short names & point spreads
                nameTable = spread_types.find('table', attrs={'class': "thead-fixed"})
                if (nameTable != None):
                    nameTd = spread_types.find_all('td', attrs={'class': 'header-grid'})
                    teamName_home = nameTd[1].text;
                    teamName_away = nameTd[2].text;
                    print("homeName: '" + teamName_home + "'");
                    print("awayName: '" + teamName_away + "'");


                    spread_trs = spread_types.find_all('tr', attrs={'class': "info_line_alternate1"})
                    for spread_tr in spread_trs:
                        spread_tds = spread_tr.find_all('td')
                        updateTime = spread_tds[0].string
                        spreadTeam = spread_tds[1].string.replace(u'\xa0', ' ').replace(u'\xbd', '.5')
                        spreadOpponent = spread_tds[2].string.replace(u'\xa0', ' ').replace(u'\xbd', '.5')
                        print(updateTime)
                        print(spreadTeam)
                        print(spreadOpponent)
                        # add to rows
                        row_home = ['pinnacle', date, startTime,
                                    teamName_home_org, teamName_away_org, teamName_home, teamName_away,
                                    updateTime, spreadTeam, spreadOpponent]                         
                        rows = []
                        rows.append(','.join(row_home))
                        with open('sbr/ncaa_movement.csv', 'a') as f:
                            for i in rows:
                                f.write(i + '\n')


                # get and click "close" button
                closeButton = browser.find_by_xpath('//button[@title="close"]');
                while not closeButton.visible:
                    time.sleep(1)
                closeButton.click()
                time.sleep(2)

                #######################################################
                #                 bookmaker

                # get and click "bookmaker" button
                infoDiv = item.find_by_xpath('//div[@id="eventLine-' + eventid + '-93"]')
                while not infoDiv.visible:
                    time.sleep(1)
                infoDiv.click()
                time.sleep(4)

                spread_data = browser.find_by_xpath('//div[@id="dialogPop"]')
                spread_soup = BeautifulSoup(spread_data.last.html, 'html.parser')
                spread_types = spread_soup.find('div', attrs={'class': "info-box"})
                # get short names & point spreads
                nameTable = spread_types.find('table', attrs={'class': "thead-fixed"})
                if (nameTable != None):
                    nameTd = spread_types.find_all('td', attrs={'class': 'header-grid'})
                    teamName_home = nameTd[1].text;
                    teamName_away = nameTd[2].text;
                    print("homeName: '" + teamName_home + "'");
                    print("awayName: '" + teamName_away + "'");


                    spread_trs = spread_types.find_all('tr', attrs={'class': "info_line_alternate1"})
                    for spread_tr in spread_trs:
                        spread_tds = spread_tr.find_all('td')
                        updateTime = spread_tds[0].string
                        spreadTeam = spread_tds[1].string.replace(u'\xa0', ' ').replace(u'\xbd', '.5')
                        spreadOpponent = spread_tds[2].string.replace(u'\xa0', ' ').replace(u'\xbd', '.5')
                        print(updateTime)
                        print(spreadTeam)
                        print(spreadOpponent)      
                        # add to rows
                        row_home = ['bookmaker', date, startTime,
                                    teamName_home_org, teamName_away_org, teamName_home, teamName_away,
                                    updateTime, spreadTeam, spreadOpponent]                         
                        rows = []
                        rows.append(','.join(row_home))
                        with open('sbr/ncaa_movement.csv', 'a') as f:
                            for i in rows:
                                f.write(i + '\n')


                # get and click "close" button
                closeButton = browser.find_by_xpath('//button[@title="close"]');
                while not closeButton.visible:
                    time.sleep(1)
                closeButton.click()
                time.sleep(4)

                # #######################################################
                #                 bovada


                print("k-51")

                # get and click "bovada" button
                infoDiv = item.find_by_xpath('//div[@id="eventLine-' + eventid + '-999996"]')
                while not infoDiv.visible:
                    time.sleep(1)
                infoDiv.click()
                time.sleep(4)

                print("k-52")


                spread_data = browser.find_by_xpath('//div[@id="dialogPop"]')
                spread_soup = BeautifulSoup(spread_data.last.html, 'html.parser')
                spread_types = spread_soup.find('div', attrs={'class': "info-box"})
                # get short names & point spreads
                nameTable = spread_types.find('table', attrs={'class': "thead-fixed"})
                if (nameTable != None):
                    nameTd = spread_types.find_all('td', attrs={'class': 'header-grid'})
                    teamName_home = nameTd[1].text;
                    teamName_away = nameTd[2].text;
                    print("homeName: '" + teamName_home + "'");
                    print("awayName: '" + teamName_away + "'");


                    spread_trs = spread_types.find_all('tr', attrs={'class': "info_line_alternate1"})
                    for spread_tr in spread_trs:
                        spread_tds = spread_tr.find_all('td')
                        updateTime = spread_tds[0].string
                        spreadTeam = spread_tds[1].string.replace(u'\xa0', ' ').replace(u'\xbd', '.5')
                        spreadOpponent = spread_tds[2].string.replace(u'\xa0', ' ').replace(u'\xbd', '.5')
                        print(updateTime)
                        print(spreadTeam)
                        print(spreadOpponent)
                        # add to rows
                        row_home = ['bovada', date, startTime,
                                    teamName_home_org, teamName_away_org, teamName_home, teamName_away,
                                    updateTime, spreadTeam, spreadOpponent]                         
                        rows = []
                        rows.append(','.join(row_home))
                        with open('sbr/ncaa_movement.csv', 'a') as f:
                            for i in rows:
                                f.write(i + '\n')

                print("k-53")


                # get and click "close" button
                closeButton = browser.find_by_xpath('//button[@title="close"]');
                while not closeButton.visible:
                    time.sleep(1)
                closeButton.click()
                time.sleep(2)

                print("k-54")

                ######################################################
                #                sports interaction

                # get and click next button
                nextAnchor = browser.find_by_xpath('//a[@class="next"]')
                while not nextAnchor.visible:
                    time.sleep(1)
                nextAnchor.click()
                time.sleep(4)
                # nextAnchor.click()
                # time.sleep(2)



                # get and click "sports interaction" button
                print("k-541")                
                items = browser.find_by_xpath('//div[@itemtype="http://schema.org/SportsEvent"]')
                item = items[key]                
                infoDiv = item.find_by_xpath('//div[@id="eventLine-' + eventid + '-300"]')
                print("k-542")       
                while not infoDiv.visible:
                    time.sleep(1)
                infoDiv.click()
                time.sleep(4)

                spread_data = browser.find_by_xpath('//div[@id="dialogPop"]')
                spread_soup = BeautifulSoup(spread_data.last.html, 'html.parser')
                spread_types = spread_soup.find('div', attrs={'class': "info-box"})
                # get short names & point spreads
                nameTable = spread_types.find('table', attrs={'class': "thead-fixed"})
                if (nameTable != None):
                    nameTd = spread_types.find_all('td', attrs={'class': 'header-grid'})
                    teamName_home = nameTd[1].text;
                    teamName_away = nameTd[2].text;
                    print("homeName: '" + teamName_home + "'");
                    print("awayName: '" + teamName_away + "'");


                    spread_trs = spread_types.find_all('tr', attrs={'class': "info_line_alternate1"})
                    for spread_tr in spread_trs:
                        spread_tds = spread_tr.find_all('td')
                        updateTime = spread_tds[0].string
                        spreadTeam = spread_tds[1].string.replace(u'\xa0', ' ').replace(u'\xbd', '.5')
                        spreadOpponent = spread_tds[2].string.replace(u'\xa0', ' ').replace(u'\xbd', '.5')
                        print(updateTime)
                        print(spreadTeam)
                        print(spreadOpponent)
                        # add to rows
                        row_home = ['sports interaction', date, startTime,
                                    teamName_home_org, teamName_away_org, teamName_home, teamName_away,
                                    updateTime, spreadTeam, spreadOpponent]                         
                        rows = []
                        rows.append(','.join(row_home))
                        with open('sbr/ncaa_movement.csv', 'a') as f:
                            for i in rows:
                                f.write(i + '\n')


                # get and click "close" button
                closeButton = browser.find_by_xpath('//button[@title="close"]');
                while not closeButton.visible:
                    time.sleep(1)
                closeButton.click()
                time.sleep(2)


                print("k-55")

                # get and click prev button
                prevAnchor = browser.find_by_xpath('//a[@class="prev"]')
                while not prevAnchor.visible:
                    time.sleep(1)
                prevAnchor.click()
                time.sleep(2)
                # prevAnchor.click()
                # time.sleep(2)



                print("k-56")                


                time.sleep(1)
                print("---- 5 ----")
                lines += 1
                # item.mouse_over()
                # while not info.visible:
                #     time.sleep(1)
                # info.click()
                # time.sleep(1)
                browser.execute_script("window.scrollBy(0, 40);")
                print("---- 6 ----")
            except:
                with open('sbr/ncaa_consensus_errors.csv','a') as f:
                    f.write(str(eventid) + " " + str(date))
                print("Consensus Error : " + str(eventid) + " " + str(date))

                # get and click "close" button
                count = 0
                find = 1
                closeButton = browser.find_by_xpath('//button[@title="close"]');
                while not closeButton.visible:
                    time.sleep(1)
                    count = count + 1
                    if (count > 5):
                        find = 0
                        break
                if (find == 1):
                    closeButton.click()
                time.sleep(2)

                ##########
                time.sleep(1)
                print("---- 5 ----")
                lines += 1
                
                browser.execute_script("window.scrollBy(0, 40);")     
                #####################

def main(driver, season, inputdate=str(date.today()).replace('-', '')):
    ## Get today's lines
    todays_date = str(date.today()).replace('-', '')
    todays_date = inputdate

    ## store BeautifulSoup info for parsing
    print("getting today's MoneyLine (1/6)")
    soup_ml, time_ml = soup_url('ML', todays_date, driver)

    # print("getting today's RunLine (2/6)")
    # soup_rl, time_rl = soup_url('RL', todays_date, driver)

    # print("getting today's totals (3/6)")
    # soup_tot, time_tot = soup_url('total', todays_date,driver)

    # ## Parse and Write
    # print("writing today's MoneyLine (1/6)")
    # df_ml = parse_and_write_data(soup_ml, todays_date, time_ml, not_ML=False)
    # ## Change column names to make them unique
    # df_ml.columns = ['key', 'date', 'ml_time', 'H/A', 'team', 'opp_team',
    #                  'ml_PIN', 'ml_FD', 'ml_HER', 'ml_BVD', 'ml_BOL']

    # print("writing today's RunLine (2/6)")
    # df_rl = parse_and_write_data(soup_rl, todays_date, time_rl)
    # df_rl = select_and_rename(df_rl, 'rl')

    # print("writing today's totals (3/6)")
    # df_tot = parse_and_write_data(soup_tot, todays_date, time_tot)
    # df_tot = select_and_rename(df_tot, 'tot')

    # ## Write to Dataframes
    # write_df = df_ml
    # write_df = write_df.merge(
    #     df_rl, how='left', on=['key', 'team', 'opp_team'])
    # write_df = write_df.merge(
    #     df_tot, how='left', on=['key', 'team', 'opp_team'])

    # ## Write to txt

    # with open('sbr/SBR_NFL_Closing_Lines_' + season + '_' + todays_date + '.csv', 'a') as f:
    #     write_df.to_csv(f, index=False, header=True)

def send_request(date):
    try:
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap[
            "phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 (KHTML, like Gecko) Chrome/15.0.87"
        service_args = [
            '--proxy=127.0.0.1:9050',
            '--proxy-type=socks5']
        # driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=service_args)
        driver = webdriver.PhantomJS("C:\\Users\\worri\\AppData\\Local\\Programs\\Python\\Python35-32\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")

        base_url = "http://www.sportsplays.com/consensus/cbb.html"
        driver.get(base_url)
        # Choose date in menu
        Select(driver.find_element_by_id("from_date_day")).select_by_value(str(date.day))
        Select(driver.find_element_by_id("from_date_month")).select_by_value(str(date.month))
        Select(driver.find_element_by_id("from_date_year")).select_by_value(str(date.year))
        driver.find_element_by_name("commit").click()
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        return soup
    except requests.exceptions.RequestException:
        print('HTTP Request failed')

def parse_to_csv(date):
    global result_sportsplay
    header = ['srap_datetime','game_date','game_time','home','away','rl_home_percentage','rl_away_percentage']
    soup = send_request(date)
    day_marker = str(datetime.datetime.today().month) + str(datetime.datetime.today().day)
    table = soup.find('table',attrs={'id':'consensus_events'})
    rows = table.find_all('tr')
    # for each row find by cell all divs inside
    for row in rows:

        day = ('0' if len(str(date.day)) == 1 else '') + str(date.day)
        month = ('0' if len(str(date.month)) == 1 else '') + str(date.month)
        year = ('0' if len(str(date.year)) == 1 else '') + str(date.year)

        row_values = [str(datetime.datetime.today()), year + month + day]
        for td in row.find_all('td'):
            for div in td.find_all('div'):
                if(div.string): 
                    row_values.append(' '.join(div.string.split()))
                    div.string.split()
                elif(div.font): 
                    row_values.append(' '.join(div.font.string.split()))
        if (len(row_values[2:])>0):
            # get home name
            splits = row_values[3].split()
            splits_name = []
            for k in range(1, len(splits)):
                splits_name.append(splits[k])
            row_values[3] = ' ' . join(splits_name)
            # replace 'New York' with 'N.Y.' 
            row_values[3] = row_values[3].replace("New York", "N.Y.")
            # replace 'St. Louis Rams' with 'Los Angeles'
            row_values[3] = row_values[3].replace("St. Louis Rams", "Los Angeles")

            # get away name
            splits = row_values[4].split()
            splits_name = []
            for k in range(1, len(splits)):
                splits_name.append(splits[k])
            row_values[4] = ' ' . join(splits_name)
            # replace 'New York' with 'N.Y.' 
            row_values[4] = row_values[4].replace("New York", "N.Y.")
            # replace 'St. Louis Rams' with 'Los Angeles'
            row_values[4] = row_values[4].replace("St. Louis Rams", "Los Angeles")

            row_values_home = [row_values[0], row_values[1], row_values[2], row_values[3],
                                row_values[4], row_values[7], row_values[8]]
            row_values_away = [row_values[0], row_values[1], row_values[2], row_values[4],
                                row_values[3], row_values[8], row_values[7]]
        # file_name = 'sportsplay/nfl_sportsplay_'+str(day_marker)+'.csv'
        file_name = 'sportsplay/ncaa_sportsplay.csv'

        with open(file_name,'a') as f:
            if(os.stat(file_name).st_size == 0):
                f.write(','.join(header)+'\n')
            if(len(row_values[2:])>0): 
                f.write(','.join(row_values_home)+'\n')
                f.write(','.join(row_values_away)+'\n')
        if(len(row_values[2:])>0):                
            result_sportsplay.append(row_values_home)
            result_sportsplay.append(row_values_away)


def run_main(driver, season, month=1):
    bad_games = []
    ## Get number of days in a month
    month = int(month)

    # days_in_month = 31 if (
    #     month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12) else 30

    days_in_month = 31 if (
        (month + 1) == 1 or (month + 1) == 3 or (month + 1) == 5 or (month + 1) == 7 or (month + 1) == 8 or (month + 1) == 10 or (month + 1) == 12) else 30
    ## Convert month to two characters
    month = ('0' if len(str(month + 1)) == 1 else '') + str(month + 1)

    print("days")
    print(days_in_month);
    
    for z in range(days_in_month):
        z = ('0' if len(str(z + 1)) == 1 else '') + str(z + 1)
        lookupdate = season + month + z
        print(lookupdate)
        try:
            main(driver, season, lookupdate)
        except IndexError:
            f = open('sbr/SBR_MLB_Lines_bad_games.txt', "a")
            f.write(lookupdate + '\n')
            f.close()
            print()
            print('bad game -- ' + lookupdate)
            print()
            pass

    # z = '11'
    # lookupdate = season + month + z
    # print(lookupdate)
    # try:
    #     main(driver, season, lookupdate)
    # except IndexError:
    #     f = open('sbr/SBR_MLB_Lines_bad_games.txt', "a")
    #     f.write(lookupdate + '\n')
    #     f.close()
    #     print()
    #     print('bad game -- ' + lookupdate)
    #     print()
    #     pass            

if __name__ == '__main__':

    #####################################################
    # get sportsplays

    # start_year = input("Please type the year for which you would like to pull data (yyyy):")
    # start_month = input("Please type the starting month for which you would like to pull data (1-12):")
    # start_day = input("Please type the starting day for which you would like to pull data (1-31):")
    # numdays = input("Please type the days for which you would like to pull data (1-365):")

    # # numdays = 130
    # base = datetime.datetime(int(start_year), int(start_month), int(start_day))
    # date_list = [base + datetime.timedelta(days=x) for x in range(0, int(numdays))]


    # for date_object in date_list:
    #     try:
    #         parse_to_csv(date_object)
    #     except AttributeError:
    #         print('wrong date'+str(date_object))
    #         pass


    #####################################################
    # get sbr


    season = str(input("Please type the year for which you would like to pull data (yyyy):"))
    start_month = input("Please type the starting month for which you would like to pull data (1-12):")
    end_month = input("Please type the last month for which you would like to pull data (1-12):")

    # driver = webdriver.PhantomJS()
    driver = webdriver.PhantomJS("C:\\Users\\worri\\AppData\\Local\\Programs\\Python\\Python35-32\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")

    # to uitilize a headless driver, download and install phantomjs and use below to open driver instead of above line
    # download link -- http://phantomjs.org/download.html
    # driver = webdriver.PhantomJS(r"C:\Users\Monstar\Python\phantomjs-2.0.0\bin\phantomjs.exe")
    # 

    # add header
    row = [ 'casinoName', 'date', 'starttime',
            'team_org', 'opponent_team_org', 'team', 'opponent_team', 
            'updateTime', 'spreadTeam', 'spreadOpponent'
            ] 
    join_row = ','.join(row)
    with open('sbr/ncaa_movement.csv', 'a') as f:
        f.write(join_row + '\n')     

    # get all
    for y in range(int(start_month) - 1, int(end_month)):
        run_main(driver, season, y)
    # season = '2015'
    # main(driver, season, '20151105')
    driver.close()
