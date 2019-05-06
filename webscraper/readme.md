# Python webscraper for gathering clinical trial information from a website

This repository contains a script made to gather information from clinicaltrials.gov.

---------------------------------------------------------------------------------------------------------

#### Author: Alex Yau

---------------------------------------------------------------------------------------------------------

The information of interest is specific information from individual clinical trials that are 
currently recruiting study participants. High importance sections include contact information,
recruitment status, and inclusion/exclusion criteria for participating in the study. 

This information was contained within drill-down links in a list of search results.
The script uses BeautifulSoup4 and Selenium to navigate the html elements within the page,
and open a new window for each drill-down link to scrape the data of interest.

Many of these sections were formatted in a non-standard way, so this script was built to include 
exceptions to catch all of those outliers. There is also a function to catch and close popups which 
appear randomly.