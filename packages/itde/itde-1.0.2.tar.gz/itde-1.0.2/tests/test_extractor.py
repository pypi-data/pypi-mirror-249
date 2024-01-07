import os
import unittest
import json

from innertube import InnerTube

from datetime import datetime

from typing import Dict
from typing import List

from itde import extract
from itde import Shelf
from itde import Container


class TestExtractor(unittest.TestCase):

    def setUp(self) -> None:
        self.client = InnerTube('WEB_REMIX')

    def test_extract_search_data(self) -> None:
        data = self.client.search('Squarepusher')
        # _save_data('search', data)
        extracted_data = extract(data)
        _print_shelves_info(extracted_data)

    def test_extract_browse_artist_data(self) -> None:
        data = self.client.browse('UCpwax2-MvnILOcR68QWOZ1g')
        # _save_data('browse_artist', data)
        extracted_data = extract(data)
        _print_shelves_info(extracted_data)

    def test_extract_browse_album_data(self) -> None:
        data = self.client.browse('MPADUCpwax2-MvnILOcR68QWOZ1g')
        # _save_data('browse_artist_albums', data)
        extracted_data = extract(data)
        _print_container_info(extracted_data)

    def test_extract_next_content_data(self) -> None:
        data = self.client.next(
            playlist_id='RDCLAK5uy_lOLCULJgoSlAgxiG4C3yl07S7R4O3DuN4'
        )
        # _save_data('next_strange_episodes', data)
        extracted_data = extract(data)
        _print_container_info(extracted_data)


def _save_data(file_type: str, data: Dict) -> None:
    now = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    filename = f"{file_type}_{now}.json"
    with open(os.path.join('innertube_response', filename), mode='w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


def _print_container_info(container: Container) -> None:
    if container:
        print()
        print(container)
        for item in container:
            print(item)
    else:
        print('Empty Container')


def _print_shelves_info(shelves: List[Shelf]) -> None:
    if shelves:
        for shelf in shelves:
            print()
            print(shelf)
            for item in shelf:
                print(item)
    else:
        print('Empty Shelves')
