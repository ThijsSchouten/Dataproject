# Name: Thijs Schouten
# Student number: 10887679

'''
This script crawls regatta data from TIME-TEAM.nl
'''

# Python library imports
import csv

# Third party library imports:
import pattern
from pattern.web import Element, URL, DOM, abs, plaintext

# Constants:
REGATTA_URL = 'http://regatta.time-team.nl/nsrf/2014/results/matrix.php'

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

def save_heat_urls(regatta_url, regatta_dom):
    
    heat_urls = []

    for link in regatta_dom('a'):
        temp = abs(link.attributes.get('href',''), base=regatta_url.redirect
                or regatta_url.string)
        if temp [-7:-4].isdigit() == True:
            heat_urls.append(temp)

    return heat_urls

def scrape_heat_page(heat_url):
    url = URL(heat_url)
    dom = DOM(url.download(cached=True))

    for results in dom.by_tag('container'):
        print results




def main():
    '''
    '''

    print 'Get Regatta URL .. '
    url = URL(REGATTA_URL)
    dom = DOM(url.download(cached=True))
    print '.. check'

    print 'Get Heat URLs .. '
    heat_urls = save_heat_urls(url, dom)
    print '.. check'

    print 'Scrape heat page .. '
    for heat in heat_urls[-1:]:
        scrape_heat_page(heat)
    print '.. check'


if __name__ == '__main__':
    main() 
