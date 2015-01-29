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
# Constants

REGATTA_TITLE = "HOLLANDIA 2013"
REGATTA_URL = "http://regatta.time-team.nl/hollandia/2013/results/matrix.php"

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

    # Set up all variables
    all_heats_dict = {}
    all_heats_in_field = []
    heat_title = ''
    ignored = []

    # Save the heat url dom
    url = URL(heat_url)
    dom = DOM(url.download(cached=True))

    # For every race
    for i in range(0,len(dom.by_tag('h2'))):

        # Create a race dictionary
        race_dictionary = {}

        # Run header_extract to extract title, type and time
        header_data = header_extract(dom.by_tag('h2')[i].content)

        if header_data[0] == "no_data":
            print ">>>>IGNORED:", header_data[1]
            ignored.append(header_data[1])
            break

        # Save title for later use:
        heat_title = header_data[1]

        # Update race_dictionary with data from header
        titles = ["_day", "_time", "_boat", "_title", "_status", "_id"]
        for j in range(0,6):
            race_dictionary[titles[j]] = header_data[j]

        race_dictionary["_regtitle"] = REGATTA_TITLE

        # Go through every table with timeteam class
        for web_table in dom('.timeteam')[i:i+1]:

            teams_list = []

            # Select row in the timeteam class table, start at 1 take 2 steps
            for row in web_table('tr')[1::2]:

                try: 
                    # Check if the first cell is a number, scrape in case it is
                    if (row('td')[0].content[:-1]).isdigit() == True:

                        # Get the names of the crew
                        temp_dom = DOM(row('td')[2]) 
                        for a in temp_dom('a'):
                            names_url = abs(a.attributes.get('href',''),\
                                         base=url.redirect or url.string)

                        # Add the vars to team dictionary                               
                        team = {} 
                        team["_people"] = scrape_names_page(names_url) 
                        team["_finish"] = extract_int(row('td')[0].content)
                        team["_code"]   = plaintext(row('td')[1].content)
                        team["_lane"]   = extract_int(row('td')[3].content)
                        team["_0500m"]  = [calc_sec(row('td')[4].content),
                                          extract_int(row('td')[5].content)]
                        team["_1000m"]  = [calc_sec(row('td')[6].content),
                                          extract_int(row('td')[7].content)]
                        team["_1500m"]  = [calc_sec(row('td')[8].content),
                                          extract_int(row('td')[9].content)]
                        team["_2000m"]  = [calc_sec(row('td')[10].content),
                                          extract_int(row('td')[11].content)] 

                        # count how many times a clubcode appears in heat
                        team["_uniqueID"] = team["_code"] + "  " + str(\
                                            hash(str(team["_people"]) +\
                                            str(race_dictionary["_time"])))

                        teams_list.append(team)

                except IndexError:                            
                    print 'IndexError'


        # Add the crew data to the heat dictionary
        race_dictionary["_teams"] = teams_list

        # Append the heat dictionary to a list
        all_heats_in_field.append(race_dictionary)

    # Return the dictionary and the skipped fields
    return all_heats_in_field

