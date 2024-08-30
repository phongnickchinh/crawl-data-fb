#mục tiêu của chương trình là đăng nhập vào facebook và lấy danh sách bạn bè
#sử dụng cookie để đăng nhập
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from login import login
from load_img import export_link

# Khởi tạo trình điều khiển cho trình duyệt (ví dụ: Chrome)
driver = webdriver.Chrome()
# Đăng nhập vào Facebook
driver = login(driver,"https://www.facebook.com")

# get friends list of a user
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

#get newfeed posts of a user or a page manager
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

# get_timeline of a page
def get_timeline_page(driver, pagename):
    try:
        page_link = "https://mbasic.facebook.com/" + pagename + "?v=timeline"
        driver.get(page_link)
        time.sleep(2)
        count = 0
        lastest_post_link = "fsdfsdfdsfdsfsd"
        while True:
            try:
                soup = BeautifulSoup(driver.page_source, "html.parser")

                feed = soup.find("div", id="structured_composer_async_container")
                section = feed.find("section")
                list_posts = section.find_all("article", recursive=False)

                with open("timeLine_" + pagename + ".txt", "a", encoding="utf-8") as f:
                    for post in list_posts:
                        try:

                            #find a tag have text include "Comment" (example "32 Comment", "Comment", "Comment 1")
                            a_tag = post.find("a", text=lambda text: text and "omment" in text)
                            #a link hae alot unnecessary characters, we only need a part of it, cut string when meet the second "&"
                            link =a_tag['href'] if a_tag is not None else ""
                            post_link = "https://mbasic.facebook.com" + link[:link.find("&", link.find("&")+1)]
                            if post_link == lastest_post_link:
                                break
                            if count == 0:
                                lastest_post_link = post_link
                            print(post_link)
                            # find div with tag header, this div contains poster's name
                            poster_div = post.find("header")
                            poster = poster_div.get_text(strip=True) if poster_div is not None else "Unknown"
                            # find text content of post, this div is next sibling of div with poster's name
                            text = poster_div.find_next_sibling("div").get_text(strip=True) if poster_div is not None else ""
                            count += 1
                            try:
                                #find all images in post
                                list_img = poster_div.find_next_sibling("div").find_next_sibling("div")
                                list_img = list_img.find_all('a')
                                picture = ""
                                for img in list_img:
                                    picture += "https://mbasic.facebook.com" + img['href'][:img['href'].find("&", img['href'].find("&")+1)] + "\n"
                            except:
                                picture = ""
                            f.write(str(count) + "\n")
                            f.write(post_link + "\n" + poster + "\n" + text + "\n" + picture + "\n")
                        except Exception as e:
                            print("Error when extracting posts")
                            print(e)
                            continue
                
                #click see more posts is a element which í child of div with id = m_show_more_pager
                try:
                    see_more_div = section.find_next_sibling("div")
                    see_more = see_more_div.find("a")
                    driver.get("https://mbasic.facebook.com" + see_more['href'])
                except:
                    print("Error when loading more posts")
                    break
            
            except Exception as e:
                print("Error in loop")
                print(e)
                break
            
    except Exception as e:
        print("Fucntion get_timeline_page error")
        print(e)
    finally:
        print("Stop at post: ", count)

def get_list_followed_page(driver):
    driver.get("https://www.facebook.com/pages/?category=liked")
    driver.maximize_window()
    time.sleep(2)
    count = 0
    last_height = driver.execute_script("return document.body.scrollHeight")
    print("Last height: ", last_height)
    while True:
        print("Scrolling...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        print("New height: ", new_height)
        if new_height == last_height:
            print("End of page")
            break
        last_height = new_height
    soup = BeautifulSoup(driver.page_source, "html.parser")
    print("Parsed!")
    #find div wwith role = main
    main_div = soup.find("div", {"role": "main"})
    print("Found main div")
    needed_divs = main_div.findChildren("div", recursive=False)
    while True:

        print("Finding divs...")
        needed_divs = needed_divs[0].findChildren("div", recursive=False)
        if len(needed_divs) > 1:
            print("Found!")
            break
        print(len(needed_divs))

    
    pages = needed_divs[1].find_all("a")
    for page in pages:
        #bỏ https://www.facebook.com/ trong href
        pagename = page['href'][21:]
        if "?" in pagename:
            continue
        print(pagename)

        with open("followed_pages.txt", "a", encoding="utf-8") as f:
            f.write(pagename + "\n")
            count += 1
    

# from load_img import export_link
# export_link("posts.txt", driver)
# # print("Done")
# pageName  ="BoxGirlVn"
# get_timeline_page(driver, pageName)
# export_link("timeLine_"+ pageName + ".txt", "image_" + pageName, "video_" + pageName, driver)
get_list_followed_page(driver)

input("Press Enter to Exit....")
driver.quit()