# -*- coding = utf-8 -*-
# @Time:2021/12/24下午8:34
# @Author:weirdo
# @File:spider.py
# @Software:PyCharm
import json

from bs4 import BeautifulSoup
import re
import requests
import urllib.error
import xlwt
import sqlite3
from  selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from browsermobproxy import Server
import time


def creatProxy():
    server = Server(r'/home/weirdo/software/browsermob-proxy-2.1.4/bin/browsermob-proxy')
    server.start()
    proxy = server.create_proxy()
    proxy.new_har("netEase", options={'captureHeaders': True, 'captureContent': False})
    return server,proxy

def playSong(url):
    server,proxy=creatProxy()

    options=Options()
    options.add_argument("--headless")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--proxy-server={0}".format(proxy.proxy))
    driver=webdriver.Chrome(options=options)
    driver.get(url)
    driver.switch_to.frame('g_iframe')

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.u-btn2.u-btn2-2.u-btni-addply.f-fl"))
        )

        driver.find_elements_by_css_selector("a.u-btn2.u-btn2-2.u-btni-addply.f-fl")[0].click()
        time.sleep(3)
        downloadSong(proxy.har)
    finally:
        server.stop()
        driver.quit()

def downloadSong(har):
    result = har
    download_url = ""

    for entry in result['log']['entries']:
        _url = entry['request']['url']
        if '.m4a' in _url:
            download_url = _url
            break

    song = requests.get(download_url, stream=True, verify=True)
    with open(f'./{song_id}.m4a', 'wb') as f:
        f.write(song.content)
    song.close()

#1430319727
if __name__=="__main__":
    netease_url="https://music.163.com/#/song?id="
    song_id=str(input("My dear son,input the id of your wanted song:"))
    wanted_song_url=netease_url+song_id
    playSong(wanted_song_url)




