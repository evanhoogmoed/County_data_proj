import pandas as pd
import requests

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
    data = requests.get(
        "https://data.cdc.gov/resource/8xkx-amqh.json?$limit=10000&date=2021-12-31T00:00:00.000").json()

    df = pd.DataFrame.from_records(data)

    #sort by state
    df.sort_values(by=['recip_state'], inplace=True)

    #get only recip_county, recip_state,
    df = df[["recip_county", "recip_state", "series_complete_pop_pct","booster_doses_vax_pct",]]

    #rename columns 
    df = df.rename(columns={"recip_county": "County", "recip_state": "State_Abrev", "series_complete_pop_pct": "Fully_Vaccinated", "booster_doses_vax_pct": "Boosters"})

    #get rid of any rows with states we are not interested in
    df = df[df.State_Abrev != "AK"]
    df = df[df.State_Abrev != "PR"]
    df = df[df.State_Abrev != "DC"]
    df = df[df.State_Abrev != "GU"]
    df = df[df.State_Abrev != "VI"]

    #get rid of any rows with Unknown county
    df = df[df.County != "Unknown County"]
    #get rid of any rows with island and virgi
    vaccine_df = df.applymap(lambda s:s.lower() if type(s) == str else s)
    vaccine_df = add_fips_code(vaccine_df)
    #write to csv
    vaccine_df.to_csv("../data/vaccination_data.csv", index=False)

if __name__ == "__main__":
    main()
