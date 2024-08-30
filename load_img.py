
import requests
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
def export_link(input_file, filename_img, filename_vid, driver):
    count = 0
    print("Exporting links...")
    list_line = []
    img_link_list = []
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            list_line.append(line.strip())

    for line in list_line:
        try:
            if line.startswith("https://mbasic.facebook.com/photo.php"):
                #change to www.facebook.com
                line = line.replace("https://mbasic.facebook.com", "https://www.facebook.com")
                driver.get(line)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                try:
                    #find img have attribute data-visualcompletion="media-vc-image"
                    imgs = soup.find_all("img", {"data-visualcompletion": "media-vc-image"})
                    for img in imgs:
                        load_img(img['src'],"images/" + filename_img)
                    count += 1
                except Exception as e:
                    print("Error image link: ", line)
                    print(e)
                    continue
            elif line.startswith("https://mbasic.facebook.com/video_redirect/"):
                try:
                    load_video(driver,"videos/" + filename_vid,line)
                    count += 1
                except Exception as e:
                    print("Error video link: ", line)
                    print(e)
                    continue
            if count % 100 == 0:
                print("Exported ", count, "posts")
        except Exception as e:
            print("Error link: ", e)
            continue

    print("Exported links")
    return img_link_list


def load_img(url, output_folder, minimum_size = 5000):
    directory = output_folder
    if not os.path.exists(directory):
        os.makedirs(directory)
    #Load the image
    response = requests.get(url)
    #Check the size of the image, if too small, ignore
    if len(response.content) < minimum_size:
        return
    #Save image
    with open(output_folder + "/img" + str(int(time.time())) + ".png", "wb") as f:
        f.write(response.content)

def load_video(driver,output_folder,url, minimum_size = 50000):
    driver.get(url)
    directory = output_folder
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    #Get the real video link
    url = driver.current_url
    # Tải video về
    response = requests.get(url)
    #check the size of the video, if too small, ignore
    if len(response.content) < minimum_size:
        print("Video too small or detected as a bot")
        return

    #save video
    with open(output_folder + "/video" + str(int(time.time())) + ".mp4", "wb") as f:
        f.write(response.content)
    
    print("Video" + str(int(time.time())) + ".mp4 saved")


# Test
# driver = webdriver.Chrome()
# from login import login
# driver = login(driver)
# # img_link_list = export_link("posts.txt", driver)

# export_link("posts.txt", driver)
# input("Press Enter to close the browser")
# driver.quit()