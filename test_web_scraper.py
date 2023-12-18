import unittest
from main import WebScraper


class TestWebScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = WebScraper()

    def test_get_csrf_token(self):
        self.assertIsNotNone(self.scraper.get_csrf_token())

    def test_scrape(self):
        result = self.scraper.scrape()
        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()
