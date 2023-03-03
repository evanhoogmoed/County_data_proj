import pandas as pd
import requests

data = requests.get(
    "https://data.cdc.gov/resource/8xkx-amqh.json?$limit=10000&date=2021-12-31T00:00:00.000").json()

df = pd.DataFrame.from_records(data)

#sort by state
df.sort_values(by=['recip_state'], inplace=True)
print(df)

#get only recip_county, recip_state,
df = df[["recip_county", "recip_state", "series_complete_pop_pct","booster_doses_vax_pct",]]

#rename columns 
df = df.rename(columns={"recip_county": "county", "recip_state": "state", "series_complete_pop_pct": "fully_vaccinated", "booster_doses_vax_pct": "boosters"})

#write to csv
df.to_csv("vaccination_data.csv", index=False)