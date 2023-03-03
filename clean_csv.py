import pandas as pd

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


df = pd.read_csv("./data/county_info_cleaned.csv")

#add county to the end of every county name unless its state is Alaska or Louisiana
df["County"] = df["County"].apply(lambda x: x + " County")

#if state is Alaska remove County from end of county name
df.loc[df["State"] == "Alaska", "County"] = df.loc[df["State"] == "Alaska", "County"].str.replace(" County", "")
#if state is Louisiana replace County with Parish
df.loc[df["State"] == "Louisiana", "County"] = df.loc[df["State"] == "Louisiana", "County"].str.replace(" County", " Parish")

#for all state names in "State" column map to abbreviation
df["State_Abbreviation"] = ""
df["State_Abbreviation"] = df["State"].map(dict_state)

#for all rows in simplified_df make all strings lowercase
df = df.applymap(lambda s:s.lower() if type(s) == str else s)

df.to_csv("county_info_cleaned.csv", index=False)