def scrape_heat_page_2(heat_url):
    '''
    Return heat data with stats about races, including:
    (pre-final/a-final/b-final etc), club, finishposition, lane, 500m time, 
    1000m time, 1500m time, 2000m time,

    return type: [all_heats_dict, heat_title]
    X @ heat title = the name of the field

    '''

    # Set up all variables
    all_heats_dict = {}
    all_heats_in_field = []
    heat_title = ''
    ignored = []

    # Save the heat url dom
    url = URL(heat_url)
    dom = DOM(url.download(cached=True))

    # For every race
    for i in range(0,len(dom.by_tag('h2'))):

        # Create a race dictionary
        race_dictionary = {}

        # Run header_extract to extract title, type and time
        header_data = header_extract(dom.by_tag('h2')[i].content)

        if header_data[0] == "no_data":
            print ">>>>IGNORED:", header_data[1]
            ignored.append(header_data[1])
            break

        # Save title for later use:
        heat_title = header_data[1]

        # Update race_dictionary with data from header
        titles = ["_day", "_time", "_boat", "_title", "_status", "_id"]
        for j in range(0,6):
            race_dictionary[titles[j]] = header_data[j]

        race_dictionary["_regtitle"] = REGATTA_TITLE

        # Go through every table with timeteam class
        for web_table in dom('.timeteam')[i:i+1]:

            teams_list = []

            # Select row in the timeteam class table, start at 1 take 2 steps
            for row in web_table('tr')[1::2]:

                try: 
                    # Check if the first cell is a number, scrape in case it is
                    if (row('td')[0].content[:-1]).isdigit() == True:

                        # Get the names of the crew
                        temp_dom = DOM(row('td')[2]) 
                        for a in temp_dom('a'):
                            names_url = abs(a.attributes.get('href',''),\
                                         base=url.redirect or url.string)

                        print "_people", scrape_names_page(names_url) 
                        print "_finish", row('td')[0].content
                        print "_code", row('td')[1].content
                        print "_lane", row('td')[4].content
                        print "_0500m", [row('td')[5].content,
                                          row('td')[4].content]
                        print "_1000m", [row('td')[7].content,
                                          row('td')[6].content]
                        print "_1500m", [row('td')[9].content,
                                          row('td')[8].content]
                        print "_2000m", [row('td')[11].content,
                                          row('td')[10].content] 

                        # Add the vars to team dictionary                               
                        team = {} 
                        team["_people"] = scrape_names_page(names_url) 
                        team["_finish"] = extract_int(row('td')[0].content)
                        team["_code"]   = plaintext(row('td')[1].content)
                        team["_lane"]   = extract_int(row('td')[4].content)
                        team["_0500m"]  = [calc_sec(row('td')[5].content),
                                          extract_int(row('td')[6].content)]
                        team["_1000m"]  = [calc_sec(row('td')[7].content),
                                          extract_int(row('td')[8].content)]
                        team["_1500m"]  = [calc_sec(row('td')[9].content),
                                          extract_int(row('td')[10].content)]
                        team["_2000m"]  = [calc_sec(row('td')[11].content),
                                          extract_int(row('td')[12].content)] 

                        team["_uniqueID"] = team["_code"] + "  " + str(\
                                            hash(str(team["_people"]) +\
                                            str(race_dictionary["_time"])))

                        # print team["_uniqueID"]

                        teams_list.append(team)
                        print team

                except IndexError:                            
                    print 'IndexError'


        # Add the crew data to the heat dictionary
        race_dictionary["_teams"] = teams_list

        # Append the heat dictionary to a list
        all_heats_in_field.append(race_dictionary)

    # Return the dictionary and the skipped fields
    return all_heats_in_field

