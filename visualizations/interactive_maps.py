import folium
import requests
import json
import branca
import pandas as pd
import webbrowser
import sqlalchemy
import geopandas as gpd
from shapely.geometry import Polygon, mapping

def db_connect():
    database_username = 'admin'
    database_password = 'Nezzy559'
    database_ip       = 'stats-db.cc4nxcpkcpin.us-west-1.rds.amazonaws.com'
    database_name     = 'stats_db'
    database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password, 
                                                      database_ip, database_name))
    return database_connection

url = (
    "https://raw.githubusercontent.com/python-visualization/folium/main/examples/data"
)

#create county map with geopandas
def create_county_map():
    # Load the json file with county coordinates
    geoData = gpd.read_file('https://raw.githubusercontent.com/holtzy/The-Python-Graph-Gallery/master/static/data/US-counties.geojson')

    # Make sure the "id" column is an integer
    geoData.id = geoData.id.astype(str).astype(int)

    # Remove Alaska and Puerto Rico.
    stateToRemove = ['02', '72']
    geoData = geoData[~geoData.STATE.isin(stateToRemove)]

    #print(geoData.head())
    return geoData

#functions the API calls to create maps
def make_vaccination_map():
    conn = db_connect()
    countydf = create_county_map()
    vaccinedf = vaccine_df(conn)
    merged_vacc_df = pd.merge(countydf, vaccinedf, left_on=["STATE", "COUNTY"], right_on=["State_Code", "County_Code"])
    m = make_folium_map(merged_vacc_df, "Fully_Vaccinated", "Fully Vaccinated (%)", "YlGn",'#276221') 
    m.get_root().width = "100%"
    m.get_root().height = "100%"
    return m

def make_income_map():
    conn = db_connect()
    countydf = create_county_map()
    incomedf = income_df(conn)
    merged_income_df = pd.merge(countydf, incomedf, left_on=["STATE", "COUNTY"], right_on=["State_Code", "County_Code"])
    m = make_folium_map(merged_income_df, "Income", "Median Income", "YlOrRd",'#8c2d04') 
    m.get_root().width = "100%"
    m.get_root().height = "100%"
    return m

def make_party_map():
    conn = db_connect()
    countydf = create_county_map()
    partydf = party_df(conn)
    merged_party_df = pd.merge(countydf, partydf, left_on=["STATE", "COUNTY"], right_on=["State_Code", "County_Code"])
    m = make_folium_party_map(merged_party_df,'#276221') 
    m.get_root().width = "100%"
    m.get_root().height = "100%"
    return m

def county_style(fips,winner,function=False):
    
    #Set state colour
    if winner == 'joseph r biden jr':
        color = '#4f7bff' #blue
    elif winner == 'donald j trump':
        color = '#ff5b4f' #red
    else:
        color = '#a64dff' #purple
    
    #Set state style
    if function == False:
        # Format for style_dictionary
        county_style = {
            'opacity': 1,
            'color': color,
        } 
    else:
        # Format for style_function
        county_style = {
             'fillOpacity': 1,
             'weight': 1,
             'fillColor': color,
             'color': '#000000'}    
  
    return county_style

def style_function(feature):
    FIPS_Code = feature['properties']['FIPS_Code']
    winner = feature['properties']['Winner']
    style = county_style(FIPS_Code,winner,function=True)
    
    return style


def make_folium_party_map(df,line_color):   
    m = folium.Map(location=[38, -99], tiles="cartodbpositron", zoom_start=5)

    style = {'color': line_color}
    state_geo = f"{url}/us-states.json"
    folium.GeoJson(data= df.to_json(),style_function=style_function).add_to(m)
    folium.GeoJson(state_geo, name="geojson",style_function=lambda x:style).add_to(m)
    return m


def make_folium_map(df,display_column,measurement,coloring,line_color):   
    m = folium.Map(location=[38, -99], tiles="cartodbpositron", zoom_start=5)

    style = {'color': line_color}
    state_geo = f"{url}/us-states.json"
    folium.GeoJson(state_geo, name="geojson",style_function=lambda x:style).add_to(m)

    folium.Choropleth(
        geo_data=df,
        name="choropleth",
        data=df,
        columns=["COUNTY", display_column],
        key_on="feature.properties.COUNTY",
        fill_color=coloring,
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=measurement,
    ).add_to(m)


    return m

#format the vaccine data to be merged with county map
def vaccine_df(conn):
    vaccine_df = pd.read_sql("SELECT * FROM vaccines", conn)
    #sort vaccine_df by State_Abrev and County in reverse
    vaccine_df = vaccine_df.sort_values(by=["State_Abrev", "County"])
    vaccine_df = split_fips_code(vaccine_df)
    vaccine_df.dropna(subset=['Fully_Vaccinated'], inplace=True)

    return vaccine_df

def income_df(conn):
    income_df = pd.read_sql("SELECT * FROM economics", conn)
    income_df = income_df.sort_values(by=["State_Abrev", "County"])
    income_df = split_fips_code(income_df)
    income_df.dropna(subset=['Income'], inplace=True)
    
    return income_df

def party_df(conn):
    partydf = pd.read_sql("SELECT * FROM politics", conn)
    partydf = partydf.sort_values(by=["State_Abrev", "County"])
    partydf = split_fips_code(partydf)
    partydf.dropna(subset=['Winner'], inplace=True)
    
    return partydf

#split the FIPS code into state and county codes
def split_fips_code(df):
    df["FIPS_Code"] = df["FIPS_Code"].astype(str).str[:-2]
    df["County_Code"] = df["FIPS_Code"].astype(str).str[-3:]

    #if the length of FIPS_Code is less than 5, add a 0 to the front
    df["FIPS_Code"] = df["FIPS_Code"].apply(lambda x: x.zfill(5))
    df["State_Code"] = df["FIPS_Code"].astype(str).str[:2]

    return df


def main():
    conn = db_connect()

    countydf = create_county_map()
    vaccinedf = vaccine_df(conn)
    incomedf = income_df(conn)
    partydf = party_df(conn)
    print(partydf.head())

 
    #create vaccine map
    merged_vacc_df = pd.merge(countydf, vaccinedf, left_on=["STATE", "COUNTY"], right_on=["State_Code", "County_Code"])
    m_vaccinated = make_folium_map(merged_vacc_df, "Fully_Vaccinated", "Fully Vaccinated (%)", "YlGn",'#276221') 
    m_vaccinated.save("vaccinated_map.html")


    #create income map
    merged_income_df = pd.merge(countydf, incomedf, left_on=["STATE", "COUNTY"], right_on=["State_Code", "County_Code"])
    m_income = make_folium_map(merged_income_df, "Income", "Median Income", "YlOrRd",'#8c2d04') 
    m_income.save("income_map.html")

    #create party map
    merged_party_df = pd.merge(countydf, partydf, left_on=["STATE", "COUNTY"], right_on=["State_Code", "County_Code"])
    m_party = make_folium_party_map(merged_party_df,'#000000')
    m_party.save("party_map.html")


    #open html in browser
    #webbrowser.open("vaccinated_map.html")
    #webbrowser.open("income_map.html")
    #webbrowser.open("party_map.html")






if __name__ == "__main__":
    main()







