import concurrent.futures, threading
import requests
import requests_cache
import pandas as pd
from bs4 import BeautifulSoup
import re
import logging

thread_local = threading.local() # instantiates thread to create local data (here: session-attr.)

requests_cache.install_cache("testcache")

def clean_county(county):
    #format the county correctly
    if "[" in county:
        county = county[:county.index("[")]
    if "(" in county:
        county = county[:county.index("(")]
    if county[-2:] == "of":
        county = county[:-2]
    #if county contains "City and County" remove it
    if "City and County" in county:
        county = county[:county.index("City and County")-2]
    if "Town and County" in county:
        county = county[:county.index("Town and County")-2]
    if "Consolidated Municipality" in county:
        county = county[:county.index("Consolidated Municipality")-2]
    if "ñ" in county:
        county = county.replace("ñ", "n")
    
    county = county.replace('\u2013', '')
    county = county.replace("-", "")
    county = county.replace(" ", "")
    county = county.replace(".", "")
    county = county.replace(",", "")
    county = county.replace("'", "")
    return county

def clean_state(state): #breaking code somehow
    #format the state correctly
    if " " in state:
        state = state.replace(" ", "") #space is messing it up somehow
    if state[:4] == "Hawa":
        state = "Hawaii"
    return state

# Get all counties in the US from the Wikipedia page and return a tuple of the county name and state
def get_all_counties():
    response = requests.get("https://en.wikipedia.org/wiki/List_of_United_States_counties_and_county_equivalents")
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", {"class": "wikitable sortable"})
    df = pd.read_html(str(table))[0]

    counties = []
    for index, row in df.iterrows():
        county = row["County or equivalent"]
        county = clean_county(county)
        state = row["State or equivalent"]
        if state == "District of Columbia" or state == "Puerto Rico" or state == "Guam" or state == "Virgin Islands (U.S.)" or state == "Northern Mariana Islands" or state == "American Samoa" or state == "U.S. Minor Outlying Islands":
            continue
        if state[:4] == "Hawa":
            state = "Hawaii"
        if " " in state:
            state = state.replace(" ", "")
        counties.append((county,state))
 
    return counties

def get_county_info(url):
    #logging.debug('Child',url)
    session = get_session()
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser") 
    
    #get title from soup
    title = soup.find("title")
    title = title.text
    #delete everything before the colon
    title = title[title.index(":")+2:]

    #split title into county and state
    print(title)
    county = title[:title.index(",")][:-7]
    state = title[title.index(",")+2:]
    

    #get average income
    income_table = soup.find("a", {"data-title": "Median household income (in 2021 dollars), 2017-2021"})
    income_td = income_table.find_next("td")
    income = income_td.text


    if len(income) < 4:
        print("Invalid income")
        income = None

    else:
        income = income.replace(",", "")
        income = int(income[2:])
        


    #print("Income:",income)
    #get population
    population_table = soup.find("a", {"data-title": "Population Estimates, July 1 2021, (V2021)"})
    population_td = population_table.find_next("td")
    population = population_td.text
    #get rid of comma and leading characters
    population = population.replace(",", "")
    population = int(population[4:])
    #print("Population:", population, "Income:", income)
    return (county, state, population, income)
    
def download_all_sites(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(get_county_info, sites))

    return results


def get_session():
    '''Create a new requests.Session if there is none in thread_local'''
    if not hasattr(thread_local, "session"): 
        thread_local.session = requests.Session()
    return thread_local.session

def create_links(counties):
    links = []
    for county in counties:
        county_name = county[0]
        state_name = county[1]
        #print("County:", county_name, "State:", state_name)

        if state_name == "Alaska" or state_name == "Louisiana":
            county_link = county_name+state_name
        else:
            county_link = county_name + "county" + state_name
        
        link = "https://www.census.gov/quickfacts/" + county_link
        links.append(link)
    return links
def create_df(county_info_list):
    df = pd.DataFrame(county_info_list, columns = ["County", "State", "Population", "Income"])
    return df

def clean_df(df):
    df["County"] = df["County"].str.replace("city", "")
    if "(" in df["County"]:
       df["County"] = df["County"][:df["County"].index("(")] 
    
    return df
def main():
    #logger = logging.getLogger()
    # log all messages, debug and up
    #logger.setLevel(logging.DEBUG)
    counties = get_all_counties()
    #print(counties)
    links = create_links(counties)
    #get the 100th link and on [100:]

    county_info_list = download_all_sites(links)
    df = create_df(county_info_list)
    df = clean_df(df)
    df.to_csv("county_info.csv", index=False)
if __name__ == "__main__":
    main()