def header_extract(input_title):
    '''
    Extract info from header. 
    @param input_title = header
    '''
    heatnames = ["LDDev", "DDev", "LDev", "LDSA", "LDSB", "LDEj",\
                 "LSA", "LSB", "DSA", "LDO", "LDN", "LDB", "Dev", "LEj", "DEj",\
                 "LB", "LN", "DN", "DB", "DO", "LO", "Ej", "SA", "SB",\
                 "O", "N", "B"]

    not_into = ["J18", "M18", "J16", "M16", "Jongens", "Meisjes",\
                         "Mix", "Club", "C4"]

    boattypes  = ["8+", "4+", "4-", "4*", "4x", "4x+", "4*+", "2x", "2*", "2-",\
                 "2+", "1x", "1*", "acht"]

    conv_names = ["coxed_eight", "coxed_four", "coxless_four", "quad",\
                           "quad", "coxed_quad", "coxed_quad", "double",\
                           "double", "coxless_pair", "coxed_pair", "single",\
                           "single", "coxed_eight"]

    heattypes_F = ["A-finale"]
    heattypes_Fb = ["B-finale", "C-finale", "D-finale", "E-finale"]
    heattypes_H = ["voorwedstrijd", "heat"]

    time, day, title, boat, heat = 'no_data', 'no_data', 'no_data', 'no_data', 'no_data'

    time = input_title.split()[1]
    day = get_weekday(input_title.split()[0])

    # Skip the ones not interested in..
    for heatname in not_into:
        if heatname in input_title:
            return ["no_data", input_title]

    # Look for the title, if the title is not in the list- return no_data
    for i, heatname in enumerate(heatnames):
        if heatname in input_title:
            title = heatname
            break
        if title == 'no_data' and i == (len(heatnames)-1):
            #print "Fault in title, input is:", input_title,\
            #      "output title is:", title
            return ["no_data", input_title] 

    for heattype in heattypes_F:
        if heattype in input_title:
            heat = "Final"
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
            boat = conv_names[index]
            break

    heat_id = title + "" + heat_id.replace("*", "x")

    # If heattype is not specified, assume it is a final
    if heat is 'no_data':
        heat = "Final"

    # Check boat values:
    if boat is 'no_data':
        print "Fault in boattype, input is:", input_title
        print "output boattype is:", boat


    # Pretty printing for easy testing:
    # print input_title
    # print "TIME:", time, "<> DAY:", day, "<> BOAT:", boat,\
    #       "<> TITLE:", title, "<> HEAT:", heat, "<> ID:", heat_id

    print heat_id + ".. done"

    return [day, time, boat, title, heat, heat_id]

def calc_sec(input_string):
    '''
    Take a string formatted as "mm:ss,ms" and return an integer representing 
    seconds. FE: "07:43,48" becomes 463,48
    '''

    formatted = "no_data"

    try:
        formatted = (float(input_string[0:2]) * 60 +\
                     float(input_string[-5:-3]) +\
                     float("."+input_string[-2:])),
    except ValueError:
        print "ValueError while getting seconds from" + input_string

    return formatted[0]

def extract_int(input_string):
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

def get_weekday(input_string):
    '''
    Extract weekday
    '''
    days_dict = {"Mon": ["monday", "mon", "mo", "maandag", "maa", "ma"],
                 "Tue": ["tuesday", "tue", "tu", "dinsdag", "din", "di"],
                 "Wed": ["wednesday", "wed", "we", "woensdag", "woe", "wo"],
                 "Thu": ["thursday", "thu", "th", "donderdag", "don", "do"],
                 "Fri": ["friday", "fri", "fr", "vrijdag", "vrij", "vri"],
                 "Sat": ["saturday", "sat", "sa" ,"zaterdag", "zat", "za"],
                 "Sun": ["sunday", "sun", "su", "zon", "zondag", "zo"]}

    print input_string

    for key in days_dict:
        if input_string in days_dict[key]:
            return key

# --------------------------------------------------------------------------
# Main 

def main():

    # Set up dictionaries
    regatta_dict = {}
    regatta_heats = {}

    # Create DOM from regatta URL
    url = URL(REGATTA_URL)
    dom = DOM(url.download(cached=True, unicode=True))

    # If scraping does not work, try \:
    # DOM(url.download(cached=True, unicode=True))

    # Fetch heat urls
    heat_urls = scrape_heat_urls(url, dom) 

    # Create a list to save the fields
    regatta_fields = []

    # Save data for every heat
    for heat in heat_urls:
        heat_data = scrape_heat_page(heat)

        for race_dictionary in heat_data:
            regatta_fields.append(race_dictionary)


    regatta_dict["heats"] = regatta_fields

    # Write dictionary to json file
    with open(REGATTA_TITLE +'.json', 'w') as outfile:
        json.dump(regatta_dict, outfile, sort_keys=True, indent=2)
    
    print "... Done"

if __name__ == '__main__':
    main() 