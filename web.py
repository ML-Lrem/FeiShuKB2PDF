from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_bottom_urls(driver, url, layer, bottom_links_list=None):
    if bottom_links_list is None:
        bottom_links_list = []
    if layer == 2:      # 第一次登录
        # 打开要访问的网页
        driver.get(url)
        # 隐式等待页面加载完成:10s
        driver.implicitly_wait(10)
        # 登录到网址
        wait = WebDriverWait(driver, 10)
        wait.until(
            EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "note-login")]'))
        ).click()
        driver.implicitly_wait(20)
    else:
        driver.get(url)
        driver.implicitly_wait(10)
    layer = layer - 1
    wait = WebDriverWait(driver, 10)
    link_container = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "block-catalog--content-scroll"))
    )
    link_elements = link_container.find_elements(By.TAG_NAME, "a")
    links = []
    for link_element in link_elements:
        link = link_element.get_attribute("href")
        links.append(link)
    for link in links:
        if layer == 0:
            bottom_links_list.append(link)
        else:
            bottom_links_list = get_bottom_urls(driver, link, layer, bottom_links_list)

    return bottom_links_list


# 获取网页动态元素/审查元素
def get_links(webdriver_path, url, layer, login_message=None):
    if login_message is None:
        login_message = ['', '']

    # ————————————获取批量文档链接 ————————————#
    # 使用edge_driver
    driver = webdriver.Edge(webdriver_path)

    document_list = get_bottom_urls(driver, url, layer)
    # document_list = []

    # 关闭浏览器
    driver.quit()
    return document_list
