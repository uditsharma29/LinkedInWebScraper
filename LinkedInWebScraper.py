# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 10:45:56 2021

@author: udits
"""
#from linkedin_scraper import Person, actions, Company
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import csv
import os
import requests

def login(email, password):
    email = email
    password = password
    
    driver.maximize_window()
    driver.get('https://www.linkedin.com/login')
    time.sleep(3)
    driver.find_element_by_id('username').send_keys(email)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_id('password').send_keys(Keys.RETURN)
    
def scroll(in_scroll, fin_scroll, scrollTime):
    start = time.time()

    # will be used in the while loop
    initialScroll = in_scroll
    finalScroll = fin_scroll
    while True:
        driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
        # this command scrolls the window starting from
        # the pixel value stored in the initialScroll 
        # variable to the pixel value stored at the
        # finalScroll variable
        initialScroll = finalScroll
        finalScroll += 200

        # we will stop the script for 3 seconds so that 
        # the data can load
        time.sleep(2)
        # You can change it as per your needs and internet speed

        end = time.time()

        # We will scroll for 10 seconds.
        # You can change it as per your needs and internet speed
        if round(end - start) > scrollTime:
            break

def fetch_profiles(number):
    all_data = []
    driver.execute_script("document.body.style.zoom='70%'")
    #Scroll to load required number of profiles
    scroll(0,200, number*1.5)
    time.sleep(1)
    
    #Fetch and store all profile links on the page
    links = [x.get_attribute('href') for x in driver.find_elements_by_css_selector("div.scaffold-finite-scroll__content a")]
    
    for i, element in zip(range(0, number*2, 2), links[::2]):
        #get current profile
        driver.get(links[i]) 
        
        #Wait for page load
        time.sleep(0.75)
        
        #Fetch page source code
        emp_src = driver.page_source
        
        #parse through Beautiful soup
        emp_soup = bs(emp_src, 'lxml')
        
        #Find header
        header = emp_soup.find('div', {'class': 'mt2 relative'})
        
        #Extract first name, last name, headline and location from header
        fname, lname = header.find('h1').get_text().split(" ")[0], ' '.join(header.find('h1').get_text().split(" ")[1:])
        headline = header.find('div', {'class': 'text-body-medium break-words'}).get_text().strip()
        location = header.find('span', {'class': 'text-body-small inline t-black--light break-words'}).get_text().strip()
        
        #Append this information to list of list
        all_data.append([fname, lname, headline, location])
        
        #Locate image wrapper, download and save to disk. If Image is not present, proceed without doing anything
        img_wrapper = emp_soup.find('div', {'class': 'pv-top-card__non-self-photo-wrapper ml0'})
        pic = img_wrapper.find('img')
        try:
            r = requests.get(pic['src']).content
            pic['alt'] = pic['alt'].replace('/', ' ')
            with open("images/"+pic['alt']+".jpg","wb+") as f:
                  f.write(r)
            f.close()
        except:
            pass
        
    headers = ['First_Name','Last_Name','Headline','Location']
    write_to_csv(headers, all_data)

def write_to_csv(headers, data):
    
    with open('employees.csv', 'w', newline = '') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(headers)
        # write all data
        writer.writerows(data)
 
if __name__ == "__main__":
    
    ### YOUR CHROMEDRIVER PATH HERE ###
    driver_path = "chromedriver_win32/chromedriver.exe"
    
    #Your username and password here
    email = # username here #
    password = # Password here #
    
    #Number of profiles to fetch (>0)
    number = 100
    
    os.mkdir('images/')
    driver = webdriver.Chrome(driver_path)
    
    login(email, password)
    
    driver.get("https://www.linkedin.com/company/hubspot/")
    
    time.sleep(2)
    
    people_tab = driver.find_element_by_xpath('//a[contains(@href,"/company/hubspot/people")]')
    
    people_tab.click()
    
    fetch_profiles(number)


    
