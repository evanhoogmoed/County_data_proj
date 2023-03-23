CREATE TABLE IF NOT EXISTS economics (
    index INT NOT NULL AUTO_INCREMENT,
    County VARCHAR(255),
    State VARCHAR(255),
    Population INT,
    Income DECIMAL(10,2),
    State_Abrev VARCHAR(2),
    FIPS_Code double,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS politics (
    index INT NOT NULL AUTO_INCREMENT,
    Year INT,
    State VARCHAR(255),
    State_Abrev VARCHAR(2),
    County VARCHAR(255),
    Democrat INT,
    Republican INT,
    Other INT,
    Winner VARCHAR(255),
    Total_Votes INT,
    FIPS_Code double,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS vaccines (
    index INT NOT NULL AUTO_INCREMENT,
    County VARCHAR(255),
    State_Abrev VARCHAR(2),
    Fully_Vaccinated double,
    Boosters double,
    FIPS_Code double,
    PRIMARY KEY (id)
);

-- Join all the tables together by FIPS_Code
SELECT
    e.State,
    p.County,
    e.Income,
    e.Population,
    v.Fully_Vaccinated,
    v.Boosters,
    p.Winner,
    p.Total_Votes,
    ROUND((GREATEST(p.Democrat, p.Republican, p.Other) / p.Total_Votes) * 100, 1) AS Winner_Percentage
FROM
    economics e
    INNER JOIN politics p ON e.FIPS_Code = p.FIPS_Code
    INNER JOIN vaccines v ON e.FIPS_Code = v.FIPS_Code
WHERE
    p.State = 'California'
ORDER BY
    e.State,
    p.County;


-- Grab only the counties in all the tables
SELECT e.County, p.County, v.County
FROM economics e
INNER JOIN politics p ON e.FIPS_Code = p.FIPS_Code
INNER JOIN vaccines v ON e.FIPS_Code = v.FIPS_Code;

-- Count the number of counties in each table
SELECT COUNT(e.County) AS Economics_Count, COUNT(p.County) AS Politics_Count, COUNT(v.County) AS Vaccines_Count
FROM economics e
INNER JOIN politics p ON e.FIPS_Code = p.FIPS_Code
INNER JOIN vaccines v ON e.FIPS_Code = v.FIPS_Code;

-- Give me the join that will give me the counties in all the tables
SELECT e.County, p.County, v.County
FROM economics e
INNER JOIN politics p ON e.FIPS_Code = p.FIPS_Code
INNER JOIN vaccines v ON e.FIPS_Code = v.FIPS_Code;

-- find counties that are in politics but not in economics or vaccines
SELECT p.County
FROM politics p
LEFT JOIN economics e ON p.FIPS_Code = e.FIPS_Code
LEFT JOIN vaccines v ON p.FIPS_Code = v.FIPS_Code
WHERE e.County IS NULL
AND v.County IS NULL;

-- Grab all info about kalawao county
SELECT *
FROM economics e
INNER JOIN politics p ON e.FIPS_Code = p.FIPS_Code
INNER JOIN vaccines v ON e.FIPS_Code = v.FIPS_Code
WHERE e.County = 'Kalawao';

-- find average income for counties that voted for trump
SELECT AVG(e.Income)
FROM economics e
INNER JOIN politics p ON e.FIPS_Code = p.FIPS_Code
WHERE p.Winner = 'donald j trump';

-- find average income for counties that voted for biden
SELECT AVG(e.Income)
FROM economics e
INNER JOIN politics p ON e.FIPS_Code = p.FIPS_Code
WHERE p.Winner = 'joseph r biden jr';

-- find the county with the longest county name
SELECT e.County, e.State, LENGTH(e.County) AS County_Length
FROM economics e
ORDER BY County_Length DESC
LIMIT 1;
