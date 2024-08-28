def login(inputdriver):
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
    driver.get("https://mbasic.facebook.com")
    # Thêm từng cookie vào trình duyệt
    for cookie in cookies:
        driver.add_cookie(cookie)

    return driver

