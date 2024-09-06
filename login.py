from selenium.webdriver.common.by import By
import time

def login(inputdriver, url = "https://mbasic.facebook.com"):
     # Chuỗi cookie dài
    with open('cookie.txt', 'r') as f:
        cookie_string = f.read()

    # Chuyển đổi chuỗi cookie thành danh sách các đối tượng cookie
    cookies = []
    for item in cookie_string.split(';'):
        if item.strip():  # Loại bỏ các mục trống
            name, value = item.strip().split('=', 1)
            cookies.append({'name': name, 'value': value})

    # Kết nối Selenium và thêm cookie
    from selenium import webdriver
    # Khởi tạo trình điều khiển cho trình duyệt (ví dụ: Chrome)
    driver = inputdriver
    # Mở trang đăng nhập của Facebook
    driver.get(url)
    # Thêm từng cookie vào trình duyệt
    for cookie in cookies:
        driver.add_cookie(cookie)
    # Tải lại trang
    driver.get(url)
    return driver

def login_w_keys(inputdriver, username, password, url_login = "https://www.instagram.com/"):
    driver = inputdriver
    driver.get(url_login)
    time.sleep(5)
    #find the username input
    xpath = "//input[@name='username']"
    username_input = driver.find_element(By.XPATH, xpath)
    #send the username
    username_input.send_keys(username)
    #find the password input
    xpath = "//input[@name='password']"
    password_input = driver.find_element(By.XPATH, xpath)
    #send the password
    password_input.send_keys(password)
    #find the login button
    xpath = "//button[@type='submit']"
    login_button = driver.find_element(By.XPATH, xpath)
    #click the login button
    login_button.click()
    time.sleep(5)
    return driver