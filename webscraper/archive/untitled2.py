# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 16:29:43 2019

@author: Alex
"""
import requests, re
import csv
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from urllib.parse import urljoin
start_url = 'https://clinicaltrials.gov/ct2/results?cond=&term=&cntry=&state=&city=&dist='

driver = webdriver.Firefox()
driver.get(start_url)


def make_soup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup

def get_links(url):
    soup = make_soup(url)
    a_tags = soup.find_all('a', href=re.compile("/ct2/show/NCT"))
    links = [urljoin(start_url, a['href'])for a in a_tags]  # convert relative url to absolute url
    return links

def get_trs(link):
    soup = make_soup(link)
    trs = soup.find_all('tr', class_="even")
    if not trs:
        print(link)
    else:
        for tr in trs:
            print(tr.text)

def next_page(url):

    try:
        link = driver.find_element_by_xpath("//div[contains(@id,'theDataTable_next')]")
#        //*[@id="theDataTable_next"]
    except NoSuchElementException:
        link = None
    return link.click()

if __name__ == '__main__':
    links = get_links(start_url)
    for link in links:
        get_trs(link)
        
    ########################## Alternative ####################################
    #    x = 1        # Outside of for loop
    #    study_button = driver.find_element_by_xpath('/html/body/div[4]/div[3]/div[2]/div[1]/div/div[2]/div[2]/table/tbody/tr[' + str(x) + ']/td[4]/a')
    #    study_button.click() #click link  
    #
    #    #increment the counter variable before starting the loop over
    #    x += 1
    ###########################################################################     
    
    ############## WebDriverException: TypeError: rect is undefined ###########
    #    action=ActionChains(driver)
    #    action.move_to_element(study_button)
    #    action.perform()
    ###########################################################################
        
    #    #Beautiful Soup grabs the HTML table on the page
    #    table = soup_level2.find_all('table')
    #    df = pd.read_html(str(table),header=0)
    #    df1 = pd.read_html('https://clinicaltrials.gov' + link['href'])
    ###########################################################################

    ################
        
        # /html/body/div[1]/div[2]
        # 

#        if len(soup_level2.find_all('div', class_="fsrwin")) != 0:
#        <div class="fsr_closeSticky fsr_closeButton"></div>
        
        
        
#        if len(soup_level2.find_all('td', headers="role")) != 0:
#            investigators = driver.find_element_by_xpath('/html/body/div[4]/div[4]/div[3]/div/div[7]/div[2]/div[10]').text
#        elif len(soup_level2.find_all('td', headers="role")) == 1:
#            investigators = driver.find_element_by_xpath('/html/body/div[4]/div[4]/div[3]/div/div[7]/div[2]/div[9]/table/tbody/tr').text
#        else:
#            investigators = ""
        
        #Giving the HTML table to pandas to put in a dataframe object
#        df_t = pd.read_html(str(text))
        
        
#with open("webscraper_output.csv", "w", encoding="utf-8") as csvfile:
#    csvwriter = csv.writer(csvfile, delimiter=",", lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
#    csvwriter.writerow(header)
#    for row in text_scrape:
        
        
#                ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                
#                popup_close_button = driver.find_element_by_class_name('fsr_closeSticky fsr_closeButton')
#                popup_close_button.click()
        
#                    try:
#                        contacts_and_locations = driver.find_element_by_xpath('/html/body/div[4]/div[4]/div[3]/div/div[7]/div[2]').text
#                        if "Contact:" not in contacts_and_locations:
#                            raise NoSuchElementException
#                    except NoSuchElementException:
#                        contacts_and_locations = driver.find_element_by_xpath('/html/body/div[4]/div[4]/div[3]/div/div[8]/div[2]').text
#                        if "Contact:" not in contacts_and_locations:
#                            raise NoSuchElementException
#                    except NoSuchElementException:
##                       #Check for contacts/locations expansion
##                        if len(soup_level2.find_all('img', src="/ct2/html/images/frame/plus.gif")) != 0:
##                        if "Study Locations" not in contacts_and_locations:
#                        contacts_and_locations = driver.find_element_by_xpath('/html/body/div[4]/div[4]/div[3]/div/div[7]/div[2]').text
#                        if "study locations" not in contacts_and_locations:
#                            raise NoSuchElementException
#                    except NoSuchElementException:
#                        contacts_and_locations = ""    