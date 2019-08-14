# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 21:35:39 2019

@author: Andrew_Boles

Description: This file allows the user to download a saved insight from Handshake. Requires username and password input.
            Note that the path to chrome_driver and download_folder also has to be specified.
"""
import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


handshake_username = input("Enter username: ")
handshake_password = input("Enter password: ")
desired_filename = input("Enter filename for download: ")
# url will change based upon need, below looks at active student profile completions
handshake_insights_url = "https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vc3R1ZGVudHM_cWlkPTZ5YVJEMmRXV0JsSENTTGJQVGNya2cmZW1iZWRfZG9tYWluPWh0dHBzOiUyRiUyRmFwcC5qb2luaGFuZHNoYWtlLmNvbSZ0b2dnbGU9Zmls"
chrome_driver = "Path\\to\\Chrome\\Driver\\On\\PC\\chromedriver.exe"
download_folder = "Path\\to\\Downloads\\"

def insight_login(driver, url, username, password):
    driver.get(url)
    # click login with email
    driver.find_element_by_id("email-address").send_keys(username, Keys.ENTER)
    # click login with alternate login (not sso)
    driver.find_element_by_class_name("alternate-login-link").click()
    # enter password 
    driver.find_element_by_name("password").send_keys(password, Keys.ENTER)
    while "Insights Explorer" not in driver.page_source:
        time.sleep(1)
    print("successfully logged into page")
    return

# Keep drivers open while waiting for downloads to finish.
def wait_for_file(filename):
    tmp = filename + ".crdownload"
    while not os.path.isfile(filename) and os.path.isfile(tmp):
        time.sleep(5)
        print("Waiting for " + filename + " to download.")
    return
    
def download_insight(driver, file_name):
    # switch to insight frame to find gear button to download insights
    driver.switch_to.frame(driver.find_element_by_id("insights-iframe"))
    # necessary to explicitly wait for insight to complete 
    WebDriverWait(driver, 90).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="lk-embed-container"]/lk-explore-dataflux/lk-explore-header/div[2]/div[2]/div/i')))
    # click the gear button
    driver.find_element_by_xpath('//*[@id="lk-embed-container"]/lk-explore-dataflux/lk-explore-header/div[2]/div[2]/div/i').click()
    # click the "Download..." choice in gear button drop down list
    driver.find_element_by_xpath('//*[@id="lk-embed-container"]/lk-explore-dataflux/lk-explore-header/div[2]/div[2]/ul/li[2]/a').click()
    # clear the previous filename and input file_name
    driver.find_element_by_xpath('//*[@id="lk-layout-embed"]/div[4]/div/div/form/div[2]/div[4]/div/div[2]/label/input').click()
    filename = driver.find_element_by_xpath('//*[@id="qr-export-modal-custom-filename"]')
    filename.clear()
    filename.send_keys(file_name)
    # click download button
    driver.find_element_by_xpath('//*[@id="qr-export-modal-download"]').click()
    print("File: " + file_name + " is downloading.")
    return

driver = webdriver.Chrome(chrome_driver)
driver.implicitly_wait(10) # causes everything to wait 10 seconds (max) for each call to driver
insight_login(driver, handshake_insights_url, handshake_username, handshake_password)
download_insight(driver, desired_filename)
wait_for_file(download_folder + desired_filename)
print("File: " + desired_filename + " successfully downloaded.")
driver.close()