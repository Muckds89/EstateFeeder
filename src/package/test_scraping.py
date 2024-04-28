import unittest
from scrape import Scraping

class TestScraping(unittest.TestCase):
    def test_scrape_immobiliare_success(self):
        Scraping().scrape_immobiliare('Padova','RESULTS','2024-04-28_18_10_53')


if __name__ == '__main__':
    unittest.main()