import folium
import requests
import json
import branca
import pandas as pd
import webbrowser
import sqlalchemy
import geopandas as gpd

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

    print(geoData.head())
    return geoData

def make_folium_map(df):   
    m = folium.Map(location=[40, -102], tiles="cartodbpositron", zoom_start=4)
    folium.Choropleth(
        geo_data=df,
        name="choropleth",
        data=df,
        columns=["COUNTY", "Fully_Vaccinated"],
        key_on="feature.properties.COUNTY",
        fill_color="YlGn",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Fully Vaccinated (%)",
    ).add_to(m)
    #save to html
    m.save("map.html")

    #open html in browser
    webbrowser.open("map.html")

#get vaccine_df and seperate the FIPS code to state and county codes 
def vaccine_df():
    conn = db_connect()
    vaccine_df = pd.read_sql("SELECT * FROM vaccines", conn)
    #sort vaccine_df by State_Abrev and County in reverse
    vaccine_df = vaccine_df.sort_values(by=["State_Abrev", "County"])
    #make FIPS code a string and drop .0 
    vaccine_df["FIPS_Code"] = vaccine_df["FIPS_Code"].astype(str).str[:-2]
    #add column County_Code and set it to the last 3 digits of FIPS_Code
    vaccine_df["County_Code"] = vaccine_df["FIPS_Code"].astype(str).str[-3:]
    #if FIPS_CODE is 4 digits add 0 to front
    vaccine_df["FIPS_Code"] = vaccine_df["FIPS_Code"].apply(lambda x: x.zfill(5))
    #add column State_Code and set it to the first 2 digits of FIPS_Code
    vaccine_df["State_Code"] = vaccine_df["FIPS_Code"].astype(str).str[:2]
    vaccine_df.dropna(subset=['Fully_Vaccinated'], inplace=True)
    print(vaccine_df.head())

    return vaccine_df

def main():
    countydf = create_county_map()
    vaccinedf = vaccine_df()

    #merge countydf and vaccine df on STATE and COUNTY
    merged_df = pd.merge(countydf, vaccinedf, left_on=["STATE", "COUNTY"], right_on=["State_Code", "County_Code"])
    print(merged_df.head())
    
    #print number of Nan values in merged_df
    print("Number of NaN values in merged_df",merged_df.isna().sum())
    make_folium_map(merged_df)



if __name__ == "__main__":
    main()



