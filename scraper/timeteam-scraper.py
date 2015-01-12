# Name: Thijs Schouten
# Student number: 10887679

'''
This script scrapes regatta data from TIME-TEAM.nl
'''

# --------------------------------------------------------------------------
# Libraries

# Python library imports
import csv

# Third party library imports:
import pattern
from pattern.web import Element, URL, DOM, abs, plaintext

# --------------------------------------------------------------------------
# Constant

REGATTA_URL = 'http://regatta.time-team.nl/hollandbeker/2014/results/matrix.php'

# --------------------------------------------------------------------------
# Utility functions

def save_csv(filename, rows):
    '''
    Args:
        filename: string filename for the CSV file
        rows: list of rows to be saved 
    '''
    with open(filename, 'wb') as f:
        writer = UnicodeWriter(f)  # implicitly UTF-8
        writer.writerow([
            'regatta', 'field', 'position', 
        ])

        writer.writerows(rows)

# unicode handler?

# --------------------------------------------------------------------------
# Scraping

def save_heat_urls(regatta_url, regatta_dom):
    
    heat_urls = []

    for link in regatta_dom('a'):
        temp = abs(link.attributes.get('href',''), base=regatta_url.redirect
                or regatta_url.string)
        if temp [-7:-4].isdigit() == True:
            heat_urls.append(temp)

    return heat_urls

def scrape_heat_page(heat_url):
    '''
    return stats about races, including:
    race stat (pre-final/a-final/b-final etc)
    club
    position
    names
    lane
    500m time
    1000m time
    1500m time
    2000m time
    promotie

    '''
    url = URL(heat_url)
    dom = DOM(url.download(cached=True))


    regatta_title = ''
    heat_time = ''
    position = ''
    crew_code = ''
    lane = ''
    five_time = ''
    five_pos = ''
    ten_time = ''
    ten_pos = ''
    fifteen_time = ''
    fifteen_pos = ''
    twenty_time = ''
    twenty_pos = ''
    promotie = ''

    for title in dom.by_tag('title'):
        regatta_title = plaintext(title.content)[:-12]

    print '' 

    for i in range(0,len(dom.by_tag('h2'))): # for every heat
    #for i in range(0,1):

        print ''

        for header in dom.by_tag('h2')[i:i+1]:
            heat_time = header.content[0:8] # heat timestamp 
            heat_title = header.content[11:] # heat title
            print regatta_title, '| Heat Title:', heat_title, '| Day/Time:', heat_time


        for web_table in dom('.timeteam')[i:i+1]:
            for row in web_table('tr')[1::2]: 
                try: 
                    if (row('td')[0].content[:-1]).isdigit() == True:
                     
                        position = row('td')[0].content
                        crew_code = plaintext(row('td')[1].content)
                        lane = row('td')[3].content
                        five_time = row('td')[4].content
                        five_pos = row('td')[5].content
                        ten_time = row('td')[6].content
                        ten_pos = row('td')[7].content
                        fifteen_time = row('td')[8].content
                        fifteen_pos = row('td')[9].content
                        twenty_time = row('td')[10].content
                        twenty_pos = row('td')[11].content

                    #for cell in row('td')[2]: # crew names
                    #    pass
                except IndexError:
                    print 'IndexError'


                print crew_code, '| position:', position, '| lane:', lane, \
                        '| 500m time/pos:', five_time, five_pos, \
                        '| 1000m time/pos:', ten_time, ten_pos, \
                        '| 1500m time/pos:', fifteen_time, fifteen_pos, \
                        '| 2000m time/pos:', twenty_time, twenty_pos, \
                        ''


                
            

    print '' 

# --------------------------------------------------------------------------
# Main 

def main():
    '''
    '''

    print 'Dom from Regatta URL .. '
    url = URL(REGATTA_URL)
    dom = DOM(url.download(cached=True))
    print '.. check'

    print 'Get Heat URLs .. '
    heat_urls = save_heat_urls(url, dom)
    print '.. check'

    print 'Scrape heat page .. '
    for heat in heat_urls:
        scrape_heat_page(heat)
    print '.. check'


if __name__ == '__main__':
    main() 
