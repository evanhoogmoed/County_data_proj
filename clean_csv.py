import pandas as pd

# Read in the data
df = pd.read_csv("county_info.csv")

#get rid of ( from county names
df["County"] = df["County"].str.replace("(", "")

#loop through each row in "County" column
for index, row in df.iterrows():
    #get county name
    county = row["County"]
    if "City and" in county:
        print(county)
        row["County"] = county.replace("City and", "")
        print(row["County"])
    

#write df to new csv
df.to_csv("county_info_cleaned.csv", index=False)