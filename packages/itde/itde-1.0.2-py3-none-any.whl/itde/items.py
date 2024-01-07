from datetime import date
from datetime import time
from typing import List
from .endpoints import Endpoint
from .ytypes import ItemType


class Item:
    def __init__(
            self,
            item_title: str = None,
            item_endpoint: Endpoint = None,
            item_type: ItemType = None,
            thumbnail_url: str = None,
    ) -> None:
        self.item_type: ItemType = item_type
        self.item_title: str = item_title
        self.item_endpoint: Endpoint = item_endpoint
        self.thumbnail_url: str = thumbnail_url

    def __repr__(self) -> str:
        return (
            'Item{'
            f'title={self.item_title}, '
            f'type={self.item_type}, '
            f'endpoint={self.item_endpoint}, '
            f'thumbnail_url={self.thumbnail_url}'
            '}'
        )


class ArtistItem(Item):
    def __init__(
            self,
            subscribers: int = None,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.subscribers: int = subscribers
        self.item_type: ItemType = ItemType.ARTIST

    def __repr__(self) -> str:
        return super().__repr__()[:-1] + (
            f', subscribers={self.subscribers}'
            '}'
        )


class ItemWithArtist(Item):
    def __init__(
            self,
            artist_items: List[ArtistItem] = None,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        if artist_items:
            self.artist_items: List[ArtistItem] = artist_items
        else:
            self.artist_items: List[ArtistItem] = []

    def __repr__(self) -> str:
        return super().__repr__()[:-1] + (
            f', artist_items={self.artist_items}'
            '}'
        )


class VideoItem(ItemWithArtist):
    def __init__(
            self,
            length: time = None,
            views: int = None,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.item_type: ItemType = ItemType.VIDEO
        self.length: time = length
        self.views: int = views

    def __repr__(self) -> str:
        return super().__repr__()[:-1] + (
            f', length={self.length}, '
            f'views={self.views}'
            '}'
        )


class AlbumItem(ItemWithArtist):
    def __init__(
            self,
            release_year: int = None,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.release_year: int = release_year
        self.item_type: ItemType = ItemType.ALBUM

    def __repr__(self) -> str:
        return super().__repr__()[:-1] + (
            f', release_year={self.release_year}'
            '}'
        )


class EPItem(AlbumItem):
    def __init__(
            self,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.item_type: ItemType = ItemType.EP


class PlaylistItem(ItemWithArtist):
    def __init__(
            self,
            length: int = None,
            views: int = None,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.length: int = length
        self.views: int = views
        self.item_type: ItemType = ItemType.PLAYLIST

    def __repr__(self) -> str:
        return super().__repr__()[:-1] + (
            f', length={self.length}, '
            f'views={self.views}'
            '}'
        )


class SingleItem(ItemWithArtist):
    def __init__(
            self,
            release_year: int = None,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.release_year: int = release_year
        self.item_type: ItemType = ItemType.SINGLE

    def __repr__(self) -> str:
        return super().__repr__()[:-1] + (
            f', release_year={self.release_year}'
            '}'
        )


class SongItem(ItemWithArtist):
    def __init__(
            self,
            length: time = None,
            reproductions: int = None,
            album_item: AlbumItem = None,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.length: time = length
        self.reproductions: int = reproductions
        self.album_item: Item = album_item
        self.item_type: ItemType = ItemType.SONG

    def __repr__(self) -> str:
        return super().__repr__()[:-1] + (
            f', length={self.length}, '
            f'reproductions={self.reproductions}, '
            f'album_item={self.album_item}'
            '}'
        )


class ProfileItem(Item):
    def __init__(
            self,
            handle: str = None,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.handle = handle
        self.item_type: ItemType = ItemType.PROFILE

    def __repr__(self) -> str:
        return super().__repr__()[:-1] + (
            f', handle={self.handle}'
            '}'
        )


class PodcastItem(ItemWithArtist):
    def __init__(
            self,
            length: time = None,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.length: time = length
        self.item_type: ItemType = ItemType.PODCAST

    def __repr__(self):
        return (
            super().__repr__()[:-1] +
            f', length={self.length}'
            '}'
        )


class EpisodeItem(ItemWithArtist):
    def __init__(
            self,
            publication_date: date = None,
            length: time = None,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.length: time = length
        self.publication_date: date = publication_date
        self.item_type: ItemType = ItemType.EPISODE

    def __repr__(self):
        return (
            super().__repr__()[:-1] +
            f', publication_date={self.publication_date}'
            f', length={self.length}'
            '}'
        )
