import unittest
from unittest.mock import patch, MagicMock, AsyncMock, call
import asyncio
from bot_handlers import HandleLocationSearch  # Adjust import according to your project structure

class TestHandleLocationSearch(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        self.loop.close()

    @patch('aiohttp.ClientSession.get')
    @patch('builtins.open', new_callable=MagicMock)
    def test_scrape_immobiliare_success(self, mock_open, mock_get):
        mock_response = AsyncMock()
        mock_response.status = 200
        # Ensure response.text() resolves to a string, not a Future
        mock_response.text = AsyncMock()
        mock_response.text.return_value = 'mocked HTML content'

        # Setup mock context manager
        mock_context_manager = AsyncMock()
        mock_context_manager.__aenter__.return_value = mock_response

        mock_get.return_value = mock_context_manager

        # mock_context_manager = AsyncMock()
        # mock_context_manager.__aenter__.return_value = mock_response

        # mock_get.return_value = mock_context_manager

        # Wrap the coroutine in a task and run it using the event loop
        result = self.loop.run_until_complete(
            HandleLocationSearch.scrape_immobiliare(
                 'Padova', '/mnt/c/Users/marco/OneDrive/Documenti/IBM FULL STACK COURSE/PYTHON FOR DATA SCIENCE/REST APIs, Webscraping, and Working with Files/WebScrappingProject/EstateFeeder/src/package/RESULTS'
            )
        )
        # Check the arguments passed to mock_open
        print(mock_open.call_args_list)

        # Check if the first call to open was with the correct arguments
        # Check if the first call to open was with the correct arguments
        first_open_call = mock_open.call_args_list[0]
        expected_call = call(f'/mnt/c/Users/marco/OneDrive/Documenti/IBM FULL STACK COURSE/PYTHON FOR DATA SCIENCE/REST APIs, Webscraping, and Working with Files/WebScrappingProject/EstateFeeder/src/package/RESULTS/Padova_listings.json', 'w', encoding='utf-8')
        self.assertEqual(first_open_call, expected_call)

        # self.assertEqual(result, 'Data scraped and saved to Padova_listings.json')
        # mock_get.assert_called_with('https://www.immobiliare.it/vendita-case/city/')
        # mock_open.assert_called_with('../JSON/city_listings.json', 'w', encoding='utf-8')



if __name__ == '__main__':
    unittest.main()
    # HandleLocationSearch.scrape_immobiliare('Padova', 'JSON')