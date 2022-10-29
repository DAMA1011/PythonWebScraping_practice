from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from multiprocessing import Pool
import json, os, time, re

list_book = []

def browser():
    my_options = webdriver.ChromeOptions()
    my_options.add_argument("--start_maximized")
    my_options.add_argument("--incognito")
    my_options.add_argument("--disable_popup_blocking")
    my_options.add_argument("--disable-notifications")
    my_options.add_argument("--lang=zh-TW")
    my_options.add_experimental_option("detach", True)
    my_driver = webdriver.Chrome(
        options = my_options,
        service = Service(ChromeDriverManager().install())
    )     
    return my_driver
 
def test_func(link):
    my_driver = browser()  # Each browser use different driver.
    my_driver.get(link)


    ac = ActionChains(my_driver)
    for i in range(100):
        target = my_driver.find_elements(By.CSS_SELECTOR, 'div.pgdbbylanguage li.pgdbetext a')
        ac.move_to_element(target[i]).click()
        ac.perform()

        my_driver.get(link)

    # aFirstLinks = my_driver.find_elements(By.CSS_SELECTOR, 'div.pgdbbylanguage li.pgdbetext a')
    # for a in aFirstLinks:
    #     regex = r'\b[\u4E00-\u9FFF]+.*\b'
    #     bookname = re.match(regex, a.get_attribute('innerText'))
    #     if bookname != None:
    #         list_book.append(a.get_attribute('innerText'))

def multip():
    links = ["https://www.gutenberg.org/browse/languages/zh", "https://www.gutenberg.org/browse/languages/zh", "https://www.gutenberg.org/browse/languages/zh"]
    my_pool = Pool(processes=3)
    for i in range(0, len(links)):  
        my_pool.apply_async(test_func, args={links[i]})

    my_pool.close()
    my_pool.join()
    
if __name__ == '__main__':
    multip()