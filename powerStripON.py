#! python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox() # Open Firefox

browser.get('http://192.168.1.100/') # Navigate page to power strip login

userElem = browser.find_element_by_name('Username')
passwdElem = browser.find_element_by_name('Password')

userElem.send_keys('COSGC')
passwdElem.send_keys('GndSt@tion')

passwdElem.send_keys(Keys.ENTER)

onElem = browser.find_element_by_link_text('All Outlets ON')

onElem.click()

browser.quit()
