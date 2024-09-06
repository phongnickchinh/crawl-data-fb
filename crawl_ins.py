import time
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from login import login, login_w_keys
from load_img import export_link
from selenium.webdriver.chrome.service import Service



def turn_off_first_popup(browser):
    #find a button have text "Not Now"
    xpath = "//button[text()='Not Now']"
    try:
        not_now_button = browser.find_element(By.XPATH, xpath)
        not_now_button.click()
        return True
    except Exception as e:
        print("Error: ", e)
    return False

def get_all_following(browser, username= "zwindy_412"):
    try:
        browser.get("https://www.instagram.com/"+ username)
        time.sleep(2)
        #find the following a tag, have text "following", href = /username/following/, role = link
        #find main tag
        main_tag = browser.find_element(By.TAG_NAME, "main")
        header_tag = main_tag.find_element(By.TAG_NAME, "header")
        third_section_tag = header_tag.find_elements(By.TAG_NAME, "section")[2]
        li_tag = third_section_tag.find_elements(By.TAG_NAME, "li")[2]
        a_tag = li_tag.find_element(By.TAG_NAME, "a")
        #click the a tag
        a_tag.click()
        time.sleep(2)

        #wwhen the pop up appear, you hae to move the mouse to the pop up so you can scroll it, it in the center of the screen
        #find div dialog
        dialog =browser.find_element(By.XPATH, "//div[@role='dialog']")
        #find the closest child div of the dialog
        divs = dialog.find_elements(By.XPATH, "./*")
        while True:
            try:
                    
                #find all child of the select div until have more than 1 child
                #if first div is empty, then continue with the next div
                for div in divs:
                    if div.get_attribute("innerHTML") == "":
                        #remove the empty div
                        divs.remove(div)
                        continue
                if len(divs) > 1:
                    break
                divs = divs[0].find_elements(By.XPATH, "./*")
            except Exception as e:
                print("Error: ", e)
                break

        print(len(divs))
        inside_div = divs[-1]
        #in ra chiều cao của div
        print(inside_div.size)
        for i in range(2):
            inside_div= inside_div.find_element(By.XPATH, "./*")
            print(inside_div.size)
        print(inside_div.get_attribute("innerHTML"))
        #TODO: scroll the div, will be done tongiht
        time.sleep(5000)

    except Exception as e:
        print("Error: ", e)
        return None


# Đường dẫn đến ChromeDriver
chrome_path = r"C:\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"
service = Service(chrome_path)
# Create Chromeoptions instance 
options = webdriver.ChromeOptions() 
options.add_argument("--disable-blink-features=AutomationControlled") 
options.add_experimental_option("excludeSwitches", ["enable-automation"])  
options.add_experimental_option("useAutomationExtension", False) 

driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window() #maximize the window
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")




#login to instagram
browser = login(driver, "https://www.instagram.com/")
time.sleep(2)
turn_off_first_popup(browser)

print(get_all_following(browser, "zwindy_412"))
#clean all cache
browser.delete_all_cookies()
browser.quit()


