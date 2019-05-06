# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 12:35:36 2019

@author: Alex

Source code: https://medium.freecodecamp.org/better-web-scraping-in-python-with-selenium-beautiful-soup-and-pandas-d6390592e251
"""
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import csv
#import requests
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
#from selenium.common.exceptions import MoveTargetOutOfBoundsException
from selenium.webdriver.common.action_chains import ActionChains

url = 'https://clinicaltrials.gov/ct2/results?cntry=CA&city=Toronto&Search=Apply&recrs=a&age_v=&gndr=&type=&rslt='

# create a new Firefox session
driver = webdriver.Firefox()
driver.implicitly_wait(30)
driver.get(url)

# Selenium hands the page source to Beautiful Soup
soup_level1 = BeautifulSoup(driver.page_source, 'lxml')

# Setting the formatting of the dataframe & csv
header = ["nct_id", "Brief Summary", "Detailed Description", "Accepts Healthy Volunteers", 
          "Inclusion Criteria", "Exclusion Criteria", "Contacts", "Investigators"]
text_scrape = pd.DataFrame(columns = header)

# while loop traverses the next page of search results, stops when last page is reached
while len(soup_level1.find_all('a', id="theDataTable_next")[0]['class']) < 3:

    # soup the page again for each new page to gather the new set of links
    soup_level1 = BeautifulSoup(driver.page_source, 'lxml')
    
    # Beautiful Soup finds all Study links on the ClinicalTrials results page and the loop begins
    links = soup_level1.find_all('a', href=re.compile("/ct2/show/NCT"))
    main_window = driver.current_window_handle
    
    for link in links:
        
        print(link)
        print('\n')
        
        # Selenium visits each Study page in a new tab
        driver.execute_script("window.open();")
        driver.switch_to.window(driver.window_handles[1])
        driver.get('https://clinicaltrials.gov' + link['href'])
        
#        ##### test on individual page #######
#        temp_url = 'https://clinicaltrials.gov/ct2/show/NCT01597518?recrs=a&cntry=CA&city=Toronto&draw=75&rank=741'
#        driver.get(temp_url)
#        #####################################
        
        # Wait for page to sufficiently load
        time.sleep(.5)

        # while loop to check for popup
        while True:
            try:
                # Selenium hands of the source of the specific study page to Beautiful Soup
                soup_level2 = BeautifulSoup(driver.page_source, 'lxml')
                
                # Check validity of study page by seeing if the navigation dropdown exists
                if len(soup_level2.find_all('div', class_="tr-dropdown")) != 0:
                    
                    try:
                        brief_summary = driver.find_element_by_xpath('/html/body/div[4]/div[4]/div[3]/div/div[1]/div[2]/div[2]').text
                    except NoSuchElementException:
                        brief_summary = ""
                        
                    if len(soup_level2.find_all('a', id="detaileddesc")) != 0:    
                        detailed_description = driver.find_element_by_xpath('/html/body/div[4]/div[4]/div[3]/div/div[1]/div[2]/div[4]').text
#                       #Check for description expansion
#                    elif len(soup_level2.find_all('img', src="/ct2/html/images/frame/plus.gif")) != 0:
#                        expand_desc = driver.find_element_by_css_selector('[title*="Study Locations"]')
#                        expand_desc.click()
                    else:
                        detailed_description = ""

                    try:
                        eligibility_criteria = driver.find_element_by_xpath('/html/body/div[4]/div[4]/div[3]/div/div[6]/div[3]').text
                        if "Eligible" not in eligibility_criteria:
                            raise NoSuchElementException
                    except NoSuchElementException:
                        eligibility_criteria = driver.find_element_by_xpath('/html/body/div[4]/div[4]/div[3]/div/div[7]/div[3]').text
                        if "Eligible" not in eligibility_criteria:
                            raise NoSuchElementException
                    except NoSuchElementException:
                        eligibility_criteria = ""
                    
                    try:
                        contacts_and_locations = driver.find_element_by_xpath('/html/body/div[4]/div[4]/div[3]/div/div[7]/div[2]').text
                        if "Contact:" not in contacts_and_locations:
                            contacts_and_locations = driver.find_element_by_xpath('/html/body/div[4]/div[4]/div[3]/div/div[8]/div[2]').text
                            if "Contact:" not in contacts_and_locations:
                                contacts_and_locations = driver.find_element_by_xpath('/html/body/div[4]/div[4]/div[3]/div/div[7]/div[2]').text
#                               #Check for contacts/locations expansion, expand then collect?
#                                if len(soup_level2.find_all('img', src="/ct2/html/images/frame/plus.gif")) != 0:
                                if "study locations" not in contacts_and_locations:
                                    raise NoSuchElementException
                    except NoSuchElementException:
                        contacts_and_locations = ""         

                    nct_id = soup_level2.find_all('a', class_="tr-study-link")[-3].text
                    
                else:
                    brief_summary = ""
                    detailed_description = ""
                    eligibility_criteria = ""
                    contacts_and_locations = ""
                    nct_id = ""
                    
                # Quit popup check loop if successful
                break
            
            # Close popup and repeat while loop
            except NoSuchElementException:
                driver.switch_to.active_element.send_keys(Keys.ESCAPE)
        
        ##################### Eligibility Criteria split #######################
        accepts_search = re.search('Accepts Healthy Volunteers:   (.*)\n', eligibility_criteria)
        try:
            accepts_text = accepts_search.group(1)
        except AttributeError:
            accepts_text = "Unknown"

#        criteria_search = re.search('Criteria\n(.*)', eligibility_criteria, re.DOTALL)
#        try:
#            criteria_text = criteria_search.group()
#        except AttributeError:
#            criteria_text = ""
           
        # Problem with study NCT03846492: Need to separate the superset condition criteria
        # Above commented code is for taking whole criteria block
        
        inclusion_search = re.search('Inclusion Criteria:\n(.*)\nExclusion Criteria:', eligibility_criteria, re.DOTALL)
        try:
            inclusion_text = inclusion_search.group(1)
        except AttributeError:
            try:
                inclusion_search = re.search('Inclusion:\n(.*)\nExclusion', eligibility_criteria, re.DOTALL)
                inclusion_text = inclusion_search.group(1)
            except AttributeError:
                try:
                    inclusion_search = re.search('INCLUSION:\n(.*)\nEXCLUSION', eligibility_criteria, re.DOTALL)
                    inclusion_text = inclusion_search.group(1)
                except AttributeError:
                    try:
                        inclusion_search = re.search('Criteria\n(.*)\nExclusion', eligibility_criteria, re.DOTALL)
                        inclusion_text = inclusion_search.group(1)
                    except AttributeError:
                        inclusion_text = ""
        exclusion_search = re.search('Exclusion Criteria:\n(.*)', eligibility_criteria, re.DOTALL)
        try:
            exclusion_text = exclusion_search.group(1)
        except AttributeError:
            try:
                exclusion_search = re.search('Exclusion:\n(.*)\nInclusion' and 'Exclusion:\n(.*)', eligibility_criteria, re.DOTALL)
                exclusion_text = exclusion_search.group(1)
            except AttributeError:
                try:
                    exclusion_search = re.search('EXCLUSION:\n(.*)', eligibility_criteria, re.DOTALL)
                    exclusion_text = exclusion_search.group(1)
                except AttributeError:
                    exclusion_text = ""
        #######################################################################
        
        
        ########################### Contacts split ############################
        # Special case study NCT01597518: expand locations with contacts in each location
        # if no contact, search within locations for contact
        # if no investigator, search within locations for investigator
        contact_search = re.search('Contacts\n(.*)\nLocations', contacts_and_locations, re.DOTALL)
        try:
            contact_text = contact_search.group(1)
        except AttributeError:
            contact_text = ""
            
        investigator_search = re.search('Investigators\n(.*)', contacts_and_locations, re.DOTALL)
        try:
            investigator_text = investigator_search.group(1)
        except AttributeError:
            investigator_text = ""
        #######################################################################
        
        df = pd.DataFrame([[nct_id, brief_summary, detailed_description, accepts_text, inclusion_text,
                            exclusion_text, contact_text, investigator_text]], columns = header)
        text_scrape = pd.concat([text_scrape,df], ignore_index=True)
        
        # Ask Selenium to close the tab and go back to search results page
        driver.close()
        driver.switch_to.window(main_window)
    
    next_page_button = driver.find_element_by_id('theDataTable_next')
    next_page_button.click()
    time.sleep(1)

# End the Selenium browser session once last results page is reached
driver.quit()

text_scrape.to_csv('webscraper_output.csv', index=False)

