# Name: Thijs Schouten
# Student number: 10887679

'''
This script scrapes regatta data from TIME-TEAM.nl
'''

# --------------------------------------------------------------------------
# Libraries

# Python library imports
import csv
import json

# Third party library imports:
import pattern
from pattern.web import Element, URL, DOM, abs, plaintext

# --------------------------------------------------------------------------
# Constant

REGATTA_URL = 'http://regatta.time-team.nl/nsrf/2014/results/matrix.php'


# --------------------------------------------------------------------------
# Scraping

def scrape_heat_urls(regatta_url, regatta_dom):
    
    # create list to store heat urls
    heat_urls = []

    for link in regatta_dom('a'):
        temp = abs(link.attributes.get('href',''), base=regatta_url.redirect
                or regatta_url.string)
        if temp [-7:-4].isdigit() == True:
            heat_urls.append(temp)

    return heat_urls

def scrape_names_page(name_url):

    #print name_url

    #var to store names
    names = []

    #create dom format from URL
    url = URL(name_url)
    dom = DOM(url.download(cached=True))

    # 
    for tr in dom('tr')[1:]:
        if "slag" in tr[0].content:
            names.append(tr[1].content)
            break
        else:
            names.append(tr[1].content)

    return names

def scrape_heat_page(heat_url):
    '''
    Return heat data with stats about races, including:
    (pre-final/a-final/b-final etc), club, finishposition, lane, 500m time, 
    1000m time, 1500m time, 2000m time,

    return type: [heat_title, participants_dict, heat_time]
    @ heat title = the name of the field
    @ participants_dict is a dict containing data about the participants
    @ heat time = time the heat took place
    @ heat type = ex. 'voorwedstrijd' or 'a-final'
    '''

    participants_dict = {}
    heat_title = '' 
    heat_type = ''

    #save
    url = URL(heat_url)
    dom = DOM(url.download(cached=True))

    #for i in range(0,len(dom.by_tag('h2'))): # for every heat

    i = 0

    for web_table in dom('.timeteam'):

        # dictionary to store crews
        crews_dict = {}
        # list to store 

        #print i
        #header = dom.by_tag('h2')[i]
        #i = i + 1                      

        #header_data = mapping(header.content)

        #heat_time = header_data[0] # heat timestamp 
        #heat_title = header_data[1] # heat title
        #heat_type = header_data[2]

        #print header_data
            
        regatta_participants = []

        for row in web_table('tr')[1::2]: # take each second row after 1
    
            try: 
                if (row('td')[0].content[:-1]).isdigit() == True:
                    print "OK"

                    #create dictionary to store crew info 
                    #add all variables to dict                               
                    crew_dict = {}
                    crew_dict["position"] = row('td')[0].content                                      
                    crew_dict["crew_code"] = plaintext(row('td')[1]\
                                            .content)
                    crew_dict["lane"] = row('td')[3].content
                    crew_dict["five_time"] = row('td')[4].content
                    crew_dict["five_pos"] = row('td')[5].content
                    crew_dict["ten_time"] = row('td')[6].content
                    crew_dict["ten_pos"] = row('td')[7].content
                    crew_dict["fifteen_time"] = row('td')[8].content
                    crew_dict["fifteen_pos"] = row('td')[9].content
                    crew_dict["twenty_time"] = row('td')[10].content
                    crew_dict["twenty_pos"] = row('td')[11].content


                    dom = DOM(row('td')[2])

                    for a in dom('a'):
                        names_url = abs(a.attributes.get('href',''), base=url.redirect or url.string)

                    crew_dict["Names"] = scrape_names_page(names_url)



                    regatta_participants.append(crew_dict)

            except IndexError:
                print row                              
                print 'IndexError'

        participants_dict = regatta_participants

    print participants_dict

    return [heat_title, participants_dict, heat_time, heat_type]

def mapping(input_title):
    heatnames = ["Meisjes", "Jongens", "Corp", "LDDev",\
                 "DDev", "LDev", "LDSA", "LDSB", "LDEj", "HTal", "DTal", \
                 "LSA", "LSB", "DSA", "LDO", "LDN", "LDB", "J18", "J16", "M18",\
                 "M16", "Dev", "LEj", "DEj",\
                 "LB", "LN", "DN", "DB", "DO", "LO", "Ej", "SA", "SB",\
                 "O", "N", "B"]  

    boattypes = ["8+", "4+", "4-", "4*", "4x", "2x", "2-", "2+", "1x", "acht"]

    heattypes_F = ["A-finale", "B-finale", "C-finale", "D-finale", "E-finale"]

    heattypes_H = ["voorwedstrijd", "heat"]

    time = input_title[0:9] # will find Sat 10:40 as well as Za 10:40
                            # strip trailing whitespace?
    title = 'x'
    boat = 'x'
    heat = 'x' 

    for heatname in heatnames:
        if heatname in input_title:
            title = heatname
            break

    for heattype in heattypes_F:
        if heattype in input_title:
            heat = "Final"
            break

    for heattype in heattypes_H:
        if heattype in input_title:
            heat = "Heat"
            break

    for boattype in boattypes:
        if boattype in input_title:
            boat = boattype 
            break

    # If heattype is not specified, assume it is a final
    if heat is 'x':
        heat = "Final"

    # Check boat values:
    if boat is 'x':
        print "Fault in boattype, input is:", input_title
        print "output boattype is:", boat

    # Check title values:
    if title is 'x':
        print "Fault in title, input is:", input_title
        print "output title is:", title

    #print input_title, ">> TIME:", time, "BOAT:", boat, "TITLE:", title,\
    #       "HEAT:", heat

    return [time, title+" "+boat, heattype]


# --------------------------------------------------------------------------
# Main 

def main():
    '''
    '''

    # Create dict to store regatta data in
    regatta_dict = {}
    # Create dict to store all heats in
    regatta_heats = {}

    # Create DOM from regatta URL
    url = URL(REGATTA_URL)
    dom = DOM(url.download(cached=True))
    
    # Add metadata to dictionary
    for title in dom.by_tag('title'):
        regatta_title = plaintext(title.content)[:-12]

    regatta_dict["id"] = regatta_title
    regatta_dict["date"] = "05/07/2014"

    # Fetch heat urls
    heat_urls = scrape_heat_urls(url, dom) 

    # Save data for every heat
    for heat in heat_urls[44:45]:
        temp_heat_data = scrape_heat_page(heat)

        temp_participants_dict = {}
        temp_participants_dict["Type"] = temp_heat_data[3]
        temp_participants_dict["Heat_dt"] = temp_heat_data[2]
        temp_participants_dict["Participants"] = temp_heat_data[1]


        regatta_heats[temp_heat_data[0]] = temp_participants_dict



    regatta_dict["heats"] = regatta_heats

    with open('data.json', 'w') as outfile:
        json.dump(regatta_dict, outfile, sort_keys=True, indent=4)
    
    print "... Done"


if __name__ == '__main__':
    main() 
