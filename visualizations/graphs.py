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

  
    #create column in top_10 with county,state_po pair
    top_10["county,state_po"] = top_10["county"].str.title() + ", " + top_10["state_po"].str.upper()
    

    #make a bar graph for these top 10 counties
    colors = ["#FF6B6B" if x == "donald j trump" else "#2FADCC" if x == "joseph r biden jr" else "green" for x in top_10["winner"]]
    top_10.plot.bar(x="county,state_po", y="Income", rot=0, color=colors)

    plt.title("Highest Income Counties")
    plt.xlabel("County")
    plt.ylabel("Income")

    #create legend
    red_patch = mpatches.Patch(color='#FF6B6B', label='Republican')
    blue_patch = mpatches.Patch(color='#2FADCC', label='Democrat')
    plt.legend(handles=[red_patch, blue_patch])

    #adjust size of graph and text
    plt.gcf().set_size_inches(12, 5)
    plt.xticks(fontsize=8)

    plt.show()

def lowest_income_counties(merged_df):
    #get the top 10 counties with the lowest income and the party that won
    bottom_10 = merged_df.nsmallest(10, "Income")

    bottom_10["county,state_po"] = bottom_10["county"].str.title() + ", " + bottom_10["state_po"].str.upper()
    

    #make a bar graph for these top 10 counties
    colors = ["#FF6B6B" if x == "donald j trump" else "#2FADCC" if x == "joseph r biden jr" else "green" for x in bottom_10["winner"]]
    bottom_10.plot.bar(x="county,state_po", y="Income", rot=0, color=colors)

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

    plt.show()


def main():
    conn = db_connect()
    
    #get columns county, state_po, and winner from politics tabl
    politics_df = pd.read_sql(sql=text("SELECT county, state_po, winner FROM politics"),con=conn.connect())

    #get columns county, state_abbreviations, and income from economics table
    economics_df = pd.read_sql(sql=text("SELECT County, State_Abbreviation, Income FROM economics"),con=conn.connect())
    
    #drop the word county or parish from the county column in econmics_df
    economics_df["County"] = economics_df["County"].str.replace(" county", "")
    economics_df["County"] = economics_df["County"].str.replace(" parish", "")

    #merge the two dataframes
    merged_df = pd.merge(politics_df, economics_df, how="inner", left_on=["county", "state_po"], right_on=["County", "State_Abbreviation"])
    merged_df = merged_df.drop(columns=["County", "State_Abbreviation"])

    #get the average income for each party
    income_by_party = merged_df.groupby("winner").mean()
    print(income_by_party)

    highest_income_counties(merged_df)
    lowest_income_counties(merged_df)


if __name__ == "__main__":
    main()