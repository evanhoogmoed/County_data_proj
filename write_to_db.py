import pandas as pd
import sqlalchemy

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

#make county info df the same format as the other dataframes
def clean_county_df(df):
    #add county to the end of every county name unless its state is Alaska or Louisiana
    df["County"] = df["County"].apply(lambda x: x + " County")

    #if state is Alaska remove from dataframe
    df = df[df["State"] != "Alaska"]

    #if state is Louisiana replace County with Parish
    df.loc[df["State"] == "Louisiana", "County"] = df.loc[df["State"] == "Louisiana", "County"].str.replace(" County", " Parish")

    #for all state names in "State" column map to abbreviation
    df["State_Abbreviation"] = ""
    df["State_Abbreviation"] = df["State"].map(dict_state)

    #for all rows in simplified_df make all strings lowercase
    df = df.applymap(lambda s:s.lower() if type(s) == str else s)

    return df

def db_connect():
    database_username = 'admin'
    database_password = 'Nezzy559'
    database_ip       = 'stats-db.cc4nxcpkcpin.us-west-1.rds.amazonaws.com'
    database_name     = 'stats_db'
    database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password, 
                                                      database_ip, database_name))
    return database_connection


def main():
    #process and format the county df
    county_df = pd.read_csv("./data/county_info_cleaned.csv")
    county_df = clean_county_df(county_df)
    county_df.to_csv("county_info_cleaned.csv", index=False)

    #format the vaccine df
    vaccine_df = pd.read_csv("./data/vaccination_data.csv")
    vaccine_df = vaccine_df[vaccine_df["state"] != "AK"]
    #lowercase all strings in dataframe
    vaccine_df = vaccine_df.applymap(lambda s:s.lower() if type(s) == str else s)

    voting_df = pd.read_csv("./data/voting_info.csv")
    voting_df = voting_df[voting_df["state"] != "alaska"]

    #establish db connection
    db_con = db_connect()

    #write all dfs to db
    voting_df.to_sql(con=db_con, name='politics', if_exists='replace')
    vaccine_df.to_sql(con=db_con, name='vaccines', if_exists='replace')
    county_df.to_sql(con=db_con, name='economics', if_exists='replace')


if __name__ == "__main__":
    main()