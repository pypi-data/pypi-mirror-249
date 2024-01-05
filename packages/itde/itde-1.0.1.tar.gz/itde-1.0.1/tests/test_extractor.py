import unittest

from itde import extract_search_data
from itde import items
from innertube import InnerTube


class TestExtractor(unittest.TestCase):

    def setUp(self):
        pass

    def test_extract_search_data(self):
        client = InnerTube('WEB_REMIX')
        data = client.search('Squarepusher')
        print(data)
        extracted_data = extract_search_data(data)
        for shelf in extracted_data:
            for item in shelf:
                print(item.item_title)
                print(item.item_endpoint)
                print(item.item_type)
                print(item.thumbnail_url)

                if isinstance(item, items.ItemWithArtist):
                    for artist in item.artist_items:
                        print('    ', artist.item_title)
                        print('    ', artist.item_endpoint)
                        print('    ', artist.item_type)
                        print('    ', artist.thumbnail_url)
