import { useState, useEffect } from 'react';
import { CountyData, DEFAULT_COUNTY_DATA } from './dto/CountyData';
import { queryAllCounties, queryCounty, queryStateCounties, parseStateCountyData } from './util/api';
import { States } from './constants'

import './App.css';

import highIncomeGraph from './images/high_income_political.jpg';
import lowIncomeGraph from './images/low_income_political.jpg';
import boxplotIncome from './images/boxplot_income.jpg';
import boxplotVaccination from './images/boxplot_vaccinated.jpg';
import scatterRepublican from './images/scatter_trump.jpg';
import scatterDemocrat from './images/scatter_biden.jpg';


import { sortByCounty, sortByPopulation, sortByIncome, sortByFullyVaccinated, sortByBoosterRate, sortByTotalVotes, sortByWinnerPercentage, sortByWinner } from './util/sort';

function App() {
  const [mapOptions, setMapOptions] = useState("income");
  const [filterOptions, setFilterOptions] = useState({ state: "", county: "" });
  const [counties, setStateCounties] = useState<string[]>([]);
  const [tableData, setTableData] = useState<CountyData[]>([DEFAULT_COUNTY_DATA]);
  const [tableSortOptions, setTableSortOptions] = useState("county");

  async function handleStateChange(event: { target: { value: any; }; }) {
    setFilterOptions({ state: event.target.value, county: "" });
    const data = await queryStateCounties(event.target.value);
    setTableData(data);
    setStateCounties(parseStateCountyData(data));
  }

  async function handleCountyChange(event: { target: { value: any; }; }) {
    setFilterOptions({ ...filterOptions, county: event.target.value });
    const data = await queryCounty(filterOptions.state, event.target.value);
    setTableData(data);
    setTableSortOptions("County");
  }

  async function handleCountyClear() {
    setFilterOptions({ ...filterOptions, county: "" });
    const data = await queryStateCounties(filterOptions.state);
    setTableData(data);
    setTableSortOptions("County");
  }

  async function handleStateClear() {
    setFilterOptions({ state: "", county: "" });
    const data = await queryAllCounties();
    setTableData(data);
    setTableSortOptions("County");
  }

  function sortTableByCounty() {
    const newTableData = sortByCounty(tableData);
    setTableData(newTableData);
    setTableSortOptions("County");
  }

  function sortTableByPopulation() {
    const newTableData = sortByPopulation(tableData);
    setTableData(newTableData);
    setTableSortOptions("Population");
  }

  function sortTableByVaccination() {
    const newTableData = sortByFullyVaccinated(tableData);
    setTableData(newTableData);
    setTableSortOptions("Fully_Vaccinated");
  }

  function sortTableByIncome() {
    const newTableData = sortByIncome(tableData);
    setTableData(newTableData);
    setTableSortOptions("Income");
  }

  function sortTableByBoosterRate() {
    const newTableData = sortByBoosterRate(tableData);
    setTableData(newTableData);
    setTableSortOptions("Boosters");
  }

  function sortTableByWinner() {
    const newTableData = sortByWinner(tableData);
    setTableData(newTableData);
    setTableSortOptions("Winner");
  }

  function sortTableByWinnerPercentage() {
    const newTableData = sortByWinnerPercentage(tableData);
    setTableData(newTableData);
    setTableSortOptions("Winner_Percentage");
  }

  function sortTableByTotalVotes() {
    const newTableData = sortByTotalVotes(tableData);
    setTableData(newTableData);
    setTableSortOptions("Total_Votes");
  }

  useEffect(() => {
    async function fetchData() {
      const response = await queryAllCounties();
      setTableData(response);
    }
    fetchData();
  }, []);

  return (
    <div>
      <h1 className='title'>REST API for Economic, Political, and COVID-19 Vaccination Data for U.S. Counties</h1>

      <h2 className='title'>Abstract</h2>
      <div className='box'>
      Accessible data is essential for promoting new discoveries and advancing current technologies. The purpose of this project was to construct a new data acquisition tool that makes evaluating and visualizing data simple and efficient. A REST API was created using Flask for running queries on a custom built database. The database included the population count, median income, outcome of the 2020 presidential election, and the percent of fully vaccinated people for United State counties. This information was selected to investigate common stereotypes in American society. This website was built to serve as an interface to the API. It provides several examples on how to visualize and explore the data and provides a graphical interface for querying the database. Please explore this page and try out the API!
      </div>

      <h2 className='title'>Examples of Visualizations</h2>
      <div className='grid'>
        <img alt='high income political graph' src={highIncomeGraph} />
        <img alt='low income political graph' src={lowIncomeGraph} />
        <img alt = 'scatter plot republican' src={scatterRepublican} />
        <img alt = 'scatter plot democrat' src={scatterDemocrat} />
        <img alt = 'boxplot income' src={boxplotIncome} />
        <img alt = 'boxplot vaccination' src={boxplotVaccination} />

      </div>

      <h2 className='title'>Interactive Maps</h2>
      <select value={mapOptions} onChange={e => setMapOptions(e.target.value)}>
        <option key='income' value="income">Median Income</option>
        <option key='vaccination' value="vaccination">Vaccination Rate</option>
        <option key='party' value="party">Political Party</option>
      </select>
      <iframe title='heatmap' src={`http://13.52.103.204:5000/map/${mapOptions}`} />

      <h2 className='title'>Rest API Query Tool</h2>
      <div className='flex-row'>
        <div className='flex-row'>
          <label>State
            <select value={filterOptions.state} onChange={handleStateChange}>
              {States.map(state => <option key={state} value={state}>{state}</option>)}
            </select>
            <button className='button' onClick={handleStateClear}>Reset</button>
          </label>
        </div>

        {
          filterOptions.state !== "" &&
          <div className='flex-row'>
            <label>County
              <select value={filterOptions.county} disabled={filterOptions.state === ""} onChange={handleCountyChange}>
                {counties?.map(county => <option key={county} value={county}>
                  {county.split(" ").slice(0, -1).join(" ")}
                </option>)}
              </select>
              <button className='button' onClick={handleCountyClear}>Reset</button>
            </label>
          </div>
        }
      </div>

      <div className='table-wrapper'>
        <table className='rest-table'>
          <thead>
            <tr>
              <th className='table-header'>State</th>
              <th
                className='table-header clickable'
                onClick={sortTableByCounty}>
                County
                {tableSortOptions === "County" ? <span>&#8593;</span> : null}
              </th>
              <th
                className='table-header clickable'
                onClick={sortTableByPopulation}>
                Population
                {tableSortOptions === "Population" ? <span>&#8593;</span> : null}
              </th>
              <th
                className='table-header clickable'
                onClick={sortTableByIncome}>
                Median Income
                {tableSortOptions === "Income" ? <span>&#8593;</span> : null}
              </th>
              <th
                className='table-header clickable'
                onClick={sortTableByVaccination}>
                Fully Vaccinated %
                {tableSortOptions === "Fully_Vaccinated" ? <span>&#8593;</span> : null}
              </th>
              <th
                className='table-header clickable'
                onClick={sortTableByBoosterRate}>
                Received Booster %
                {tableSortOptions === "Boosters" ? <span>&#8593;</span> : null}
              </th>
              <th
                className='table-header clickable'
                onClick={sortTableByWinner}>
                Winner
                {tableSortOptions === "Winner" ? <span>&#8593;</span> : null}
              </th>
              <th
                className='table-header clickable'
                onClick={sortTableByWinnerPercentage}>
                Win %
                {tableSortOptions === "Winner_Percentage" ? <span>&#8593;</span> : null}
              </th>
              <th
                className='table-header clickable'
                onClick={sortTableByTotalVotes}>
                Voters
                {tableSortOptions === "Total_Votes" ? <span>&#8593;</span> : null}
              </th>
            </tr>
          </thead>
          <tbody>
            {
              tableData?.map((row, i) => {
                return (
                  <tr className='table-row' key={i}>
                    <td className='table-data'>{row?.State || ""}</td>
                    <td className='table-data'>{row?.County || ""}</td>
                    <td className='table-data'>{row?.Population || ""}</td>
                    <td className='table-data'>{row?.Income || ""}</td>
                    <td className='table-data'>{row?.Fully_Vaccinated || ""}</td>
                    <td className='table-data'>{row?.Boosters || ""}</td>
                    <td className='table-data'>{row?.Winner || ""}</td>
                    <td className='table-data'>{row?.Winner_Percentage || ""}</td>
                    <td className='table-data'>{row?.Total_Votes || ""}</td>
                  </tr>
                )
              })
            }
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;