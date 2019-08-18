# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 08:22:35 2019

@author: Andrew_Boles
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


handshake_username = "andrew_boles@baylor.edu" #input("Enter username: ")
handshake_password = "#Remington009" #input("Enter password: ")
# url will change based upon need, below looks at active student profile completions
handshake_manage_student_url = "https://baylor.joinhandshake.com/students"
chrome_driver = "C:\\Users\\andrew_boles\\AppData\\Local\\ChromeDriver\\chromedriver.exe"

desired_note = "Write note here."
student_email_list = []

def get_student_name(email):
    return email.split('@')[0].split('_')

def login(driver, url, username, password):
    driver.get(url)
    # click login with email
    driver.find_element_by_xpath('//*[@id="ui-id-1"]/div[1]/div/div/a').click()
    driver.find_element_by_id("non-sso-email-address").send_keys(username, Keys.ENTER)
    # click login with alternate login (not sso)
    driver.find_element_by_class_name("alternate-login-link").click()
    # enter password 
    driver.find_element_by_name("password").send_keys(password, Keys.ENTER)
    print("successfully logged into page")
    return
    
beginning_time = time.time()
driver = webdriver.Chrome(chrome_driver)
driver.implicitly_wait(10) # causes everything to wait 10 seconds (max) for each call to driver
login(driver, handshake_manage_student_url, handshake_username, handshake_password)
# after logging in, loop through each email address and add correct note to student
for s in student_email_list:
    driver.find_element_by_xpath('//*[@id="react-select-2--value"]/div[1]').click()
    driver.find_element_by_xpath('//*[@id="global-search"]').send_keys(get_student_name(s)[0] + " " + get_student_name(s)[1])
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="global-search"]').send_keys(Keys.ENTER)
    driver.find_element_by_xpath('//*[@id="main"]/div[1]/div[2]/div/div[1]/div/div/div[2]/div[2]/div[1]/div[3]/div/div/a[3]/span').click()
    driver.find_element_by_xpath('//*[@id="notes-modal"]/div[2]/div/div[2]/form/textarea').send_keys(desired_note)
    driver.find_element_by_xpath('//*[@id="add-new-note"]').click()
    print("Note added to: " + s)
    driver.get(handshake_manage_student_url)
driver.close()
ending_time = time.time()
print("Student notes added. Time taken: " + str(ending_time - beginning_time) + " seconds.")