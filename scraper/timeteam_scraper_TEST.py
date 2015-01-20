# Name: Thijs Schouten
# Student number: 10887679

'''
This script scrapes regatta data from TIME-TEAM.nl
'''

# --------------------------------------------------------------------------
# Libraries

# Python library imports
import json

# Third party library imports:
import pattern
from pattern.web import Element, URL, DOM, abs, plaintext

# --------------------------------------------------------------------------
# Constant

JSON_NAME = "TEST"
REGATTA_DATE = "05/07/2014"
REGATTA_URL = 'http://regatta.time-team.nl/nsrf/2014/results/matrix.php'

# --------------------------------------------------------------------------
# Scraping

def scrape_heat_urls(regatta_url, regatta_dom):
    '''
    Scrape all the URLs from base regatta page
    @param regatta_url = url to the overview page of the regatta
    @regatta_dom = dom variable containing the page with the heat urls
    return type : heat_urls --> all the heat urls in list
    '''

    heat_urls = []

    # Save absolute links to heats
    for link in regatta_dom('a'):
        temp = abs(link.attributes.get('href',''), base=regatta_url.redirect
                or regatta_url.string)
        if temp [-7:-4].isdigit() == True:
            heat_urls.append(temp)

    return heat_urls

def scrape_names_page(name_url):
    '''
    Return the names found on the name_url url
    @ param name_url = link to page containing crew names
    return type : list of names in the boat
    '''

    # create dom format from URL
    url = URL(name_url)
    dom = DOM(url.download(cached=True))

    names = []

    # For every row in the dom (skipping first): if the first cell
    # contains "slag", append the name and break loop. Else, just append. 
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

    return type: [all_heats_dict, heat_title]
    X @ heat title = the name of the field

    '''

    # Print statement to show program is running
    print "Scraping heat.."

    # Set up all variables
    all_heats_dict = {}
    all_heats_in_field = []
    heat_title = '' 

    # Save the heat url dom
    url = URL(heat_url)
    dom = DOM(url.download(cached=True))

    # For every heat/final
    for i in range(0,len(dom.by_tag('h2'))):

        # Create a heat dictionary
        heat_dictionary = {}

        # Run header_extract to extract title, type and time
        header_data = header_extract(dom.by_tag('h2')[i].content)
        print header_data

        # Save title for later use:
        heat_title = header_data[1]

        # Save time and day plus final/heat data
        heat_dictionary["heat_day_time"] = header_data[0] 
        heat_dictionary["heattype"] = header_data[2]
        heat_dictionary["field"] = header_data[1]
        heat_dictionary["id"] = header_data[3]
        print header_data[3]

        # Go through every table with timeteam class
        for web_table in dom('.timeteam')[i:i+1]:

            # List to store all crews in:
            crew_dict_list = []

            # Select every row in the timeteam class table, start at 1 take 2 steps
            for row in web_table('tr')[1::2]:

                try: 
                    # Check if the first cell is a number, scrape in case it is
                    if (row('td')[0].content[:-1]).isdigit() == True:

                        #-- add variables to dict                               
                        crew_dict = {}
                        crew_dict["position"] = pos_mapping(row('td')[0].content)                                      
                        crew_dict["crew_code"] = plaintext(row('td')[1]\
                                                .content)
                        crew_dict["lane"] = pos_mapping(row('td')[3].content)
                        crew_dict["five_time"] = time_mapping(row('td')[4].content)
                        crew_dict["five_pos"] = pos_mapping(row('td')[5].content)
                        crew_dict["ten_time"] = time_mapping(row('td')[6].content)
                        crew_dict["ten_pos"] = pos_mapping(row('td')[7].content)
                        crew_dict["fifteen_time"] = time_mapping(row('td')[8].content)
                        crew_dict["fifteen_pos"] = pos_mapping(row('td')[9].content)
                        crew_dict["twenty_time"] = time_mapping(row('td')[10].content)
                        crew_dict["twenty_pos"] = pos_mapping(row('td')[11].content)
                        #--
                        

                        #-- get the names of the crew
                        temp_dom = DOM(row('td')[2]) 

                        for a in temp_dom('a'):
                            names_url = abs(a.attributes.get('href',''), base=url.redirect or url.string)
                        #--

                        crew_dict["names"] = scrape_names_page(names_url)  


                        crew_dict_list.append(crew_dict)

                # Print error if index is out of range
                except IndexError:                             
                    print 'IndexError'

        # Add the crew data to the heat dictionary
        heat_dictionary["participants"] = crew_dict_list

        # Append the heat dictionary to a list
        all_heats_in_field.append(heat_dictionary)

    # Return the dictionary and the title
    return all_heats_in_field

def header_extract(input_title):
    '''
    Extract the data from the header
    '''
    heatnames = ["LDDev", "DDev", "LDev", "LDSA", "LDSB", "LDEj",\
                 "LSA", "LSB", "DSA", "LDO", "LDN", "LDB", "Dev", "LEj", "DEj",\
                 "LB", "LN", "DN", "DB", "DO", "LO", "Ej", "SA", "SB",\
                 "O", "N", "B"]  

    boattypes = ["8+", "4+", "4-", "4*", "4x", "2x", "2*", "2-", "2+", "1x",\
                 "1*", "acht"]

    boattype_conv_names = ["acht", "viermet", "vierzonder", "dubbelvier",\
                           "dubbelvier", "dubbeltwee", "dubbeltwee", \
                           "tweezonder", "tweemet", "skiff", "skiff", "acht"]

    heattypes_F = ["A-finale"]
    heattypes_Fb = ["B-finale", "C-finale", "D-finale", "E-finale"]
    heattypes_H = ["voorwedstrijd", "heat"]

    console.log
    time = input_title[0:9] # will find Sat 10:40 as well as Za 10:40
                            # strip trailing whitespace?

    title = 'no_data'
    boat = 'no_data'
    heat = 'no_data' 

    for heatname in heatnames:
        if heatname in input_title:
            title = heatname
            break

    for heattype in heattypes_F:
        if heattype in input_title:
            heat = "Final A"
            break

    for heattype in heattypes_Fb:
        if heattype in input_title:
            print heattype
            heat = "Final B"
            break

    for heattype in heattypes_H:
        if heattype in input_title:
            heat = "Heat"
            break

    for boattype in boattypes:
        if boattype in input_title:
            index = boattypes.index(boattype)
            heat_id = boattype
            boat = boattype_conv_names[index]
            break

    heat_id = title + "" + heat_id

    # If heattype is not specified, assume it is a final
    if heat is 'no_data':
        heat = "Final"

    # Check boat values:
    if boat is 'no_data':
        print "Fault in boattype, input is:", input_title
        print "output boattype is:", boat

    # Check title values:
    if title is 'no_data':
        print "Fault in title, input is:", input_title
        print "output title is:", title


    # Pretty printing for easy testing:
    print input_title
    print "TIME: ", time
    print "BOAT: ", boat
    print "TITLE:", title
    print "HEAT: ", heat
    print "ID:   ", heat_id
    print ""

    return [time, title+"_"+boat, heat, heat_id]

def time_mapping(input_string):
    '''
    Take a string formatted as "mm:ss,ms" and return an integer representing 
    seconds. FE: "07:43,48" becomes 463,48
    '''

    # Show no_data as default
    formatted = "no_data"

    try:
        formatted = (float(input_string[0:2]) * 60 +\
                     float(input_string[-5:-3]) +\
                     float("."+input_string[-2:])),
    except ValueError:
        print "ValueError while getting seconds from" + input_string

    return formatted

def pos_mapping(input_string):
    '''
    Take string, like [1] or (6), and return the number as an int.
    '''
    r = input_string
    s = ''.join(x for x in r if x.isdigit())

    try:
        return int(s)
    except:
        print "Couldnt get position of" + input_string
        return "no_data"

# --------------------------------------------------------------------------
# Main 

def main():
    '''
    '''

    # Set up dictionaries
    regatta_dict = {}
    regatta_heats = {}

    # Create DOM from regatta URL
    url = URL(REGATTA_URL)
    dom = DOM(url.download(cached=True))
    
    # Add metadata to dictionary
    for title in dom.by_tag('title'):
        regatta_title = plaintext(title.content)[:-12]

    regatta_dict["name"] = regatta_title
    regatta_dict["date"] = REGATTA_DATE

    # Fetch heat urls
    heat_urls = scrape_heat_urls(url, dom) 

    #
    regatta_fields = []

    # Save data for every heat
    # for heat in heat_urls[44:45]: --> DSA 8+ NSRF slot
    for heat in heat_urls[-20:]:
        heat_data = scrape_heat_page(heat)

        for heat_dictionary in heat_data:
            regatta_fields.append(heat_dictionary)


    regatta_dict["heat"] = regatta_fields

    # Write dictionary to json file
    with open(JSON_NAME +'.json', 'w') as outfile:
        json.dump(regatta_dict, outfile, sort_keys=True, indent=2)
    
    print "... Done"


if __name__ == '__main__':
    main() 
