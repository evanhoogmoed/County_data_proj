import { CountyData } from "../dto/CountyData";

export function sortByCounty(countyData: CountyData[]): CountyData[] {
    return countyData.sort((a, b) => {
        return a.County.localeCompare(b.County);
    });
}

export function sortByPopulation(countyData: CountyData[]): CountyData[] {
    const sorted = countyData.sort((a, b) => {
        return b.Population - a.Population;
    });
    return sorted;
}

export function sortByIncome(countyData: CountyData[]): CountyData[] {
    return countyData.sort((a, b) => {
        return b.Income - a.Income;
    });
}

export function sortByFullyVaccinated(countyData: CountyData[]): CountyData[] {
    return countyData.sort((a, b) => {
        return b.Fully_Vaccinated - a.Fully_Vaccinated;
    });
}

export function sortByBoosterRate(countyData: CountyData[]): CountyData[] {
    return countyData.sort((a, b) => {
        return b.Boosters - a.Boosters;
    });
}

export function sortByTotalVotes(countyData: CountyData[]): CountyData[] {
    return countyData.sort((a, b) => {
        return b.Total_Votes - a.Total_Votes;
    });
}

export function sortByWinnerPercentage(countyData: CountyData[]): CountyData[] {
    return countyData.sort((a, b) => {
        return b.Winner_Percentage - a.Winner_Percentage;
    });
}

export function sortByWinner(countyData: CountyData[]): CountyData[] {
    return countyData.sort((a, b) => {
        return a.Winner.localeCompare(b.Winner);
    });
}



