# 匯入套件
# 操作 browser 的 API
from re import L
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 處理逾時例外的工具
from selenium.common.exceptions import TimeoutException

# 面對動態網頁，等待某個元素出現的工具，通常與 expected_conditions 搭配
from selenium.webdriver.support.ui import WebDriverWait

# 搭配 WebDriverWait 使用，對元素狀態的一種期待條件，若條件發生，則等待結束，往下一行執行
from selenium.webdriver.support import expected_conditions as EC

# 期待元素出現要透過什麼方式指定，通常與 EC、WebDriverWait 一起使用
from selenium.webdriver.common.by import By

# 強制等待
from time import sleep

# 整理 json 的工具
import json

# 執行 command 的時候使用
import os

# 子處理程序，用來取代 os.system 的功能
import subprocess

# 建立儲存用的資料夾
folderPath = 'M:\BDSE28 上課影片\JDBC'
if not os.path.exists(folderPath):
    os.makedirs(folderPath)

def start():
    # 啟動瀏覽器工具的選項
    my_options = webdriver.ChromeOptions()
    my_options.add_argument("--start_maximized")
    # my_options.add_argument("--incognito")
    my_options.add_argument("--disable_popup_blocking")
    my_options.add_argument("--disable-notifications")
    my_options.add_argument("--lang=zh-TW")
    my_options.add_experimental_option("detach", True)

    # 使用 Chrome 的 WebDriver
    my_driver = webdriver.Chrome(
        options = my_options,
        service = Service(ChromeDriverManager().install())
    )

    # 放置爬取的資料
    listData = []

    my_driver.get('https://www.youtube.com/playlist?list=PLT_yviZi9JqTZWmVu91AL0VUtXemOPN_z')

    try:
        WebDriverWait(my_driver, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'a#video-title')
            )
        )

        allvideos = my_driver.find_elements(By.CSS_SELECTOR, 'a#video-title')

        sleep(2)

        for video in allvideos:
            print('=' * 100)
            
            aTitle = video.get_attribute('innerText')
            print(aTitle)
            aLink = video.get_attribute('href')
            print(aLink)

            listData.append({
                'title': aTitle,
                'link': aLink
            })

    except TimeoutException:
        print('等候逾時')

    with open(f'{folderPath}/youtube.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(listData, ensure_ascii=False, indent=4))

    sleep(3)

    my_driver.quit()


def download():
    with open(f'{folderPath}/youtube.json', 'r', encoding='utf-8') as file:
        strjson = file.read()

    listResult = json.loads(strjson)

    for index, obj in enumerate(listResult):

        print('=' * 100)
        print(f'正在下載: {obj["link"]}')

        # 定義指令
        cmd = [
            './yt-dlp.exe',
            obj['link'],
            '-f', 'b[ext=mp4]',
            '-o', f'{folderPath}/%(title)s.%(ext)s'
        ]
        
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        output = result.stdout
        print('下載完成，訊息如下:')
        print(output)

# 下載不會一次一條檔案，需再改
if __name__ == "__main__":
    # start()
    download()