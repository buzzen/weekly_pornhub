#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
import time
import sys
import json

class Downloader:
    '''Download video for given URL.'''

    def __init__(self, urls, username="oderteme", password="JamesHarden13", 
            downloaded_filename="downloaded.json"):
        self.driver = webdriver.Chrome()
        self.urls = urls
        self.username = username
        self.password = password
        self.downloaded_filename = downloaded_filename

    def setup(self):
        "login first"

        self.driver.get("http://www.pornhub.com")

        # login if not logged in
        body_tag = self.driver.find_element_by_tag_name("body")
        if body_tag.get_attribute("class") == "logged-out":
            if not self.login():
                print("failed to login")
                raise Exception("failed to login")
            else:
                print("congrats! You've logged in.")
            # pornhub sometimes redirect to random page after logging in 
            # so I manually visit the video page after logging in
            
        elif body_tag.get_attribute("class") == "logged-in":
            print("already logged in")
        else:
            print("wrong logged in state")
            raise Exception("WTF?")

    def run(self):
        self.setup() # login first

        for url in self.urls:
            # skip videos that have been downloaded
            if self.is_downloaded(url, self.downloaded_filename):
                print("This video has been downloaded before!")
                continue

            paid_video = False # if it's true then skip to next video

            # request the page
            print("Accessing", url)
            self.driver.get(url)

            # wait for page (if needed) to locate download button
            for i in range(60): # wait at most 60 seconds
                if self.is_page_ready():
                    print("page is ready")
                    time.sleep(1) # clicking immediately after complete doesn't work
                    download_button = self.driver.find_element_by_xpath(
                        "//*[@id='js-shareData']/div/div[3]/div")
                    download_button.click()
                    if "paidDownload" in download_button.get_attribute("class"):
                        print("You need to pay to download!")
                        paid_video = True
                        break
                    break
                time.sleep(1) # wait for page loading
            else:
                print("timeout")
                continue

            if paid_video: # skip to next video if it's paid video
                continue

            # find the download link
            try:
                download_links = self.driver.find_elements_by_class_name(
                    "downloadBtn.greyButton")
            except NoSuchElementException:
                print("this video can't be downloaded")
                continue

            # begining download
            succeed = False # for mark_as_downloaded
            # loop download links until finding downloadable
            for download_link in download_links: 
                try:
                    download_link.click()
                    succeed = True
                    break
                except ElementNotInteractableException:
                    continue

            # remember downloaded videos
            if succeed:
                self.mark_as_downloaded(url, self.downloaded_filename)

    def is_page_ready(self):
        ready_state = self.driver.execute_script("return document.readyState")
        if ready_state == "loading":
            print("loading page")
        elif ready_state == "complete":
            print("page loaded")
        elif ready_state == "interactive":
            print("page is interactive")

        return ready_state == "complete"

    def login(self):
        # login from download button
        for i in range(60): # wait for page to load for at most 15 seconds
            if self.is_page_ready():
                login_link = self.driver.find_element_by_id("headerLoginLink")
                login_link.click()
                break
            time.sleep(1)
        else:
            raise Exception("timeout")


        # fill username and password, then submit

        try: # pop-up login window
            id_box = self.driver.find_element_by_id("usernameModal")
            id_box.send_keys(self.username)
            pass_box = self.driver.find_element_by_id("passwordModal")
            pass_box.send_keys(self.password)
            pass_box.submit()
        except ElementNotInteractableException: # login page
            for i in range(60):
                time.sleep(1)
                if self.is_page_ready():
                    id_box = self.driver.find_element_by_id("username")
                    id_box.send_keys(self.username)
                    pass_box = self.driver.find_element_by_id("password")
                    pass_box.send_keys(self.password)
                    submit = self.driver.find_element_by_id("submit")
                    submit.click()
                    break

        # manually wait for 5 seconds so browser can respond to my log in button click
        time.sleep(5) 
        print("logging in...")

        return True

    def mark_as_downloaded(self, url, filename):
        with open(filename, "r") as f:
            try:
                downloaded_urls = json.load(f)
            except json.decoder.JSONDecodeError:
                downloaded_urls = []

            downloaded_urls.append(url)

        with open(filename, "w") as f:
                json.dump(downloaded_urls, f)

    def is_downloaded(self, url, filename):
        with open(filename) as f:
            try:
                downloaded_urls = json.load(f)
            except json.decoder.JSONDecodeError:
                return False

            return url in downloaded_urls

if __name__ == "__main__":
    urls = [
        "https://www.pornhub.com/view_video.php?viewkey=ph5ebd5cf2658e8",
        "https://www.pornhub.com/view_video.php?viewkey=ph5e5866a54b458",
        "https://www.pornhub.com/view_video.php?viewkey=ph5e9618d3baddf",
        "https://www.pornhub.com/view_video.php?viewkey=ph5ea206352bd49"
      ]
    download = Downloader(urls)
    download.run()