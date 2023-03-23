import { CountyData } from "../dto/CountyData";
import { sortByPopulation, sortByIncome, sortByFullyVaccinated, sortByBoosterRate, sortByTotalVotes, sortByWinnerPercentage, sortByWinner, sortByCounty } from "./sort";

describe("testing the sort functions for County table data", () => {
    const mockData: CountyData[] = [
        {
            "Boosters": 32.6,
            "County": "kent county",
            "FIPS_Code": 10001.0,
            "Fully_Vaccinated": 51.5,
            "Income": 63715.0,
            "Population": 184149,
            "State": "delaware",
            "Total_Votes": 87025,
            "Winner": "joseph r biden jr",
            "Winner_Percentage": 51.2
        },
        {
            "Boosters": 32.1,
            "County": "new castle county",
            "FIPS_Code": 10003.0,
            "Fully_Vaccinated": 64.3,
            "Income": 78428.0,
            "Population": 571708,
            "State": "delaware",
            "Total_Votes": 287633,
            "Winner": "joseph r biden jr",
            "Winner_Percentage": 67.8
        },
        {
            "Boosters": 41.4,
            "County": "sussex county",
            "FIPS_Code": 10005.0,
            "Fully_Vaccinated": 63.9,
            "Income": 68886.0,
            "Population": 247527,
            "State": "delaware",
            "Total_Votes": 129352,
            "Winner": "donald j trump",
            "Winner_Percentage": 55.1
        }
    ];

    test("testing the sortByPopulation function", () => {
        const expected: CountyData[] = [
            {
                "Boosters": 32.1,
                "County": "new castle county",
                "FIPS_Code": 10003.0,
                "Fully_Vaccinated": 64.3,
                "Income": 78428.0,
                "Population": 571708,
                "State": "delaware",
                "Total_Votes": 287633,
                "Winner": "joseph r biden jr",
                "Winner_Percentage": 67.8
            },
            {
                "Boosters": 41.4,
                "County": "sussex county",
                "FIPS_Code": 10005.0,
                "Fully_Vaccinated": 63.9,
                "Income": 68886.0,
                "Population": 247527,
                "State": "delaware",
                "Total_Votes": 129352,
                "Winner": "donald j trump",
                "Winner_Percentage": 55.1
            },
            {
                "Boosters": 32.6,
                "County": "kent county",
                "FIPS_Code": 10001.0,
                "Fully_Vaccinated": 51.5,
                "Income": 63715.0,
                "Population": 184149,
                "State": "delaware",
                "Total_Votes": 87025,
                "Winner": "joseph r biden jr",
                "Winner_Percentage": 51.2
            }
        ];

        const result = sortByPopulation(mockData);
        expect(result).toEqual(expected);
    });

    test("testing the sortByIncome", () => {
        const expected: CountyData[] = [
            {
                "Boosters": 32.1,
                "County": "new castle county",
                "FIPS_Code": 10003.0,
                "Fully_Vaccinated": 64.3,
                "Income": 78428.0,
                "Population": 571708,
                "State": "delaware",
                "Total_Votes": 287633,
                "Winner": "joseph r biden jr",
                "Winner_Percentage": 67.8
            },
            {
                "Boosters": 41.4,
                "County": "sussex county",
                "FIPS_Code": 10005.0,
                "Fully_Vaccinated": 63.9,
                "Income": 68886.0,
                "Population": 247527,
                "State": "delaware",
                "Total_Votes": 129352,
                "Winner": "donald j trump",
                "Winner_Percentage": 55.1
            },
            {
                "Boosters": 32.6,
                "County": "kent county",
                "FIPS_Code": 10001.0,
                "Fully_Vaccinated": 51.5,
                "Income": 63715.0,
                "Population": 184149,
                "State": "delaware",
                "Total_Votes": 87025,
                "Winner": "joseph r biden jr",
                "Winner_Percentage": 51.2
            }
        ];

        const result = sortByIncome(mockData);
        expect(result).toEqual(expected);
    });

    test("testing the sortByFullyVaccinated", () => {
        const expected: CountyData[] = [
            {
                "Boosters": 32.1,
                "County": "new castle county",
                "FIPS_Code": 10003.0,
                "Fully_Vaccinated": 64.3,
                "Income": 78428.0,
                "Population": 571708,
                "State": "delaware",
                "Total_Votes": 287633,
                "Winner": "joseph r biden jr",
                "Winner_Percentage": 67.8
            },
            {
                "Boosters": 41.4,
                "County": "sussex county",
                "FIPS_Code": 10005.0,
                "Fully_Vaccinated": 63.9,
                "Income": 68886.0,
                "Population": 247527,
                "State": "delaware",
                "Total_Votes": 129352,
                "Winner": "donald j trump",
                "Winner_Percentage": 55.1
            },
            {
                "Boosters": 32.6,
                "County": "kent county",
                "FIPS_Code": 10001.0,
                "Fully_Vaccinated": 51.5,
                "Income": 63715.0,
                "Population": 184149,
                "State": "delaware",
                "Total_Votes": 87025,
                "Winner": "joseph r biden jr",
                "Winner_Percentage": 51.2
            }
        ];

        const result = sortByFullyVaccinated(mockData);
        // TODO: fix this test
    });

    test("testing the sortByBoostersRate", () => {
        const expected: CountyData[] = [
            {
                "Boosters": 41.4,
                "County": "sussex county",
                "FIPS_Code": 10005.0,
                "Fully_Vaccinated": 63.9,
                "Income": 68886.0,
                "Population": 247527,
                "State": "delaware",
                "Total_Votes": 129352,
                "Winner": "donald j trump",
                "Winner_Percentage": 55.1
            },
            {
                "Boosters": 32.6,
                "County": "kent county",
                "FIPS_Code": 10001.0,
                "Fully_Vaccinated": 51.5,
                "Income": 63715.0,
                "Population": 184149,
                "State": "delaware",
                "Total_Votes": 87025,
                "Winner": "joseph r biden jr",
                "Winner_Percentage": 51.2
            },
            {
                "Boosters": 32.1,
                "County": "new castle county",
                "FIPS_Code": 10003.0,
                "Fully_Vaccinated": 64.3,
                "Income": 78428.0,
                "Population": 571708,
                "State": "delaware",
                "Total_Votes": 287633,
                "Winner": "joseph r biden jr",
                "Winner_Percentage": 67.8
            }
        ];

        const result = sortByBoosterRate(mockData);
        expect(result).toEqual(expected);
    });

    test("testing the sortByTotalVotes", () => {
        const expected: CountyData[] = [
            {
                "Boosters": 32.1,
                "County": "new castle county",
                "FIPS_Code": 10003.0,
                "Fully_Vaccinated": 64.3,
                "Income": 78428.0,
                "Population": 571708,
                "State": "delaware",
                "Total_Votes": 287633,
                "Winner": "joseph r biden jr",
                "Winner_Percentage": 67.8
            },
            {
                "Boosters": 41.4,
                "County": "sussex county",
                "FIPS_Code": 10005.0,
                "Fully_Vaccinated": 63.9,
                "Income": 68886.0,
                "Population": 247527,
                "State": "delaware",
                "Total_Votes": 129352,
                "Winner": "donald j trump",
                "Winner_Percentage": 55.1
            },
            {
                "Boosters": 32.6,
                "County": "kent county",
                "FIPS_Code": 10001.0,
                "Fully_Vaccinated": 51.5,
                "Income": 63715.0,
                "Population": 184149,
                "State": "delaware",
                "Total_Votes": 87025,
                "Winner": "joseph r biden jr",
                "Winner_Percentage": 51.2
            }
        ];

        const result = sortByTotalVotes(mockData);
        expect(result).toEqual(expected);
    });

    test("testing the sortByWinnerPercentage", () => {
        const expected: CountyData[] = [
            {
                "Boosters": 32.1,
                "County": "new castle county",
                "FIPS_Code": 10003.0,
                "Fully_Vaccinated": 64.3,
                "Income": 78428.0,
                "Population": 571708,
                "State": "delaware",
                "Total_Votes": 287633,
                "Winner": "joseph r biden jr",
                "Winner_Percentage": 67.8
            },
            {
                "Boosters": 41.4,
                "County": "sussex county",
                "FIPS_Code": 10005.0,
                "Fully_Vaccinated": 63.9,
                "Income": 68886.0,
                "Population": 247527,
                "State": "delaware",
                "Total_Votes": 129352,
                "Winner": "donald j trump",
                "Winner_Percentage": 55.1
            },
            {
                "Boosters": 32.6,
                "County": "kent county",
                "FIPS_Code": 10001.0,
                "Fully_Vaccinated": 51.5,
                "Income": 63715.0,
                "Population": 184149,
                "State": "delaware",
                "Total_Votes": 87025,
                "Winner": "joseph r biden jr",
                "Winner_Percentage": 51.2
            }
        ];

        const result = sortByWinnerPercentage(mockData);
        expect(result).toEqual(expected);
    });

    test("testing sortByWinner", () => {
        const expected: CountyData[] = [
            {
                "Boosters": 41.4,
                "County": "sussex county",
                "FIPS_Code": 10005.0,
                "Fully_Vaccinated": 63.9,
                "Income": 68886.0,
                "Population": 247527,
                "State": "delaware",
                "Total_Votes": 129352,
                "Winner": "donald j trump",
                "Winner_Percentage": 55.1
            },
            {
                "Boosters": 32.1,
                "County": "new castle county",
                "FIPS_Code": 10003.0,
                "Fully_Vaccinated": 64.3,
                "Income": 78428.0,
                "Population": 571708,
                "State": "delaware",
                "Total_Votes": 287633,
                "Winner": "joseph r biden jr",
                "Winner_Percentage": 67.8
            },
            {
                "Boosters": 32.6,
                "County": "kent county",
                "FIPS_Code": 10001.0,
                "Fully_Vaccinated": 51.5,
                "Income": 63715.0,
                "Population": 184149,
                "State": "delaware",
                "Total_Votes": 87025,
                "Winner": "joseph r biden jr",
                "Winner_Percentage": 51.2
            }
        ];

        const result = sortByWinner(mockData);
        expect(result).toEqual(expected);
    });

    test("testing sortByCounty", () => {
        const result = sortByCounty(mockData);
        expect(result).toEqual(mockData);
    });



});