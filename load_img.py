
import requests
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
def export_link(input_file, filename_img, filename_vid, driver):
    count = 0
    found = False
    print("Exporting links...")
    list_line = []
    img_link_list = []
    with open("text_file/line_got.txt", "r") as file:
        last_line = file.readlines()
        if last_line:
            last_line = last_line[-1].strip()
        else:
            print("line_got is empty")
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            if found:
                list_line.append(line.strip())
            if line.strip() in last_line:
                found = True

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
                        load_img(img['src'],"assets/images/" + filename_img)
                    count += 1
                    if count % 10 == 0:
                        with open("text_file/line_got.txt","a") as f:
                            line = line.replace("https://www.facebook.com", "https://mbasic.facebook.com")
                            f.write(line+"\n")
                        if count %100==0:
                            print("Exported ", count, "posts")
                except Exception as e:
                    print("Error image link: ", line)
                    print(e)
                    continue
            elif line.startswith("https://mbasic.facebook.com/video_redirect/"):
                try:
                    load_video(driver,"assets/videos/" + filename_vid,line)

                    count += 1
                    if count % 10 == 0:
                        with open("text_file/line_got.txt","a") as f:
                            line = line.replace("https://www.facebook.com", "https://mbasic.facebook.com")
                            f.write(line+"\n")
                        if count %100==0:
                            print("Exported ", count, "posts")
                except Exception as e:
                    print("Error video link: ", line)
                    print(e)
                    continue

        except Exception as e:
            print("Error link: ", e)
            continue

    print("Exported links")
    return img_link_list


def load_img(url, output_folder,file_name = "", minimum_size = 5000):
    directory = output_folder
    if not os.path.exists(directory):
        os.makedirs(directory)
    #Load the image
    response = requests.get(url, stream=True, allow_redirects=False)
    #Check the size of the image, if too small, ignore
    if len(response.content) < minimum_size:
        return
    #Save image
    if file_name == "":
        file_name = str(int(time.time()))
    with open(output_folder + "/img" + file_name + ".jpg", "wb") as f:
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