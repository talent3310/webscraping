import requests
from bs4 import BeautifulSoup
from splinter import Browser
from datetime import date
import time
from pandas import DataFrame
from selenium import webdriver
import re
import os 
import sys
import datetime
import os.path
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.ui import Select

result_sportsplay = []
result_vegas = []
name_sbr = [
    'Akron',
    'Alabama',
    'Alabama',
    'Alabama A&M',
    'Albany',
    'American University',
    'Appalachian State',
    'Appalachian State',
    'Arizona',
    'Arizona State',
    'Arkansas',
    'Arkansas State',
    'Arkansas-Little Rock',
    'Army',
    'Auburn',
    'Austin Peay',
    'Ball State',
    'Baylor',
    'Belmont',
    'Boise State',
    'Boston College',
    'Bowling Green',
    'Bradley',
    'Brown',
    'Bucknell',
    'Buffalo',
    'Butler',
    'BYU',
    'Cal Poly',
    'Cal State Bakersfield',
    'Cal State Fullerton',
    'Cal State Northridge',
    'California',
    'Canisius',
    'Central Connecticut State',
    'Central Michigan',
    'Chaminade University',
    'Charleston',
    'Charlotte',
    'Chattanooga',
    'Cincinnati',
    'Citadel',
    'Clemson',
    'Cleveland State',
    'Coastal Carolina',
    'Colorado',
    'Colorado State',
    'Columbia',
    'Connecticut',
    'Coppin State',
    'Cornell',
    'Creighton',
    'Dartmouth',
    'Davidson',
    'Dayton',
    'Delaware',
    'Denver',
    'DePaul',
    'Detroit',
    'Drexel',
    'Duke',
    'Duquesne',
    'East Carolina',
    'East Tennessee State',
    'Eastern Illinois',
    'Eastern Kentucky',
    'Eastern Michigan',
    'Eastern Washington',
    'Elon',
    'Evansville',
    'Fairfield',
    'Florida',
    'Florida Atlantic',
    'Florida Gulf Coast',
    'Florida International',
    'Florida State',
    'Fordham',
    'Fresno State',
    'Furman',
    'George Mason',
    'George Washington',
    'Georgetown',
    'Georgia',
    'Georgia Southern',
    'Georgia State',
    'Georgia Tech',
    'Gonzaga',
    'Grambling State',
    'Grand Canyon',
    'Green Bay',
    'Hartford',
    'Harvard',
    'Hawaii',
    'Hofstra',
    'Holy Cross',
    'Houston',
    'Howard',
    'Idaho',
    'Idaho State',
    'Illinois',
    'Illinois State',
    'Illinois-Chicago',
    'Indiana',
    'Indiana State',
    'Iona',
    'Iowa',
    'Iowa State',
    'IPFW',
    'IUPUI',
    'Jacksonville State',
    'James Madison',
    'Kansas',
    'Kansas State',
    'Kent State',
    'Kentucky',
    'La Salle',
    'Lafayette',
    'Lamar',
    'Long Beach State',
    'Longwood',
    'Louisiana Tech',
    'Louisiana-Monroe',
    'Louisville',
    'Loyola (IL)',
    'Loyola Marymount',
    'LSU',
    'Manhattan',
    'Marist',
    'Marquette',
    'Marshall',
    'Maryland',
    'Massachusetts',
    'Massachusetts Lowell',
    'Memphis',
    'Mercer',
    'Miami (FL)',
    'Miami (OH)',
    'Iowa State',
    'Michigan',
    'Michigan State',
    'Middle Tennessee',
    'Milwaukee',
    'Minnesota',
    'Mississippi State',
    'Missouri',
    'Missouri State',
    'Monmouth',
    'Montana',
    'Montana State',
    'Morehead State',
    'Murray State',
    'N.J.I.T.',
    'Navy',
    'Nebraska',
    'Nebraska-Omaha',
    'Nevada',
    'New Mexico',
    'New Mexico State',
    'Niagara',
    'Norfolk State',
    'North Carolina',
    'North Carolina Central',
    'North Carolina State',
    'North Carolina-Wilmington',
    'North Dakota State',
    'North Texas',
    'Northeastern',
    'Northern Arizona',
    'Northern Colorado',
    'Northern Illinois',
    'Northern Iowa',
    'Northern Kentucky',
    'Northwestern',
    'Northwestern State',
    'Notre Dame',
    'Oakland',
    'Ohio',
    'Ohio State',
    'Oklahoma',
    'Oklahoma State',
    'Old Dominion',
    'Ole Miss',
    'Oral Roberts',
    'Oregon',
    'Oregon State',
    'Pacific',
    'Penn State',
    'Pennsylvania',
    'Pepperdine',
    'Pittsburgh',
    'Portland',
    'Portland State',
    'Princeton',
    'Providence',
    'Purdue',
    'Quinnipiac',
    'Rhode Island',
    'Rice',
    'Richmond',
    'Rider',
    'Robert Morris',
    'Rutgers',
    'Sacramento State',
    'Sacred Heart',
    'Saint Louis',
    'Samford',
    'San Diego',
    'San Diego State',
    'San Francisco',
    'San Jose State',
    'Santa Clara',
    'Seattle',
    'Seton Hall',
    'Siena',
    'SIU-Edwardsville',
    'SMU',
    'South Alabama',
    'South Carolina',
    'South Dakota',
    'South Dakota State',
    'South Florida',
    'Southeast Missouri State',
    'Southern Illinois',
    'Southern Miss',
    'Southern Utah',
    'St. Bonaventure',
    'St. Francis (BKN)',
    "St. John's",
    "Saint Joseph's (PA)",
    'Stanford',
    'Stephen F. Austin',
    'Stony Brook',
    'Syracuse',
    'TCU',
    'Temple',
    'Tennessee',
    'Tennessee State',
    'Tennessee Tech',
    'Tennessee-Martin',
    'Texas',
    'Texas A&M',
    'Texas State',
    'Texas Tech',
    'Texas-Arlington',
    'Toledo',
    'Towson',
    'Troy',
    'Tulane',
    'Tulsa',
    'UAB',
    'UC Davis',
    'UC Irvine',
    'UC Riverside',
    'UC Santa Barbara',
    'UCF',
    'UCLA',
    'UMKC',
    'UNC Greensboro',
    'UNLV',
    'USC',
    'Utah',
    'Utah State',
    'UTEP',
    'UTSA',
    'Valparaiso',
    'Vanderbilt',
    'Vermont',
    'Villanova',
    'Virginia',
    'Virginia Military',
    'Virginia Tech',
    'Wake Forest',
    'Washington',
    'Washington State',
    'Weber State',
    'Western Carolina',
    'Western Illinois',
    'Western Kentucky',
    'Western Michigan',
    'Wichita State',
    'William & Mary',
    'Winthrop',
    'Wisconsin',
    'Wofford',
    'Wright State',
    'Wyoming',
    'Xavier',
    'Yale',
    'Youngstown State',
    'Virginia Commonwealth',
    'UMBC',
    'North Carolina A&T',
    'Southeastern Louisiana',
    'Sam Houston State',
    'Prairie View A&M',
    'Alaska Anchorage',
    'UNC Asheville',
    'Bryant University'
]
name_sportsplays = [
    'Akron Zips',
    'Alabama Crimson Tide',
    'Alabama Crimson Tide',
    'Alabama A&M Bulldogs',
    'Albany Great Danes',
    'American Eagles',
    'Akron Zips',
    'App State Mountaineers',
    'Arizona Wildcats',
    'Arizona State Sun Devils',
    'Arkansas Razorbacks',
    'Arkansas State Red Wolves',
    'Arkansas Little Rock Trojans',
    'Army Knights',
    'Auburn Tigers',
    'Austin Peay Governors',
    'Ball State Cardinals',
    'Baylor Bears',
    'Belmont Bruins',
    'Boise State Broncos',
    'Boston College Eagles',
    'Bowling Green Falcons',
    'Bradley Braves',
    'Brown Bears',
    'Bucknell Bison',
    'Buffalo Bulls',
    'Butler Bulldogs',
    'BYU Cougars',
    'Cal Poly SLO Mustangs',
    'CS Bakersfield Roadrunners',
    'Cal State Fullerton Titans',
    'CS Northridge Matadors',
    'California Golden Bears',
    'Canisius Golden Griffins',
    'C. Conn State. Blue Devils',
    'Central Michigan Chippewas',
    'Chaminade Silversword',
    'Charleston Cougars',
    'NC Charlotte 49ers',
    'UT Chattanooga Moccasins',
    'Cincinnati Bearcats',
    'The Citadel Bulldogs',
    'Clemson Tigers',
    'Cleveland State Vikings',
    'Coastal Carolina Chanticleers',
    'Colorado Buffaloes',
    'Colorado State Rams',
    'Columbia Lions',
    'Connecticut Huskies',
    'Coppin State Eagles',
    'Cornell Big Red',
    'Creighton Blue Jays',
    'Dartmouth Big Green',
    'Davidson Wildcats',
    'Dayton Flyers',
    'Delaware Blue Hens',
    'Denver University Pioneers',
    'Depaul Blue Demons',
    'Detroit Titans',
    'Drexel Dragons',
    'Duke Blue Devils',
    'Duquesne Dukes',
    'East Carolina Pirates',
    'E. Tenn State Buccaneers',
    'Eastern Illinois Panthers',
    'Eastern Kentucky Colonels',
    'Eastern Michigan Eagles',
    'Eastern Washington Eagles',
    'Elon College Phoenix',
    'Evansville Aces',
    'Fairfield Stags',
    'Florida Gators',
    'Florida Atlantic Owls',
    'Florida Gulf Coast Eagles',
    'Florida Intl Golden Panthers',
    'Florida State Seminoles',
    'Fordham Rams',
    'Fresno State Bulldogs',
    'Furman Paladins',
    'George Mason Patriots',
    'Geo Washington Colonials',
    'Georgetown Hoyas',
    'Georgia Bulldogs',
    'Georgia Southern Eagles',
    'Georgia State Panthers',
    'Georgia Tech Yellow Jackets',
    'Gonzaga Bulldogs',
    'Grambling State Tigers',
    'Grand Canyon Antelopes',
    'Wisconsin Green Bay Phoenix',
    'Hartford Hawks',
    'Harvard Crimson',
    'Hawaii Warriors',
    'Hofstra Pride',
    'Holy Cross Crusaders',
    'Houston Cougars',
    'Howard Bison',
    'Idaho Vandals',
    'Idaho State Bengals',
    'Illinois Fighting Illini',
    'Illinois State Redbirds',
    'Illinois Chicago Flames',
    'Indiana University Hoosiers',
    'Indiana State Sycamores',
    'Iona Gaels',
    'Iowa Hawkeyes',
    'Arizona State Sun Devils',
    'IPFW Mastadons',
    'IUPUI Jaguars',
    'Jacksonville St. Gamecocks',
    'James Madison Dukes',
    'Kansas Jayhawks',
    'Kansas State Wildcats',
    'Kent State Golden Flashes',
    'Kentucky Wildcats',
    'La Salle Explorers',
    'Lafayette Leopards',
    'Lamar Cardinals',
    'Long Beach State 49ers',
    'Longwood Lancers',
    'Louisiana Tech Bulldogs',
    'UL Monroe Warhawks',
    'Louisville Cardinals',
    'Loyola Chicago Ramblers',
    'Loyola Marymount Lions',
    'LSU Tigers',
    'Manhattan Jaspers',
    'Marist Red Foxes',
    'Marquette Golden Eagles',
    'Marshall Thundering Herd',
    'Maryland Terrapins',
    'Massachusetts Minutemen',
    'UMass-Lowell',
    'Memphis Tigers',
    'Mercer Bears',
    'Miami Hurricanes',
    'Miami Ohio Redhawks',
    'Iowa State Cyclones',
    'Michigan Wolverines',
    'Michigan State Spartans',
    'Mid Tenn State Blue Raiders',
    'Wisconsin Milwaukee Panthers',
    'Minnesota Golden Gophers',
    'Mississippi State Bulldogs',
    'Missouri Tigers',
    'Missouri State Bears',
    'Monmouth Hawks',
    'Montana Grizzlies',
    'Montana State Bobcats',
    'Morehead State Eagles',
    'Murray State Racers',
    'NJIT Highlanders',
    'Navy Midshipmen',
    'Nebraska Cornhuskers',
    'Nebraska Omaha Mavericks',
    'Nevada Wolf Pack',
    'New Mexico Lobos',
    'New Mexico State Aggies',
    'Niagara Purple Eagles',
    'Norfolk State Spartans',
    'North Carolina Tar Heels',
    'NC Central Eagles',
    'North Carolina State Wolfpack',
    'NC Wilmington Seahawks',
    'North Dakota State Bison',
    'North Texas Mean Green',
    'Northeastern Huskies',
    'N. Arizona Lumberjacks',
    'Northern Colorado Bears',
    'Northern Illinois Huskies',
    'Northern Iowa Panthers',
    'Northern Kentucky Norse',
    'Northwestern Wildcats',
    'Northwestern State Demons',
    'Notre Dame Fighting Irish',
    'Oakland Golden Grizzlies',
    'Ohio Bobcats',
    'Ohio State Buckeyes',
    'Oklahoma Sooners',
    'Oklahoma State Cowboys',
    'Old Dominion Monarchs',
    'Mississippi Rebels',
    'Oral Roberts Golden Eagles',
    'Oregon Ducks',
    'Oregon State Beavers',
    'Pacific Tigers',
    'Penn State Nittany Lions',
    'Pennsylvania Quakers',
    'Pepperdine Waves',
    'Pittsburgh Panthers',
    'Portland Pilots',
    'Portland State Vikings',
    'Princeton Tigers',
    'Providence Friars',
    'Purdue Boilermakers',
    'Quinnipiac Bobcats',
    'Rhode Island Rams',
    'Rice Owls',
    'Richmond Spiders',
    'Rider Broncs',
    'Robert Morris Colonials',
    'Rutgers Scarlet Knights',
    'Sacramento State Hornets',
    'Sacred Heart Pioneers',
    'Saint Louis Billikens',
    'Samford Bulldogs',
    'San Diego Toreros',
    'San Diego State Aztecs',
    'San Francisco Dons',
    'San Jose State Spartans',
    'Santa Clara Broncos',
    'Seattle Redhawks',
    'Seton Hall Pirates',
    'Siena Saints',
    'SIU Edwardsville Cougars',
    'SMU Mustangs',
    'South Alabama Jaguars',
    'South Carolina Gamecocks',
    'South Dakota Coyotes',
    'S. Dakota State Jack Rabbits',
    'South Florida Bulls',
    'SE Missouri State Redhawks',
    'Southern Illinois Salukis',
    'Southern Miss Golden Eagles',
    'Southern Utah Thunderbirds',
    'St. Bonaventure Bonnies',
    'St. Francis Terriers',
    "St. John's Red Storm",
    "St. Joseph's Hawks",
    'Stanford Cardinal',
    'Stephen F. Austin Lumberjacks',
    'Stony Brook Sea Wolves',
    'Syracuse Orange',
    'TCU Horned Frogs',
    'Temple Owls',
    'Tennessee Volunteers',
    'Tennessee State Tigers',
    'Tenn Tech Golden Eagles',
    'Tenn Martin Skyhawks',
    'Texas Longhorns',
    'Texas A&M Aggies',
    'Texas State Bobcats',
    'Texas Tech Red Raiders',
    'Texas Arlington Mavericks',
    'Toledo Rockets',
    'Towson State Tigers',
    'Troy Trojans',
    'Tulane Green Wave',
    'Tulsa Golden Hurricane',
    'UAB Blazers',
    'California Davis Aggies',
    'Cal Irvine Anteaters',
    'Cal Riverside Highlanders',
    'Santa Barbara Gauchos',
    'Central Florida Knights',
    'UCLA Bruins',
    'UMKC Kangaroos',
    'NC Greensboro Spartans',
    "UNLV Runnin' Rebels",
    'USC Trojans',
    'Utah Utes',
    'Utah State Aggies',
    'UTEP Miners',
    'TX San Antonio Roadrunners',
    'Valparaiso Crusaders',
    'Vanderbilt Commodores',
    'Vermont Catamounts',
    'Villanova Wildcats',
    'Virginia Cavaliers',
    'VMI Keydets',
    'Virginia Tech Hokies',
    'Wake Forest Demon Deacons',
    'Washington Huskies',
    'Washington State Cougars',
    'Weber State Wildcats',
    'Western Carolina Catamounts',
    'Western Illinois Leathernecks',
    'Western Kentucky Hilltoppers',
    'Western Michigan Broncos',
    'Wichita State Shockers',
    'William & Mary Tribe',
    'Winthrop Eagles',
    'Wisconsin Badgers',
    'Wofford Terriers',
    'Wright State Raiders',
    'Wyoming Cowboys',
    'Xavier Musketeers',
    'Yale Bulldogs',
    'Youngstown State Penguins',
    'VCU Rams',
    'UMBC Retrievers',
    'North Carolina A & T Aggies',
    'Southeastern Louisiana',
    'Sam Houston Bearkats',
    'Prairie View A&M Panthers',
    'Alaska Anch Seawolves',
    'NC Asheville Bulldogs',
    'Bryant Bulldogs'
]
name_vegas = [
    'Akron',
    'Alabama',
    'Alabama',
    'Alabama A&M',
    'Albany',
    'American University',
    'Appalachian State',
    'Appalachian State',
    'Arizona',
    'Arizona State',
    'Arkansas',
    'Arkansas State',
    'Arkansas-Little Rock',
    'Army',
    'Auburn',
    'Austin Peay',
    'Ball State',
    'Baylor',
    'Belmont',
    'Boise State',
    'Boston College',
    'Bowling Green',
    'Bradley',
    'Brown',
    'Bucknell',
    'SUNY-Buffalo',
    'Butler',
    'BYU',
    'Cal Poly',
    'Cal State Bakersfield',
    'CS Fullerton',
    'CS Northridge',
    'California',
    'Canisius',
    'Central Connecticut State',
    'Central Michigan',
    'Chaminade',
    'Charleston',
    'Charlotte',
    'Chattanooga',
    'Cincinnati',
    'Citadel',
    'Clemson',
    'Cleveland State',
    'Coastal Carolina',
    'Colorado',
    'Colorado State',
    'Columbia',
    'Connecticut',
    'Coppin State',
    'Cornell',
    'Creighton',
    'Dartmouth',
    'Davidson',
    'Dayton',
    'Delaware',
    'Denver',
    'DePaul',
    'Detroit',
    'Drexel',
    'Duke',
    'Duquesne',
    'East Carolina',
    'East Tennessee St.',
    'Eastern Illinois',
    'Eastern Kentucky',
    'Eastern Michigan',
    'Eastern Washington',
    'Elon',
    'Evansville',
    'Fairfield',
    'Florida',
    'Florida Atlantic',
    'Florida Gulf Coast',
    'Florida Intl',
    'Florida State',
    'Fordham',
    'Fresno State',
    'Furman',
    'George Mason',
    'George Washington',
    'Georgetown',
    'Georgia',
    'Georgia Southern',
    'Georgia State',
    'Georgia Tech',
    'Gonzaga',
    'Grambling State',
    'Grand Canyon',
    'Green Bay',
    'Hartford',
    'Harvard',
    'Hawaii',
    'Hofstra',
    'Holy Cross',
    'Houston',
    'Howard',
    'Idaho',
    'Idaho State',
    'Illinois',
    'Illinois State',
    'Illinois-Chicago',
    'Indiana',
    'Indiana State',
    'Iona',
    'Iowa',
    'Iowa State',
    'IUPU-Fort Wayne',
    'Indiana-Purdue',
    'Jacksonville State',
    'James Madison',
    'Kansas',
    'Kansas State',
    'Kent State',
    'Kentucky',
    'La Salle',
    'Lafayette',
    'Lamar',
    'CS Long Beach',
    'Longwood',
    'Louisiana Tech',
    'Louisiana-Monroe',
    'Louisville',
    'Loyola-Chicago',
    'Loyola-Marymount',
    'Louisiana State',
    'Manhattan',
    'Marist',
    'Marquette',
    'Marshall',
    'Maryland',
    'Massachusetts',
    'Massachusetts Lowell',
    'Memphis',
    'Mercer',
    'Miami (FL)',
    'Miami (OH)',
    'Miami (OH)',
    'Michigan',
    'Michigan State',
    'Middle Tennessee',
    'Milwaukee',
    'Minnesota',
    'Mississippi State',
    'Missouri',
    'Missouri State',
    'Monmouth',
    'Montana',
    'Montana State',
    'Morehead State',
    'Murray State',
    'New Jersey Tech',
    'Navy',
    'Nebraska',
    'Nebraska-Omaha',
    'Nevada',
    'New Mexico',
    'New Mexico State',
    'Niagara',
    'Norfolk State',
    'North Carolina',
    'North Carolina Central',
    'North Carolina State',
    'UNC Wilmington',
    'North Dakota State',
    'North Texas',
    'Northeastern',
    'Northern Arizona',
    'Northern Colorado',
    'Northern Illinois',
    'Northern Iowa',
    'Northern Kentucky',
    'Northwestern',
    'Northwestern State',
    'Notre Dame',
    'Oakland',
    'Ohio',
    'Ohio State',
    'Oklahoma',
    'Oklahoma State',
    'Old Dominion',
    'Mississippi',
    'Oral Roberts',
    'Oregon',
    'Oregon State',
    'Pacific',
    'Penn State',
    'Pennsylvania',
    'Pepperdine',
    'Pittsburgh',
    'Portland',
    'Portland State',
    'Princeton',
    'Providence',
    'Purdue',
    'Quinnipiac',
    'Rhode Island',
    'Rice',
    'Richmond',
    'Rider',
    'Robert Morris',
    'Rutgers',
    'CS Sacramento',
    'Sacred Heart',
    'St. Louis',
    'Samford',
    'San Diego',
    'San Diego State',
    'San Francisco',
    'San Jose State',
    'Santa Clara',
    'Seattle',
    'Seton Hall',
    'Siena',
    'SIU Edwardsville',
    'Southern Methodist',
    'South Alabama',
    'South Carolina',
    'South Dakota',
    'South Dakota State',
    'South Florida',
    'SE Missouri State',
    'Southern Illinois',
    'Southern Miss',
    'Southern Utah',
    'St. Bonaventure',
    'St. Francis (BKN)',
    "St. John's",
    "Saint Joseph's (PA)",
    'Stanford',
    'Stephen F. Austin',
    'Stony Brook',
    'Syracuse',
    'Texas Christian',
    'Temple',
    'Tennessee',
    'Tennessee State',
    'Tennessee Tech',
    'UT Martin',
    'Texas',
    'Texas AM',
    'Texas State',
    'Texas Tech',
    'Texas-Arlington',
    'Toledo',
    'Towson',
    'Troy',
    'Tulane',
    'Tulsa',
    'UAB',
    'UC Davis',
    'UC Irvine',
    'UC Riverside',
    'UC Santa Barbara',
    'Central Florida',
    'UCLA',
    'UMKC',
    'UNC Greensboro',
    'UNLV',
    'Southern Cal',
    'Utah',
    'Utah State',
    'UTEP',
    'Texas-San Antonio',
    'Valparaiso',
    'Vanderbilt',
    'Vermont',
    'Villanova',
    'Virginia',
    'Virginia Military',
    'Virginia Tech',
    'Wake Forest',
    'Washington',
    'Washington State',
    'Weber State',
    'Western Carolina',
    'Western Illinois',
    'Western Kentucky',
    'Western Michigan',
    'Wichita State',
    'William Mary',
    'Winthrop',
    'Wisconsin',
    'Wofford',
    'Wright State',
    'Wyoming',
    'Xavier',
    'Yale',
    'Youngstown State',
    'Virginia Commonwealth',
    'MD-Baltimore County',
    'North Carolina AT',
    'SE Louisiana',
    'Sam Houston State',
    'Prairie View AM',
    'Alaska-Anchorage',
    'UNC Asheville',
    'Bryant'
]


