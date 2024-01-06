# BSE India Data Scraping Library

## Overview

This Python library provides functions to scrape data from the BSE India website. It covers various functionalities such as retrieving corporate announcements, gainer/loser data for the market and specific groups, fetching index data, getting historical stock data, and more.

## Installation

To use this library, you need to have Python installed. You can install the library using pip:


pip install bsescraper

# Available Functions

1. Corporate Announcements

get_corporate_ann(code, category, startdate, enddate)

2. Gainer/Loser Data (Market)

GainerLoserDataMarket(type, order)

Gainer/Loser Data (Group)

GainerLoserDataGroup(type, group, order)

3. Get Index Data

get_index(category)

4. Get Stock Data

get_stock_data(code, startdate, enddate)

5. Get Scrip Code

get_code(name)

6. Top Turnovers

top_turnovers(num)

7. Convert to DataFrame

dataframe(dictionary)

8. Save DataFrame to CSV

save(df, name)

9. Library Version

version()

10. Library Description

11. description()

Available Functions

functions()