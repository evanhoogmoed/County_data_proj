export interface CountyData {
    State: string;
    County: string;
    FIPS_Code: number;
    Income: number;
    Fully_Vaccinated: number;
    Boosters: number;
    Population: number;
    Total_Votes: number;
    Winner_Percentage: number;
    Winner: string;
}

export const DEFAULT_COUNTY_DATA: CountyData = {
    State: '',
    County: '',
    FIPS_Code: 0,
    Income: 0,
    Fully_Vaccinated: 0,
    Boosters: 0,
    Population: 0,
    Total_Votes: 0,
    Winner_Percentage: 0,
    Winner: '',
};