def soup_url(type_of_line, tdate=str(date.today()).replace('-', ''), driver=''):
    ## get html code for odds based on desired line type and date
    line_types = [('ML', 'money-line/'), ('RL', ''), ('total', 'totals/'), ('1H', '1st-half/'),
                  ('1HRL', 'pointspread/1st-half/'), ('1Htotal', 'totals/1st-half/')]
    url_addon = [lt[1] for num, lt in enumerate(line_types) if lt[0] == type_of_line][0]
    url = 'http://www.sportsbookreview.com/betting-odds/nfl-football/' + url_addon + '?date=' + tdate
    timestamp = time.strftime("%H:%M:%S")

    print(url);
    ## needs to run through line_movement_soup to get
    driver.get(url)

    print("----- kk ----------");
    soup_big = BeautifulSoup(driver.page_source, 'html.parser')
    soup = soup_big.find_all('div', id='OddsGridModule_16')[0]
    
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

    if(not os.path.isfile('sbr/SBR_NFL_' + season + '_' + game_date + '_line_moves.csv')):
        f = open('sbr/SBR_NFL_' + season + '_' + game_date + '_line_moves.csv', 'a')
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

            with open('sbr/SBR_NFL_' + season + '_' + game_date + '_line_moves.csv', 'a') as f:
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

        for key, item in enumerate(items):
            try:
                eventline = item.find_by_xpath('..').html
                soup = BeautifulSoup(eventline, 'html.parser')
                title = soup.find("meta", attrs={'itemprop': "name"})



                teams = title["content"].split('vs')
                eventid = soup.div['id']
                item.mouse_over()

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
                startTime = browser.find_by_xpath('//div[@id="time-' + eventid + '"]/div').html;
                print(startTime);
                # time = timeDiv.find('div', attrs={'class': "eventLine-book-value"}).text;
                # print(time);
                # print("time: " + time);

                # Get and click info button
                info = item.find_by_xpath('//div[@id="' + eventid + '"]/div/span[@class="info"]')
                count = 0
                while not info.visible:
                    time.sleep(1)
                    item.mouse_over()
                    if (count >= 10):
                        browser.execute_script("window.scrollBy(0, -40);")
                    count += 1
                info.click()
                time.sleep(2)
                event_box_header = browser.find_by_xpath("//div[@id='eventBox-" + eventid + "']/div/div/div[@class='event-menu-header']")
                time.sleep(1)


                print("---- 1 ----")

                if (len(event_box_header)>1): raise Exception
                while not event_box_header.first.visible:
                    time.sleep(1)
                consensus_link = browser.find_by_xpath("//div[@id='eventBox-" + eventid + "']/div/div/div[@class='event-menu-header']/a[contains(text(), 'Consensus')]").first
                time.sleep(1)
                # Finds consensus link
                while not consensus_link.visible:
                    time.sleep(1)

                print("---- 2 ----")
                consensus_link.click()
                time.sleep(2)
                consensus_data = browser.find_by_xpath('//*[@class="consensus"]')
                consensus_soup = BeautifulSoup(consensus_data.last.html, 'html.parser')
                consensus_types = consensus_soup.find_all('div', attrs={'class': "info-box"})
                print("---- 3 ----")
                for consensus_type in consensus_types:
                    header = consensus_type.find('div', attrs={'class': "header"}).text
                    data = consensus_type.find('table', attrs={'class': "data"})
                    print("---- 4 ----")

                    #############################################################################
                    # get short names
                    nameTable = consensus_type.find('table', attrs={'class': "thead-fixed"})

                    if (nameTable == None):
                        break;
                    nameTd = consensus_type.find_all('td', attrs={'class': 'header-grid'})

                    teamName_home = nameTd[1].text;
                    teamName_away = nameTd[2].text;
                    print("homeName: '" + teamName_home + "'");
                    print("awayName: '" + teamName_away + "'");


                    # print("name: " + shortName.html);
                    print("---- 4 - 1 ----")
                    # for shortName in shortNames:
                    #     print("name: " + shortName.html);

                    # teamName_home = shortNames[0].html
                    # teamName_away = shortNames[1].html

                    # print("homeName: '" + teamName_home + "'");
                    # print("awayName: '" + teamName_away + "'");

                    rows = []
                    if (data):
                        for i in data.find_all('tr'):

                            count = 0
                            for j in i.find_all('td'):
                                if (j.strong):
                                    percent = ''.join(j.strong.text.split())
                                    text = ''.join(j.text.split()).replace(u'\xa0', ' ').replace(u'\xbd', '.5')

                                    # row.append(text.replace(percent, ''))
                                    # row.append(percent)

                                    allText = ' '.join(j.text.split()).replace(u'\xa0', ' ').replace(u'\xbd', '.5')
                                    splitArray = allText.split()
                                    print("-- strong text kk ---->" + allText)
                                    print("-- strong text kk[0] ---->" + splitArray[0])
                                    # print("-- strong text kk -> len ---->" + len(splitArray))
                                    print(len(splitArray))
                                    print("-- strong text ---->" + text)
                                    print("-- strong ---->" + percent)

                                    if (count == 0):
                                        if (len(splitArray) == 3):
                                            spreadHome = splitArray[0]
                                        else:
                                            spreadHome = '0'
                                        percentHome = percent
                                    elif (count == 1):
                                        if (len(splitArray) == 3):
                                            spreadAway = splitArray[0]
                                        else:
                                            spreadAway = '0'
                                        percentAway = percent
                                    count = count + 1

                                elif (j.text):
                                    # row.append(j.text)
                                    print("-- text ---->" + j.text)


        # row = ['game_id', 'season', 'week', 'date', 
        #         'time', 'team', 'opponent_team', 'points', 
        #         'opponent_points', 'points_difference', 'spread', 'win_against_spread', 
        #         'spread_percentage_sbr', 'spread_percentage_sportsplays'] 


                            #########################################################
                            # add home row
                            row_home = ['', '', '', date,
                                    startTime, teamName_home_org, teamName_away_org, 
                                    teamName_home, teamName_away, scoreHome,
                                    scoreAway]

                            print("--- 22 ----")        
                            row_home.append(str(int(scoreHome) - int(scoreAway)))
                            print("--- 23 ----")        
                            row_home.append(spreadHome)
                            print("--- 24 ----")        
                            if (int(scoreHome) > int(scoreAway)):
                                row_home.append('1')
                            else:
                                row_home.append('0')
                            row_home.append(percentHome)
                            print("--- 25 ----")        
                            # row_home.append('')
                            print("--- 26 ----")        



                            #############################################################
                            # add away row


                            row_away = ['', '', '', date,
                                    startTime, teamName_away_org, teamName_home_org, 
                                    teamName_away, teamName_home, scoreAway,
                                    scoreHome]
                            print("--- 32 ----")        
                            row_away.append(str(int(scoreAway) - int(scoreHome)))
                            print("--- 33 ----")        
                            row_away.append(spreadAway)
                            if (int(scoreAway) > int(scoreHome)):
                                row_away.append('1')
                            else:
                                row_away.append('0')
                            print("--- 34 ----")        
                            row_away.append(percentAway)
                            print("--- 35 ----")        
                            # row_away.append('')


                            # get percent of sportsplays
                            # for k in range(0, len(result_sportsplay)):
                            #     one_sportsplay = result_sportsplay[k]
                            #     one_date = one_sportsplay[1]
                            #     one_time = one_sportsplay[2]
                            #     one_home = one_sportsplay[3]
                            #     one_away = one_sportsplay[4]
                            #     one_percent = one_sportsplay[5]


                            #     print(one_sportsplay)
                            #     print(one_date)
                            #     print(one_time)
                            #     print(one_home)
                            #     print(one_away)
                            #     print(one_percent)

                            #     print("--------");
                            #     print(teamName_home_org)
                            #     print(teamName_away_org)
                            #     print(date)
                            #     print(startTime)

                            #     if (one_home.find(teamName_away_org) != -1 and
                            #         one_away.find(teamName_home_org) != -1 and
                            #         one_date.find(date) != -1 and
                            #         one_time.find(startTime) != -1):
                            #         row_away.append(one_percent)
                            #         break

                            # add to rows
                            # rows.append(','.join(row_home))
                            # rows.append(','.join(row_away))
                            break
                        # with open('sbr/nfl_consensus_pick_all.csv', 'a') as f:
                        #     for i in rows:
                        #         f.write(i + '\n')
                        break
                    break


                consensus_types = consensus_soup.find_all('div', attrs={'class': "info-box"})

                # money lines
                if (consensus_types[1].find('table', attrs={'class': "thead-fixed"}) != None):
                    moneylineTds = consensus_types[1].find('tr', 'info_line_alternate1').find_all('td')

                    moneylineValue1 = moneylineTds[1].contents[0].replace(u'\xa0', ' ').replace(u'\xbd', '.5').split()[0]
                    moneylineValue2 = moneylineTds[2].contents[0].replace(u'\xa0', ' ').replace(u'\xbd', '.5').split()[0]
                    print(moneylineValue1)
                    print(moneylineValue2)
                    row_home.append(moneylineValue1)
                    row_home.append(moneylineValue2)
                    row_away.append(moneylineValue2)
                    row_away.append(moneylineValue1)
                else:
                    row_home.append("")
                    row_home.append("")
                    row_away.append("")
                    row_away.append("")                    

                # total
                if (consensus_types[2].find('table', attrs={'class': "thead-fixed"}) != None):
                    totalTds = consensus_types[2].find('tr', 'info_line_alternate1').find_all('td')

                    totalValue1 = totalTds[1].contents[0].replace(u'\xa0', ' ').replace(u'\xbd', '.5').split()[0]
                    totalValue2 = totalTds[2].contents[0].replace(u'\xa0', ' ').replace(u'\xbd', '.5').split()[0]
                    print(totalValue1)
                    print(totalValue2)
                    row_home.append(totalValue1)
                    row_home.append(totalValue2)
                    row_away.append(totalValue2)
                    row_away.append(totalValue1)
                else:
                    row_home.append("")
                    row_home.append("")
                    row_away.append("")
                    row_away.append("")

                # get percent of sportsplays
                for k in range(0, len(result_sportsplay)):
                    one_sportsplay = result_sportsplay[k]
                    one_date = one_sportsplay[1]
                    one_time = one_sportsplay[2]
                    one_home = one_sportsplay[3]
                    one_away = one_sportsplay[4]

                    one_pick = one_sportsplay[5]
                    one_percent = one_sportsplay[7]

                    # if (one_home.find(teamName_home_org) != -1 and
                    #     one_away.find(teamName_away_org) != -1 and
                    #     one_date.find(date) != -1 and
                    #     one_time.find(startTime) != -1):
                    #     row_home.append(one_percent)
                    #     break
                    if (one_home.find(teamName_home_org) != -1 and
                        one_away.find(teamName_away_org) != -1 and
                        one_date.find(date) != -1):
                        row_home.append(one_pick)
                        row_home.append(one_percent)
                        break
                # get percent of sportsplays
                for k in range(0, len(result_sportsplay)):
                    one_sportsplay = result_sportsplay[k]
                    one_date = one_sportsplay[1]
                    one_time = one_sportsplay[2]
                    one_home = one_sportsplay[3]
                    one_away = one_sportsplay[4]

                    one_pick = one_sportsplay[5]
                    one_percent = one_sportsplay[7]


                    # if (one_home.find(teamName_away_org) != -1 and
                    #     one_away.find(teamName_home_org) != -1 and
                    #     one_date.find(date) != -1 and
                    #     one_time.find(startTime) != -1):
                    #     row_away.append(one_percent)
                    #     break
                    if (one_home.find(teamName_away_org) != -1 and
                        one_away.find(teamName_home_org) != -1 and
                        one_date.find(date) != -1):
                        row_away.append(one_pick)
                        row_away.append(one_percent)
                        break


                # ========================================================================================
                # ????????????????????????????????????????????????????????????????????????????????????????????
                #  get spread percent of vegas of home team
                
                find = 0
                for vegas_item in result_vegas:
                    vegas_date = vegas_item[0] + vegas_item[1]
                    print(vegas_date)
                    vegas_spread = vegas_item[7]
                    print(vegas_spread)
                    print(vegas_item[11])

                    if (vegas_item[11] == teamName_home_org and
                        vegas_date.find(date) != -1):
                        row_home.append(vegas_spread)
                        find = 1
                        break
                        
                if find == 0:
                    row_home.append('NaN')
                #  get spread percent of vegas of away team
                print("vegas 2")
                find = 0
                for vegas_item in result_vegas:
                    vegas_date = vegas_item[0] + vegas_item[1]
                    vegas_spread = vegas_item[7]
                    if (vegas_item[11] == teamName_away_org and
                        vegas_date.find(date) != -1):
                        row_away.append(vegas_spread)
                        find = 1
                        break

                if find == 0:
                    row_away.append('NaN')
                print("\n===================================row home ========================\n")
                print(row_home)
                print("\n===================================row away ========================\n")
                print(row_away)
                # ????????????????????????????????????????????????????????????????????????????????????????????
                # ========================================================================================
                # add to rows
                rows.append(','.join(row_home))
                rows.append(','.join(row_away))
                with open('sbr/nfl_consensus_pick_all.csv', 'a') as f:
                    for i in rows:
                        f.write(i + '\n')


                time.sleep(1)
                print("---- 5 ----")
                lines += 1
                item.mouse_over()

                count = 0
                while not info.visible:
                    time.sleep(1)
                    item.mouse_over()
                    if (count >= 10):
                        browser.execute_script("window.scrollBy(0, -40);")
                    count += 1

                info.click()
                time.sleep(1)
                browser.execute_script("window.scrollBy(0, 40);")
            except:
                with open('sbr/nfl_consensus_pick_errors.csv','a') as f:
                    f.write(str(eventid) + " " + str(date))
                print("Consensus Error : " + str(eventid) + " " + str(date))

                time.sleep(1)
                print("---- 5 ----")
                lines += 1
                item.mouse_over()

                count = 0
                while not info.visible:
                    time.sleep(1)
                    item.mouse_over()
                    if (count >= 10):
                        browser.execute_script("window.scrollBy(0, -40);")
                    count += 1

                info.click()
                time.sleep(1)
                browser.execute_script("window.scrollBy(0, 40);")                   

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
        driver = webdriver.PhantomJS("C:\\siban_work\\environments\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")

        base_url = "http://www.sportsplays.com/consensus/NFL.html"
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
    header = ['srap_datetime','game_date','game_time','home','away', 'home_pick', 'away_pick', 'rl_home_percentage','rl_away_percentage']
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
                                row_values[4], row_values[5], row_values[6], row_values[7], row_values[8]]
            row_values_away = [row_values[0], row_values[1], row_values[2], row_values[4],
                                row_values[3], row_values[6], row_values[5], row_values[8], row_values[7]]
        # file_name = 'sportsplay/nfl_sportsplay_'+str(day_marker)+'.csv'
        file_name = 'sportsplay/nfl_sportsplay_pick.csv'

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
    
    for z in range(14, 20):
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
    # z = '13'
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


