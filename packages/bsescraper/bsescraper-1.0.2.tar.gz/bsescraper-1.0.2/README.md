# BSE India Data Scraping Library

## Overview

This Python library provides functions to scrape data from the BSE India website. It covers various functionalities such as retrieving corporate announcements, gainer/loser data for the market and specific groups, fetching index data, getting historical stock data, and more.

## Installation

To use this library, you need to have Python installed. You can install the library using pip:


pip install bsescraper

# Available Functions

## Corporate Announcements

get_corporate_ann(code(int), category(string), startdate, enddate) date format as "dd/mm/yyyy"

get_corporate_ann_keywords(code(int),keywords(list of strings),category(string), startdate, enddate)

## Gainer/Loser Data (Market)

GainerLoserDataMarket(type, order(0,2,5))

## Gainer/Loser Data (Group)

GainerLoserDataGroup(type, group, order(0,2,5))

## Get Index Data

get_index(category)

## Get Stock Data

get_stock_data(security code, startdate, enddate) date format as "dd/mm/yyyy"

## Get Security Code

get_code(Security Name)

## Top Turnovers

top_turnovers(num)

## Convert to DataFrame

dataframe(dictionary)

## Save DataFrame to CSV

save(df, name)

## Library Version

version()

## Library Description

description()

## Available Functions

functions()