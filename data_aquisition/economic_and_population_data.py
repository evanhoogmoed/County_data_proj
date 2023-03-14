import concurrent.futures, threading
import requests
import requests_cache
import pandas as pd
from bs4 import BeautifulSoup
import re
import logging

thread_local = threading.local() # instantiates thread to create local data (here: session-attr.)

requests_cache.install_cache("testcache")

dict_state = {'Alabama':'AL', 'Alaska':'AK', 'Arizona':'AZ', 'Arkansas':'AR', 'California':'CA',
              'Colorado':'CO', 'Connecticut':'CT', 'Delaware':'DE', 'District of Columbia':'DC', 
              'Florida':'FL', 'Georgia':'GA', 'Hawaii':'HI', 'Idaho':'ID', 'Illinois':'IL', 
              'Indiana':'IN', 'Iowa':'IA', 'Kansas':'KS', 'Kentucky':'KY', 'Louisiana':'LA', 
              'Maine':'ME', 'Maryland':'MD', 'Massachusetts':'MA', 'Michigan':'MI', 'Minnesota':'MN', 
              'Mississippi':'MS', 'Missouri':'MO', 'Montana':'MT', 'Nebraska':'NE', 'Nevada':'NV', 
              'New Hampshire':'NH', 'New Jersey':'NJ', 'New Mexico':'NM', 'New York':'NY', 
              'North Carolina':'NC', 'North Dakota':'ND', 'Ohio':'OH', 'Oklahoma':'OK', 
              'Oregon':'OR', 'Pennsylvania':'PA', 'Rhode Island':'RI', 'South Carolina':'SC', 
              'South Dakota':'SD', 'Tennessee':'TN', 'Texas':'TX', 'Utah':'UT', 'Vermont':'VT', 
              'Virginia':'VA', 'Washington':'WA', 'West Virginia':'WV', 'Wisconsin':'WI', 'Wyoming':'WY'}

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

def clean_state(state):
    #format the state correctly
    if " " in state:
        state = state.replace(" ", "")
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
        if state == "District of Columbia" or state == "Puerto Rico" or state == "Guam" or state == "Virgin Islands (U.S.)" or state == "Northern Mariana Islands" or state == "American Samoa" or state == "U.S. Minor Outlying Islands" or state == "Alaska":
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
    county = title[:title.index(",")]
    state = title[title.index(",")+2:]
    print(county)  

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

        if  state_name == "Louisiana":
            county_link = county_name+state_name
        else:
            county_link = county_name + "county" + state_name
        
        link = "https://www.census.gov/quickfacts/" + county_link
        links.append(link)
    return links

#add additional columns for lookup and clean dataframe
def create_df(county_info_list):
    df = pd.DataFrame(county_info_list, columns = ["County", "State", "Population", "Income"])
    df["State_Abrev"] = df["State"].map(dict_state)
    df = df.applymap(lambda s:s.lower() if type(s) == str else s)
    #if county contains (county) remove it
    df["County"] = df["County"].apply(lambda x: x[:x.index("(")-1] if "(" in x else x)
    #replace n with tilde with just n
    df["County"] = df["County"].apply(lambda x: x.replace("ñ", "n") if "ñ" in x else x)
    df = add_fips_code(df)
    return df


#adds extra column to dataframe with unique identifier for each county
def add_fips_code(df):
    fips_df = pd.read_csv("./data/fips.csv")
    fips_df = fips_df.applymap(lambda s:s.lower() if type(s) == str else s)
    df["FIPS_Code"] = ""
    for index, row in df.iterrows():
        county = row["County"]
        state = row["State_Abrev"]
        fips_code = fips_df.loc[(fips_df["Area_name"] == county) & (fips_df["State"] == state)]['FIPS_Code']
        fips_code = fips_code.to_numpy()
        if len(fips_code) == 0:
            print("no fips code found for county: ", county, " state: ", state)
            continue
        df.loc[index, "FIPS_Code"] = fips_code[0]
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
    #df = clean_df(df)
    df.to_csv("./data/county_info.csv", index=False)

if __name__ == "__main__":
    main()