# =======================================================================================
# Functions for the vegas 
# -------------------------------------------------
result_vegas = []
#     return soup
def soup_url_vegas(week, year):
    url = 'http://www.vegasinsider.com/nfl/matchups/matchups.cfm/week/' + week +'/season/' + year
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
# Convert month name to number
def monthNametoNumber(mName):
    dict = {'Jan': '01', 'Feb': '02', 'Mar': '03','Apr': '04','May': '05','Jun': '06','Jul': '07','Aug': '08','Sep': '09','Oct': '10','Nov': '11','Dec': '12'}
    return dict[mName]
# Get date
def get_vegas(week, year):
    global result_vegas
    url = 'http://www.vegasinsider.com/nfl/matchups/matchups.cfm/week/' + week +'/season/' + year
    soup_total = BeautifulSoup(requests.get(url).text, 'html.parser')
    soup_mainParent = soup_total.find("td",attrs={'class':'main-content-cell'})
    soup_main = soup_mainParent.findChild('div',attrs={'id':'','class':'SLTables1'})
    soup_main_firstChild = soup_main.findChild('table')
    monthDay = '0'
    
    for tag in [soup_main_firstChild] + soup_main_firstChild.findNextSiblings():

        if tag.name =='table':
            dateInfoStrList = tag.strong.contents[0].split()           
            year = dateInfoStrList[5]
            month = monthNametoNumber(dateInfoStrList[3])
            day = dateInfoStrList[4]
            day = day[:-1]
            if len(day) == 1:
                day = '0' + day
            monthDay =  month + day
            pass
        elif tag.name == 'div' :
            className = ''
            try:
                className = tag.attrs['class'][0]
            except : 
                print('detected align attrs!')
                pass

            if className == 'SLTables1' :
                a = []
                uis = g(tag)[0]
            
                for bt_mouvment_page in get_games_links(uis):
                   
                    d =[]
                    d.append(year)
                    d.append(monthDay)
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
                    
                    # print(d);
                    if len(d) > 2:
                        
                        if len(d)== 10:
                            d.append('NaN')
                        print('result=> ',d )
                        if (len(d) == 13):
                            d.append('NaN')
                        a.append(','.join(d) + '\n')
                        #########################################
                        # add sbr name
                        nameBySbr = d[2]
                        for k in range(len(name_vegas)):
                            if name_vegas[k] == d[2]:
                                nameBySbr = name_sbr[k]
                                print(name_sbr[k])
                                break
                        d.append(nameBySbr)
                        
                        result_vegas.append(d)
                        
                        ##############################################

                        with open('vegas/ncaa_vegasinsider.csv', 'a') as t:

                            t.write(','.join(d) + '\n')

