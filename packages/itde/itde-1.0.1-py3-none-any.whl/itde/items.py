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
        self.item_type = item_type
        self.item_title = item_title
        self.item_endpoint = item_endpoint
        self.thumbnail_url = thumbnail_url


class ArtistItem(Item):
    def __init__(
            self,
            subscribers: int = None,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.subscribers = subscribers
        self.item_type = ItemType.ARTIST


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
            self.artist_items = []


class VideoItem(ItemWithArtist):
    def __init__(
            self,
            length: str = None,
            views: int = None,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.item_type = ItemType.VIDEO
        self.length = length
        self.views = views


class AlbumItem(ItemWithArtist):
    def __init__(
            self,
            release_year: int = None,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.release_year = release_year
        self.item_type = ItemType.ALBUM


class PlaylistItem(ItemWithArtist):
    def __init__(
            self,
            length: int = None,
            views: int = None,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.length = length
        self.views = views
        self.item_type = ItemType.PLAYLIST


class SongItem(ItemWithArtist):
    def __init__(
            self,
            length: str = None,
            reproductions: int = None,
            album_item: AlbumItem = None,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.length = length
        self.reproductions = reproductions
        self.album_item = album_item
        self.item_type = ItemType.SONG


class ProfileItem(Item):
    # FIXME
    def __init__(
            self,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.item_type = ItemType.PROFILE


class PodcastItem(Item):
    # FIXME
    def __init__(
            self,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.item_type = ItemType.PODCAST
