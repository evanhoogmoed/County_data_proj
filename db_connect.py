import sqlalchemy
import pandas as pd
import pymysql
from sqlalchemy import text

#read in county_info_cleaned.csv
#county_df = pd.read_csv("county_info_cleaned.csv")
#read in counting_voting_info.csv
voting_df = pd.read_csv("counting_voting_info.csv")


database_username = 'admin'
database_password = 'Nezzy559'
database_ip       = 'stats-db.cc4nxcpkcpin.us-west-1.rds.amazonaws.com'
database_name     = 'stats_db'
database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password, 
                                                      database_ip, database_name))
voting_df.to_sql(con=database_connection, name='politics', if_exists='replace')
#print("Writing to Db")
#county_df.to_sql(con=database_connection, name='economics', if_exists='replace')

#test = pd.read_sql(sql=text("SELECT * FROM economics"),con=database_connection.connect())
#print(test)
