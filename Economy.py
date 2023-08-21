import time
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup


def crawl_data(selected_mode, search_text, depth):
    # 创建一个空的 Pandas DataFrame 用于存储所有数据
    df_total = pd.DataFrame(columns=['标题', '内容', '链接', '作者'])

    # 启动 Chrome 浏览器
    driver = webdriver.Edge()

    for i in range(1, int(depth) + 1):
        # 设置头信息
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203'
        }
        driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": header})

        # 打开页面
        url = f"http://www.ccwin.cn/focus/{search_text}/index.php?page={i}"
        driver.get(url)

        # 模拟滚动加载数据
        scroll_pause_time = 5  # 等待加载的时间
        time.sleep(scroll_pause_time)

        # 获取页面源码
        page_source = driver.page_source

        # 解析页面
        soup = BeautifulSoup(page_source, 'html.parser')

        titles = [title.text if title.text else "N/A" for title in soup.find_all('a', class_='nex_arttitles xi2')]
        contents = [content.text if content.text else "N/A" for content in soup.find_all('div', class_='nex_articersummary')]
        links = [link['href'] if link else "N/A" for link in soup.find_all('a', class_='nex_arttitles xi2')]
        authors = [author.span.text if author.span.text else "N/A" for author in soup.find_all('div', class_='nex_atctl')]

        # 确保所有数组的长度相同
        min_length = min(len(titles), len(contents), len(links), len(authors))
        titles = titles[:min_length]
        contents = contents[:min_length]
        links = links[:min_length]
        authors = authors[:min_length]

        # 创建一个临时的 Pandas DataFrame
        data = {
            '标题': titles,
            '内容': contents,
            '链接': links,
            '作者': authors
        }
        df_temp = pd.DataFrame(data)

        # 将当前迭代的数据合并到总的 DataFrame 中
        df_total = pd.concat([df_total, df_temp], ignore_index=True)

    # 关闭浏览器
    driver.quit()

    return df_total
