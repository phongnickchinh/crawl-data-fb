
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
def export_link(file_name, driver):
    list_line = []
    img_link_list = []
    with open(file_name, "r", encoding="utf-8") as f:
        for line in f:
            list_line.append(line.strip())

    for line in list_line:
        try:
            if line.startswith("https://"):
                driver.get(line)
        except Exception as e:
            print("Error when getting link: ", e)
            continue
            #tìm thẻ img
        soup = BeautifulSoup(driver.page_source, "html.parser")
        try:
            imgs = soup.find_all("img")
            #lấy các thuộc tính của thẻ img có src bằng đầu bằng https://scontent
            for img in imgs:
                src= img.get("src")
                if src.startswith("https://scontent"):
                    load_img(src)
                    img_link_list.append(src)
        except Exception as e:
            print("Error when getting image link: ", e)
            continue

    return img_link_list
def load_img(url):

    # Tải ảnh về
    response = requests.get(url)
    #@kiểm tra dung lượng ảnh để loại bỏ ảnh quá nhỏ (các icon chẳng hạn), những ảnh nhỏ hơn 5kb sẽ không được lưu
    if len(response.content) < 5000:
        return
    
    # Lưu ảnh vào file trong thư mục hiện tại, đặt tên là image + thời gian tính đến giây
    with open("image/image" + str(int(time.time())) + ".png", "wb") as f:
        f.write(response.content)


# Test
driver = webdriver.Chrome()
from login import login
driver = login(driver)
img_link_list = export_link("posts.txt", driver)

input("Press Enter to close the browser")
driver.quit()