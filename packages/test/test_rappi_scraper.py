import unittest
from packages.core.rappi_scraper import RappiParser


class TestRappiScrapper(unittest.TestCase):
    def test_categories(self):
        rappi_parser = RappiParser()
        categories = rappi_parser.categories
        self.assertEqual(len(categories) > 1, True)

    def test_get_restaurants_urls(self):
        rappi_parser = RappiParser()
        restaurants_urls = rappi_parser.get_restaurants_urls(category="Hamburguesas")
        self.assertEqual(len(restaurants_urls) > 1, True)

    def test_get_restaurants_results(self):
        limit = 3
        rappi_parser = RappiParser()
        restaurants_urls = rappi_parser.get_restaurants_urls(category="Hamburguesas")
        restaurants_results = rappi_parser.get_restaurants_results(restaurants_urls=restaurants_urls,
                                                                   limit=limit)
        self.assertEqual(len(restaurants_results)-1<=limit, True)

if __name__ == '__main__':
    unittest.main()
