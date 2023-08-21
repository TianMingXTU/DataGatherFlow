import time
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common import WebDriverException


def crawl_data(selected_mode, search_text, depth):
    try:
        # 启动 Chrome 浏览器
        driver = webdriver.Edge()

        # 设置头信息
        header = {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203'
        }
        driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": header})

        # 打开页面
        url = f"https://blog.csdn.net/nav/{search_text}"
        driver.get(url)

        # 模拟滚动加载数据
        scroll_pause_time = 5  # 等待加载的时间
        screen_height = driver.execute_script("return window.screen.height;")   # 获取屏幕高度

        i = 1
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 滚动到页面底部
            time.sleep(scroll_pause_time)
            new_height = driver.execute_script("return document.body.scrollHeight;")
            if new_height == screen_height:
                break
            screen_height = new_height
            i += 1
            if i > int(depth):  # 控制滚动次数，根据需要适当调整
                break

        # 获取页面源码
        page_source = driver.page_source

        # 关闭浏览器
        driver.quit()

        # 解析页面
        soup = BeautifulSoup(page_source, 'html.parser')

        titles = [title.text if title.text else "N/A" for title in soup.find_all('span', class_='blog-text')]
        contents = [content.text if content.text else "N/A" for content in soup.find_all('p', class_='desc')]
        links = [link['href'] if link else "N/A" for link in soup.find_all('a', class_='blog')]
        authors = [author.a.text if author.a.text else "N/A" for author in soup.find_all('div', class_='operation-c')]

        # 确保所有数组的长度相同
        min_length = min(len(titles), len(contents), len(links), len(authors))
        titles = titles[:min_length]
        contents = contents[:min_length]
        links = links[:min_length]
        authors = authors[:min_length]

        # 创建一个 Pandas DataFrame
        data = {
            '标题': titles,
            '内容': contents,
            '链接': links,
            '作者': authors
        }
        df = pd.DataFrame(data)
        return df
    except WebDriverException as e:
        print("WebDriver 操作出现异常:", e)

