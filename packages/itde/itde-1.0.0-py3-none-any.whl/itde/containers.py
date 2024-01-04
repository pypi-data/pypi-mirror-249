import logging

from .items import Item
from .ytypes import ShelfType
from .ytypes import ItemType
from .endpoints import Endpoint


logger = logging.getLogger(__name__)


class Shelf(list):
    def __init__(
            self,
            shelf_type: ShelfType = None,
            shelf_endpoint: Endpoint = None,
    ) -> None:
        super().__init__()
        self.shelf_type = shelf_type
        self.shelf_endpoint = shelf_endpoint


class CardShelf(Item, Shelf):
    def __init__(
            self,
            item_title: str = None,
            item_endpoint: Endpoint = None,
            item_type: ItemType = None,
            thumbnail_url: str = None,
    ) -> None:
        super(CardShelf, self).__init__(
            item_title=item_title,
            item_endpoint=item_endpoint,
            thumbnail_url=thumbnail_url,
            item_type=item_type
        )
        self.shelf_endpoint = None
        self.shelf_type = ShelfType.TOP_RESULT


class Container(list):
    def __init__(
            self,
            title: str,
    ) -> None:
        super().__init__()
        self.title = title
