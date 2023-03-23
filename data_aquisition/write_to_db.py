import pandas as pd
import sqlalchemy

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
    county_df = pd.read_csv("./data/county_info.csv")
    vaccine_df = pd.read_csv("./data/vaccination_data.csv")
    voting_df = pd.read_csv("./data/voting_info.csv")

    #establish db connection
    db_con = db_connect()

    #write all dfs to db
    voting_df.to_sql(con=db_con, name='politics', if_exists='replace')
    vaccine_df.to_sql(con=db_con, name='vaccines', if_exists='replace')
    county_df.to_sql(con=db_con, name='economics', if_exists='replace')


if __name__ == "__main__":
    main()
