#!/usr/bin/python3

import sys
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from downloader import Downloader

# get the URLs of porn which you want to download
print(sys.argv)

mv_url = ("https://www.pornhub.com/video?o=mv&min_duration=20" if len(sys.argv) < 2 
    else sys.argv[1]) # url of page including most viewed porns
print("fecthing urls from", mv_url)

r = requests.get(mv_url)
mvpage_html = r.text
mvpage_tree = BeautifulSoup(mvpage_html, 'html.parser')
porn_list_tag = mvpage_tree.find(id="videoCategory")
porn_list_item_tags = [li for li in porn_list_tag.find_all("li") 
    if "pcVideoListItem" in li["class"]]
relative_urls = [li_tag.a["href"] for li_tag in porn_list_item_tags]
page_urls = ["https://www.pornhub.com" + url for url in relative_urls]

# navigating thru the video page to get the URL of video file
# you have to login
try:
    demo_downloader = Downloader(page_urls)
    demo_downloader.run()
finally:
    demo_downloader.driver.quit()
    
# download