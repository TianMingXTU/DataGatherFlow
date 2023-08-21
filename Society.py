import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By


def crawl_data(selected_mode, search_text, depth):
    try:
        # 使用 EdgeOptions 初始化 driver
        options = Options()
        options.use_chromium = True
        driver = webdriver.Edge(options=options)

        # 设置头信息
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203'
        }
        driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": header})

        # 打开页面
        url = f"https://news.cctv.com/{search_text}/"
        driver.get(url)

        # 模拟滚动加载数据和点击加载更多
        for _ in range(int(depth)):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 滚动到页面底部
            time.sleep(4)  # 等待加载时间，根据实际情况适当调整
            load_more_buttons = driver.find_elements(By.ID, 'C94212.PZd4MuV7QTb5.Euuu2IJOvZIL.i0')
            if load_more_buttons:
                load_more_buttons[0].click()
            else:
                break

        # 获取页面源码
        page_source = driver.page_source

        # 解析页面
        soup = BeautifulSoup(page_source, 'html.parser')

        titles = [title.a.text if title.a else "N/A" for title in soup.find_all('h3', class_='title')]
        contents = [content.a.text if content.a else "N/A" for content in soup.find_all('p', class_='brief')]
        links = [link.a['href'] if link.a else "N/A" for link in soup.find_all('h3', class_='title')]
        authors = [author.a.text if author.a else "N/A" for author in soup.find_all('span', class_='date')]

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
            '时间': authors
        }
        df = pd.DataFrame(data)

        # 关闭浏览器
        driver.quit()

        return df
    except WebDriverException as e:
        print("WebDriver 操作出现异常:", e)


