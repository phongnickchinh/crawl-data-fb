from login import login
from load_img import export_link
from crawl import get_timeline_page
from selenium import webdriver
import time


browser = webdriver.Chrome()
browser = login(browser, "https://mbasic.facebook.com")
time.sleep(5)
# read all link in followed_pages.txt
with open("followed_pages.txt", "r") as f:
    for line in f:
        line = line.replace("\n", "")
        print("Exporting ", line)
        get_timeline_page(line, browser)
        export_link("timeLine_"+line, "imgs_"+line, "vids_"+line,browser)
        print("Exported ", line)
        time.sleep(5)

browser.quit()
