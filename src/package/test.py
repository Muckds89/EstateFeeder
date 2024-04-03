import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio
from bot_handlers import HandleLocationSearch  # Adjust import according to your project structure

class TestHandleLocationSearch(unittest.TestCase):

    def setUp(self):
        # Set up an event loop for asynchronous tests
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        # Close the event loop after the test
        self.loop.close()

    @patch('bot_handlers.requests.get', new_callable=AsyncMock)
    @patch('bot_handlers.BeautifulSoup')
    @patch('builtins.open', new_callable=AsyncMock)
    def test_scrape_immobiliare_success(self, mock_open, mock_bs4, mock_requests):
        # Mock the response from requests.get
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = 'mocked HTML content'
        mock_requests.return_value = asyncio.Future()
        mock_requests.return_value.set_result(mock_response)

        # Mock the BeautifulSoup parsing and other setup as before...

        # Wrap the coroutine in a task and run it using the event loop
        # result = self.loop.run_until_complete(
        #     HandleLocationSearch.scrape_immobiliare(
        #          'Padova', '../JSON'
        #     )
        # )

        result = await HandleLocationSearch.scrape_immobiliare('Padova', '../JSON')


if __name__ == '__main__':
    unittest.main()
