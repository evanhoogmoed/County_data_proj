import pandas as pd

#adds extra column to dataframe with unique identifier for each county
def add_fips_code(df):
    fips_df = pd.read_csv("../data/fips.csv")
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
    #read in countypres csv
    df = pd.read_csv("../data/countypres_2000-2020.csv")
    df = df[df["year"] == 2020]
    df = df[["year", "state", "state_po", "county_name", "candidate", "party", "candidatevotes", "totalvotes"]]
    #print(df.head(10))
    #remove states we are not considering
    df = df[df["state_po"] != "AK"]
    df = df[df["state_po"] != "DC"]
    
    #create new dataframe
    simplified_df = pd.DataFrame(columns = ["Year","State", "State_Abrev", "County", "Democrat","Republican","Other", "Winner", "Total_Votes"])


    #get all unique county and state pairs from df
    county_list = df[["county_name", "state"]].drop_duplicates().values.tolist()
    for county,state in county_list:
        #get all rows with matching county and state
        county_df = df[(df["county_name"] == county) & (df["state"] == state)]
        democrat = 0
        republican = 0
        other = 0
        for index, row in county_df.iterrows():
            if row["party"] == "DEMOCRAT":
                democrat = democrat + int(row["candidatevotes"])
            elif row["party"] == "REPUBLICAN":
                republican = republican + int(row["candidatevotes"])
            else:
                other = other + int(row["candidatevotes"])
            
        #get candidate with most votes    
        winner = county_df[county_df["candidatevotes"] == county_df["candidatevotes"].max()]["candidate"].iloc[0]

        #get total votes
        totalvotes = county_df["totalvotes"].iloc[0]
        #get year
        year = county_df["year"].iloc[0]
        #get state
        state = county_df["state"].iloc[0]

        #get state_po
        state_po = county_df["state_po"].iloc[0]
        #get county
        county = county_df["county_name"].iloc[0]

        #if statements to handle the odd ball cases and to add parish and county where needed
        if state == "LOUISIANA":
            county = county + " parish"

        elif county[-5:] != " CITY" and county[-7:] != " COUNTY" and state != "LOUISIANA":
            county = county + " county"

        if state_po == "VA" and county == "JAMES CITY" or state_po == "VA" and county == "CHARLES CITY":
            county = county + " county"
         

        #if county begins with SAINT replace it with st.
        if county[0:5] == "SAINT":
            county = "ST." + county[5:]
        
        if county[0:3] == "ST ":
            county = "ST. " + county[3:]

        simplified_df = pd.concat([simplified_df, pd.DataFrame({"Year": year, "State": state, "State_Abrev": state_po, "County": county, "Democrat": democrat, "Republican": republican, "Other": other, "Winner": winner, "Total_Votes": totalvotes}, index=[0])], ignore_index=True)


    #for all rows in simplified_df make all strings lowercase
    simplified_df = simplified_df.applymap(lambda s:s.lower() if type(s) == str else s)
    simplified_df = add_fips_code(simplified_df)
    #write simplified_df to csv
    simplified_df.to_csv("../data/voting_info.csv", index=False)


if __name__ == "__main__":
    main()

