import pandas as pd

def main():
    #read in countypres csv
    df = pd.read_csv("countypres_2000-2020.csv")
    df = df[df["year"] == 2020]
    #get only columns year, state, state_po, county, candidate, party, candidatevotes, totalvotes
    df = df[["year", "state", "state_po", "county_name", "candidate", "party", "candidatevotes", "totalvotes"]]
    #print(df.head(10))

    #loop through every row in df
    #for index, row in df.iterrows():
    #create new dataframe
    simplified_df = pd.DataFrame(columns = ["year", "state", "state_po", "county", "democrat","republican","other", "winner", "totalvotes"])


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
        #add row to simplified_df
        #simplified_df = simplified_df.append({"year": year, "state": state, "state_po": state_po, "county": county, "democrat": democrat, "republican": republican, "other": other, "winner": winner, "totalvotes": totalvotes}, ignore_index=True)
        #add row to simplified_df using concat
        simplified_df = pd.concat([simplified_df, pd.DataFrame({"year": year, "state": state, "state_po": state_po, "county": county, "democrat": democrat, "republican": republican, "other": other, "winner": winner, "totalvotes": totalvotes}, index=[0])], ignore_index=True)


    #for all rows in simplified_df make all strings lowercase
    simplified_df = simplified_df.applymap(lambda s:s.lower() if type(s) == str else s)
    #write simplified_df to csv
    simplified_df.to_csv("counting_voting_info.csv", index=False)


if __name__ == "__main__":
    main()

