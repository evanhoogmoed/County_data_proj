import sqlalchemy
import pandas as pd 
from sqlalchemy import text
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
def db_connect():
    database_username = 'admin'
    database_password = 'Nezzy559'
    database_ip       = 'stats-db.cc4nxcpkcpin.us-west-1.rds.amazonaws.com'
    database_name     = 'stats_db'
    database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password, 
                                                      database_ip, database_name))
    return database_connection
def highest_income_counties(merged_df):
        
    #get the top 10 counties with the highest income and the party that won
    top_10 = merged_df.nlargest(10, "Income")

    top_10["County,State_Abrev"] = top_10["County"].str.title() + ", " + top_10["State_Abrev"].str.upper()
    #drop the word county or parish from county,state_abrev
    top_10["County,State_Abrev"] = top_10["County,State_Abrev"].str.replace(" County", "")
    top_10["County,State_Abrev"] = top_10["County,State_Abrev"].str.replace(" Parish", "")

    
    #make a bar graph for these top 10 counties
    colors = ["#FF6B6B" if x == "donald j trump" else "#2FADCC" if x == "joseph r biden jr" else "green" for x in top_10["Winner"]]
    top_10.plot.bar(x="County,State_Abrev", y="Income", rot=0, color=colors)

    plt.title("Highest Income Counties")
    plt.xlabel("County")
    plt.ylabel("Income")

    #create legend
    red_patch = mpatches.Patch(color='#FF6B6B', label='Republican')
    blue_patch = mpatches.Patch(color='#2FADCC', label='Democrat')
    plt.legend(handles=[red_patch, blue_patch])

    #adjust size of graph and text
    plt.gcf().set_size_inches(14, 5)
    plt.xticks(fontsize=8)

    #plt.show()
    plt.savefig("high_income_political.svg")
    plt.savefig("high_income_political.jpg")

def lowest_income_counties(merged_df):
    #get the top 10 counties with the lowest income and the party that won
    bottom_10 = merged_df.nsmallest(10, "Income")

    bottom_10["County,State_Abrev"] = bottom_10["County"].str.title() + ", " + bottom_10["State_Abrev"].str.upper()
    
    #drop the word county or parish from county,state_abrev
    bottom_10["County,State_Abrev"] = bottom_10["County,State_Abrev"].str.replace(" County", "")
    bottom_10["County,State_Abrev"] = bottom_10["County,State_Abrev"].str.replace(" Parish", "")

    #make a bar graph for these top 10 counties
    colors = ["#FF6B6B" if x == "donald j trump" else "#2FADCC" if x == "joseph r biden jr" else "green" for x in bottom_10["Winner"]]
    bottom_10.plot.bar(x="County,State_Abrev", y="Income", rot=0, color=colors)

    plt.title("Lowest Income Counties")
    plt.xlabel("County")
    plt.ylabel("Income")

    #create legend
    red_patch = mpatches.Patch(color='#FF6B6B', label='Republican')
    blue_patch = mpatches.Patch(color='#2FADCC', label='Democrat')
    plt.legend(handles=[red_patch, blue_patch])

    #adjust size of graph and text
    plt.gcf().set_size_inches(12, 5)
    plt.xticks(fontsize=8)

    #plt.show()
    #save plt as html
    plt.savefig("low_income_political.svg")
    plt.savefig("low_income_political.jpg")


def main():
    conn = db_connect()
    
    #get columns county, state_po, and winner from politics tabl
    politics_df = pd.read_sql(sql=text("SELECT * FROM politics"),con=conn.connect())

    #get columns county, state_abbreviations, and income from economics table
    economics_df = pd.read_sql(sql=text("SELECT * FROM economics"),con=conn.connect())

    #merge the two dataframes
    merged_df = pd.merge(politics_df, economics_df, how="inner", left_on=["County","State_Abrev"], right_on=["County", "State_Abrev"])


    highest_income_counties(merged_df)
    lowest_income_counties(merged_df)





    


if __name__ == "__main__":
    main()