# Parse to csv file
def parse_to_csv_vegas(week, year):
    get_vegas(week, year)
    

# ==============================================================================================

if __name__ == '__main__':

    ##################################################
    # get vegas
    year = input("[VEGAS] Please type the year for which you would like to pull data (yyyy):")
    start_week = input("[VEGAS] Please type the starting month for which you would like to pull data (1-17):")
    numWeeks = input("[VEGAS] Please type the week numbers:")
    
    for i in range(int(start_week), int(start_week) + int(numWeeks)):
        parse_to_csv_vegas(str(i), str(year))


    #####################################################
    # get sportsplays

    start_year = input("Please type the year for which you would like to pull data (yyyy):")
    start_month = input("Please type the starting month for which you would like to pull data (1-12):")
    start_day = input("Please type the starting day for which you would like to pull data (1-31):")
    numdays = input("Please type the days for which you would like to pull data (1-365):")

    # numdays = 130
    base = datetime.datetime(int(start_year), int(start_month), int(start_day))
    date_list = [base + datetime.timedelta(days=x) for x in range(0, int(numdays))]


    for date_object in date_list:
        try:
            parse_to_csv(date_object)
        except AttributeError:
            print('wrong date'+str(date_object))
            pass


    #####################################################
    # get sbr


    season = str(input("Please type the year for which you would like to pull data (yyyy):"))
    start_month = input("Please type the starting month for which you would like to pull data (1-12):")
    end_month = input("Please type the last month for which you would like to pull data (1-12):")

    # driver = webdriver.PhantomJS()
    driver = webdriver.PhantomJS("C:\\siban_work\\environments\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")

    # to uitilize a headless driver, download and install phantomjs and use below to open driver instead of above line
    # download link -- http://phantomjs.org/download.html
    # driver = webdriver.PhantomJS(r"C:\Users\Monstar\Python\phantomjs-2.0.0\bin\phantomjs.exe")
    # 

    # add header
    row = ['game_id', 'season', 'week', 'date', 
            'time', 'team_org', 'opponent_team_org', 'team', 'opponent_team', 'points', 
            'opponent_points', 'points_difference', 'spread', 'win_against_spread', 
            'spread_percentage_sbr', 'moneyline_team', 'moneyline_opponent', 'total_team', 
            'total_opponent', 'pick_sportsplays', 'spread_percentage_sportsplays', 'vegas'] 
    join_row = ','.join(row)
    with open('sbr/nfl_consensus_pick_all.csv', 'a') as f:
        f.write(join_row + '\n')     

    # get all
    for y in range(int(start_month) - 1, int(end_month)):
        run_main(driver, season, y)
    # season = '2015'
    # main(driver, season, '20151105')
    driver.close()
