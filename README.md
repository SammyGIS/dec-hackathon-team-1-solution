## Project Overview
This project involves extracting country data from a public REST API, transforming the data, loading it into a database, and analyzing it to gain insights. The data is used to answer specific analytical questions and visualize the results in a dashboard.

## Data Source
- REST API: [REST Countries](https://restcountries.com/v3.1/all)

## Extracted Fields
- Country Name
- Independence
- United Nation Member
- Start of Week
- Official Country Name
- Common Native Name
- Currency Code
- Currency Name
- Currency Symbol
- Country Code (IDD)
- Capital
- Region
- Sub Region
- Languages
- Area
- Population
- Continents

## Architecture Diagram
![alt text](project_architecture.png)

## Analytical Questions
1. How many countries speak French?
2. How many countries speak English?
3. How many countries have more than 1 official language?
4. How many countries' official currency is Euro?
5. How many countries are from Western Europe?
6. How many countries have not yet gained independence?
7. How many distinct continents and how many countries from each?
8. How many countries' start of the week is not Monday?
9. How many countries are not United Nation members?
10. How many countries are United Nation members?
11. Least 2 countries with the lowest population for each continent
12. Top 2 countries with the largest area for each continent
13. Top 5 countries with the largest area
14. Top 5 countries with the lowest area

## Visualization
The results are visualized using a suitable tool such as Tableau, Power BI, or Plotly.

## Project Structure


## Getting Started
1. Clone the repository.
2. Install required dependencies.
3. Run the scripts in the order of extraction, loading, analysis, and dashboard.

## Dependencies
- requests
- pandas


## License
This project is licensed under the MIT License.
