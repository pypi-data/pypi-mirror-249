from .items import Item
from .ytypes import ShelfType
from .ytypes import ItemType
from .endpoints import Endpoint


class Shelf(list):
    def __init__(
            self,
            shelf_type: ShelfType = None,
            shelf_endpoint: Endpoint = None,
    ) -> None:
        super().__init__()
        self.shelf_type: ShelfType = shelf_type
        self.shelf_endpoint: Endpoint = shelf_endpoint

    def __repr__(self) -> str:
        return (
            'Shelf{'
            f'shelf_type={self.shelf_type}, '
            f'shelf_endpoint={self.shelf_endpoint}, '
            f'items={super().__repr__()}'
            '}'
        )


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
        self.shelf_endpoint: Endpoint | None = None
        self.shelf_type: ShelfType = ShelfType.TOP_RESULT

    def __repr__(self) -> str:
        return (
            'CardShelf{'
            f'title={self.item_title}, '
            f'type={self.item_type}, '
            f'endpoint={self.item_endpoint}, '
            f'thumbnail_url={self.thumbnail_url}, '
            f'{super(Item, self).__repr__()}'
            '}'
        )


class Container(list):
    def __init__(
            self,
            title: str = None,
    ) -> None:
        super().__init__()
        self.title: str = title

    def __repr__(self) -> str:
        return (
            'Container{'
            f'title={self.title}, '
            f'items={super().__repr__()}'
            '}'
        )
