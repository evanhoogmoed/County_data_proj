import { CountyData } from "../dto/CountyData";

export async function queryAllCounties() {
    let query = `http://localhost:5000/api`;
    const result = await fetch(query);
    return result.json();
}

export async function queryStateCounties(state: string) {
    let query = `http://localhost:5000/api/${state}`;
    const result = await fetch(query);
    return await result.json();
}

export async function queryCounty(state: string, county: string) {
    let query = `http://localhost:5000/api/${state}/${county}`;
    const result = await fetch(query);
    return await result.json();
}

export function parseStateCountyData(countyData: CountyData[]): string[] {
    let counties: string[] = [];
    countyData.forEach((county: CountyData) => {
        if (counties.indexOf(county.County) === -1) {
            counties.push(county.County);
        }
    });
    return counties;
}