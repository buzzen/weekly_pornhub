import unittest
from main import fetch_urls
from downloader import Downloader
import os

@unittest.skip("need to improve as real requests cost too much")
class TestFetchingURLs(unittest.TestCase):

    def test_fetching_urls(self):
        mv_url = "https://www.pornhub.com/video?o=mv&cc=us"
        page_urls = fetch_urls(mv_url)
        self.assertEqual(len(page_urls), 32)

    @unittest.expectedFailure
    def test_demo(self):
        self.assertEqual(1, 2)

class TestDownloaded(unittest.TestCase):
    '''Using mock object to replace real file reading and network accessing'''

    def setUp(self):
        self.urls = [
            "https://www.pornhub.com/view_video.php?viewkey=ph5ebd5cf2658e8",
            "https://www.pornhub.com/view_video.php?viewkey=ph5e5866a54b458",
            "https://www.pornhub.com/view_video.php?viewkey=ph5e9618d3baddf",
            "https://www.pornhub.com/view_video.php?viewkey=ph5ea206352bd49"
          ]
        self.demo_downloader = Downloader(self.urls)
        self.filename = "test_downloaded.json"
        with open(self.filename, "w"): # create a json file for testing
            pass

    def test_whether_new_urls_are_downloaded(self):
        for url in self.urls:
            with self.subTest(url=url):
                self.assertEqual(self.demo_downloader.is_downloaded(url, self.filename),
                    False)

    def test_whether_old_urls_are_downloaded(self):
        for url in self.urls:
            self.demo_downloader.mark_as_downloaded(url, self.filename)

        for url in self.urls:
            with self.subTest(url=url):
                self.assertEqual(self.demo_downloader.is_downloaded(url, self.filename),
                    True)

    def tearDown(self):
        self.demo_downloader.driver.quit()
        os.remove(self.filename)

if __name__ == "__main__":
    unittest.main()
