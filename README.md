# ** Topos_interview_assignment **

* Description: Write a scraper in either python or NodeJS to collect data from Wikipedia about the top cities in the United States. The fields you collect, as well as the volume of data is up to you, but ideally you add additional data beyond the initial table, such as data found on the individual city pages, or other sources of your choice. The final format should be a CSV file that is ready to be uploaded to a BigQuery table. Please read Bigquery’s Manual to prepare your CSV in the right format. Intermediary steps, environments or processes necessary to run the scraper should be documented in code as well as a Readme.md and hosted on github in a repo devoted to this assignment. 

## I bulid this web scraping pipline with python, pandas and beautifulsoup. Create a main table from wiki link: https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population, search cities' founded date and time zone information from sub-links in this table and add these information to the main table.

## Steps to run this script:
## 1. Download this script and pip3 install required packages, then cd into that folder;
## 2. run: python3 Wensong_Liu_assignment.py in command line and wait for results(need a little time to run this script).
