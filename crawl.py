#mục tiêu của chương trình là đăng nhập vào facebook và lấy danh sách bạn bè
#sử dụng cookie để đăng nhập
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from login import login

# Khởi tạo trình điều khiển cho trình duyệt (ví dụ: Chrome)
driver = webdriver.Chrome()

# Đăng nhập vào Facebook
driver = login(driver)

# get friends list
def get_list_friends(driver):
    #open list friends
    driver.get("https://mbasic.facebook.com/profile.php?v=friends")
    #wait till the page is loaded
    time.sleep(2)
    count = 0
    friends = []
    #find all elements with tag a, class = ch
    while True:
        friends = driver.find_elements(By.CSS_SELECTOR, "td.w.t a")
        with open("friends.txt", "a", encoding="utf-8") as f:
            for friend in friends:
                #get text and link of each friend
                f.write(friend.text + ":  ") + f.write(friend.get_attribute("href") + "\n")
                count += 1

        if len(friends) < 24:
            break
        #click see more friends is a element which í child of div with id = m_more_friends
        try:
            more_friends_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div#m_more_friends a"))
            )
            more_friends_button.click()
            print("Loading more friends...")
        except:
            print("Error when loading more friends")
            break
    print("Total friends: ", count)


#get newfeed posts
def get_post_newfeed(driver):
    try:

        #open newfeed
        driver.get("https://mbasic.facebook.com")
        time.sleep(2)
        while True:
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")
            try:
                #newfeeds maybe in div with id = m_news_feed_stream or root
                posts = soup.find("div", id="m_news_feed_stream")
                if posts is None:
                    posts = soup.find("div", id="root")
                if posts is None:
                    print("Cant find newfeed div")
                    break
                section = posts.find("section")

                #find all articles in section, each article is a post
                posts = section.find_all("article", recursive=False)
                if posts is not None:
                    with open("posts.txt", "a", encoding="utf-8") as f:
                        for post in posts:
                            #find a tag have text include "Comment" (example "32 Comment", "Comment", "Comment 1")
                            a_tag = post.find("a", text=lambda text: text and "omment" in text)
                            #a link hae alot unnecessary characters, we only need a part of it, cut string when meet the second "&"
                            link =a_tag['href'] if a_tag is not None else ""
                            post_link = "https://mbasic.facebook.com" + link[:link.find("&", link.find("&")+1)]
                            print(post_link)
                            # find div with tag header, this div contains poster's name
                            poster_div = post.find("header")
                            poster = poster_div.get_text(strip=True) if poster_div is not None else "Unknown"
                            # find text content of post, this div is next sibling of div with poster's name
                            text = poster_div.find_next_sibling("div").get_text(strip=True) if poster_div is not None else ""
                            try:
                                #find all images in post
                                list_img = poster_div.find_next_sibling("div").find_next_sibling("div")
                                list_img = list_img.find_all('a')
                                picture = ""
                                for img in list_img:
                                    picture += "https://mbasic.facebook.com" + img['href'][:img['href'].find("&", img['href'].find("&")+1)] + "\n"
                            except:
                                picture = ""
                            f.write(post_link + "\n" + poster + "\n" + text + "\n" + picture + "\n")
                            
                #click see more posts is a element which í child of div with id = m_show_more_pager
                try:
                    driver.get("https://mbasic.facebook.com" +  section.find_next_sibling("a").get('href'))
                except:
                    print("Error when loading more posts")
                    break

            except Exception as e:
                print("Error when extracting posts")
                print(e)
                break
    except:
        print("Fucntion get_post_newfeed error")


get_post_newfeed(driver)
input("Press Enter to continue...")
driver.quit()