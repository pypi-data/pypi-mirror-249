from typing import Dict
from typing import List
from typing import Callable

from .endpoints import BrowseEndpoint
from .endpoints import SearchEndpoint
from .endpoints import UrlEndpoint
from .endpoints import WatchEndpoint

from .containers import CardShelf
from .containers import Endpoint
from .containers import Shelf
from .containers import Container

from .items import AlbumItem
from .items import VideoItem
from .items import ArtistItem
from .items import PlaylistItem
from .items import SongItem

from .exceptions import InvalidKey
from .exceptions import KeyNotFound
from .exceptions import UnregisteredItemType
from .exceptions import UnregisteredShelfType
from .exceptions import UnknownEndpoint

from .ytypes import EndpointType
from .ytypes import SearchResultStrucType
from .ytypes import BrowseResultStrucType
from .ytypes import NextResultStrucType
from .ytypes import SectionType
from .ytypes import PanelItemStructType
from .ytypes import ShelfStructType
from .ytypes import ShelfItemStructType
from .ytypes import ShelfType
from .ytypes import ItemType
from .ytypes import TextDivisorType


def handle(function: Callable) -> Callable:
    def inner_function(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except (
                KeyError,
                IndexError,
                TypeError,
                ValueError
        ) as exception:
            raise InvalidKey(exception)
    return inner_function


@handle
def extract_search_data(data: Dict) -> List[Shelf]:
    # -> Tabbed Search Results Renderer
    data = data["contents"]
    if SearchResultStrucType.TABBED_SEARCH_RESULTS.value in data:
        contents = data["tabbedSearchResultsRenderer"][
            "tabs"][0]["tabRenderer"]["content"][
            "sectionListRenderer"]["contents"]
    else:
        raise KeyNotFound(data.keys())

    shelves_list: List[Shelf] = []
    for entry in contents:
        # -> Music Shelf
        if ShelfStructType.MUSIC_SHELF.value in entry:
            key = ShelfStructType.MUSIC_SHELF.value
            shelf_type = ShelfType(
                entry[key]["title"][
                    "runs"][0]["text"]
            )
            entry_contents = entry[key]["contents"]
            endpoint = _extract_endpoint(
                endpoint=entry[key]["bottomEndpoint"]
            )
            shelf = Shelf(
                shelf_type=shelf_type,
                shelf_endpoint=endpoint
            )

        # -> Music Card Shelf
        elif ShelfStructType.MUSIC_CARD_SHELF.value in entry:
            key = ShelfStructType.MUSIC_CARD_SHELF.value
            shelf_type = ShelfType(
                entry[key]["header"][
                    "musicCardShelfHeaderBasicRenderer"][
                    "title"]["runs"][0]["text"])
            entry_contents = entry[key].get("contents", None)
            # TODO find item_title, endpoint,
            #  thumbnail_url and item_type
            shelf = CardShelf(
                item_title=None,
                item_endpoint=None,
                item_type=None,
                thumbnail_url=None,
            )

        # -> Item Section
        elif SectionType.ITEM_SECTION.value in entry:
            continue

        # -> Invalid cases
        else:
            raise KeyNotFound(entry.keys())

        item_type = _extract_item_type(shelf_type)
        if not item_type:  # Top Result Case
            continue
        for entry_item in entry_contents:
            #  -> musicResponsiveListItemRenderer
            if ShelfItemStructType.MUSIC_RESPONSIVE_LIST_ITEM.value in entry_item:
                key = ShelfItemStructType.MUSIC_RESPONSIVE_LIST_ITEM.value
                thumbnail_url = entry_item[key]["thumbnail"][
                    "musicThumbnailRenderer"]["thumbnail"][
                    "thumbnails"][-1]["url"]
                item_title = entry_item[key]["flexColumns"][0][
                    "musicResponsiveListItemFlexColumnRenderer"]["text"][
                    "runs"][0]["text"]
                match item_type:
                    # -> Artist
                    case ItemType.ARTIST:
                        subscribers = _extract_subscribers(
                            subscribers=entry_item[key]["flexColumns"][1][
                                "musicResponsiveListItemFlexColumnRenderer"][
                                "text"]["runs"][-1]
                        )
                        endpoint = _extract_endpoint(
                            endpoint=entry_item[key]["navigationEndpoint"]
                        )
                        item = ArtistItem(
                            item_title=item_title,
                            item_endpoint=endpoint,
                            thumbnail_url=thumbnail_url,
                            subscribers=subscribers
                        )

                    # -> Album
                    case ItemType.ALBUM:
                        release_year = entry_item[key]["flexColumns"][1][
                            "musicResponsiveListItemFlexColumnRenderer"][
                            "text"]["runs"][-1]["text"]
                        endpoint = _extract_endpoint(
                            endpoint=entry_item[key]["navigationEndpoint"]
                        )
                        item = AlbumItem(
                            item_title=item_title,
                            item_endpoint=endpoint,
                            thumbnail_url=thumbnail_url,
                            release_year=int(release_year)
                        )

                    # -> Video
                    case ItemType.VIDEO:
                        length = entry_item[key]["flexColumns"][1][
                            "musicResponsiveListItemFlexColumnRenderer"][
                            "text"]["runs"][-1]["text"]
                        views = entry_item[key]["flexColumns"][1][
                            "musicResponsiveListItemFlexColumnRenderer"][
                            "text"]["runs"][-3]["text"]
                        endpoint = _extract_endpoint(
                            endpoint=entry_item[key]["flexColumns"][0][
                                "musicResponsiveListItemFlexColumnRenderer"][
                                "text"]["runs"][-1]["navigationEndpoint"]
                        )
                        item = VideoItem(
                            item_title=item_title,
                            item_endpoint=endpoint,
                            thumbnail_url=thumbnail_url,
                            length=length,
                            views=views
                        )

                    # -> Playlist
                    case ItemType.PLAYLIST:
                        if shelf_type == ShelfType.FEATURED_PLAYLIST:
                            length = entry_item[key]["flexColumns"][1][
                                "musicResponsiveListItemFlexColumnRenderer"][
                                "text"]["runs"][-1]["text"]
                            views = None
                        elif shelf_type == ShelfType.COMMUNITY_PLAYLIST:
                            length = None
                            views = entry_item[key]["flexColumns"][1][
                                "musicResponsiveListItemFlexColumnRenderer"][
                                "text"]["runs"][-1]["text"]
                        else:
                            # TODO
                            length = None
                            views = None
                        endpoint = _extract_endpoint(
                            endpoint=entry_item[key]["navigationEndpoint"]
                        )
                        item = PlaylistItem(
                            item_title=item_title,
                            item_endpoint=endpoint,
                            thumbnail_url=thumbnail_url,
                            length=length,
                            views=views
                        )

                    # -> Song
                    case ItemType.SONG:
                        length = entry_item[key]["flexColumns"][1][
                            "musicResponsiveListItemFlexColumnRenderer"][
                            "text"]["runs"][-1]["text"]
                        reproduction = entry_item[key]["flexColumns"][2][
                            "musicResponsiveListItemFlexColumnRenderer"][
                            "text"]["runs"][-1]["text"]
                        endpoint = _extract_endpoint(
                            endpoint=entry_item[key]["flexColumns"][0][
                                "musicResponsiveListItemFlexColumnRenderer"][
                                "text"]["runs"][-1]["navigationEndpoint"]
                        )
                        related_data = _extract_item_related_data(
                            data=entry_item[key]["flexColumns"][1][
                                "musicResponsiveListItemFlexColumnRenderer"][
                                "text"]["runs"]
                        )
                        item = SongItem(
                            item_title=item_title,
                            item_endpoint=endpoint,
                            thumbnail_url=thumbnail_url,
                            length=length,
                            reproductions=reproduction,
                            artist_items=related_data[0],
                            album_item=related_data[1]
                        )

                    # TODO -> Episode
                    case ItemType.EPISODE:
                        continue

                    # TODO -> Podcast
                    case ItemType.PODCAST:
                        continue

                    # TODO -> Profile
                    case ItemType.PROFILE:
                        continue

                    case _:
                        raise UnregisteredItemType(item_type)
            else:
                raise KeyNotFound(f'Content: {entry_item.keys()}')

            shelf.append(item)
        shelves_list.append(shelf)
    return shelves_list


@handle
def extract_browse_data(data: Dict) -> List[Shelf]:
    # -> Single Column Browse Results Renderer
    data = data["contents"]
    if BrowseResultStrucType.SINGLE_COLUMN_BROWSE_RESULTS.value in data:
        contents = data["singleColumnBrowseResultsRenderer"][
            "tabs"][0]["tabRenderer"]["content"][
            "sectionListRenderer"]["contents"]
    else:
        raise KeyNotFound(data.keys())

    shelves_list: List[Shelf] = []
    for entry in contents:
        # -> Music Shelf
        if ShelfStructType.MUSIC_SHELF.value in entry:
            key = ShelfStructType.MUSIC_SHELF.value
            shelf_type = ShelfType(
                entry[key]["title"][
                    "runs"][0]["text"]
            )
            entry_contents = entry[key]["contents"]
            endpoint = _extract_endpoint(
                endpoint=entry[key]["bottomEndpoint"]
            )
            shelf = Shelf(
                shelf_type=shelf_type,
                shelf_endpoint=endpoint
            )

        # -> Music Carousel Shelf
        elif ShelfStructType.MUSIC_CAROUSEL_SHELF.value in entry:
            key = ShelfStructType.MUSIC_CAROUSEL_SHELF.value
            shelf_type = ShelfType(
                entry[key]["header"][
                    "musicCarouselShelfBasicHeaderRenderer"][
                    "title"]["runs"][0]["text"]
            )
            entry_contents = entry[key]["contents"]
            try:
                endpoint = _extract_endpoint(
                    endpoint=entry[key]["header"][
                        "musicCarouselShelfBasicHeaderRenderer"][
                        "title"]["runs"][0]["navigationEndpoint"]
                )
            except KeyError:
                endpoint = None
            shelf = Shelf(
                shelf_type=shelf_type,
                shelf_endpoint=endpoint
            )

        # -> Music Description Shelf
        elif ShelfStructType.MUSIC_DESCRIPTION_SHELF.value in entry:
            continue

        else:
            raise KeyNotFound(entry.keys())

        item_type = _extract_item_type(shelf_type)
        for entry_item in entry_contents:
            # -> musicTwoRowItemRenderer
            if ShelfItemStructType.MUSIC_TWO_ROW_ITEM.value in entry_item:
                key = ShelfItemStructType.MUSIC_TWO_ROW_ITEM.value
                thumbnail_url = entry_item[key]["thumbnailRenderer"][
                    "musicThumbnailRenderer"]["thumbnail"][
                    "thumbnails"][-1]["url"]
                item_title = entry_item[key]["title"]["runs"][0]["text"]
                endpoint = _extract_endpoint(
                    endpoint=entry_item[key]["navigationEndpoint"]
                )
                match item_type:
                    # -> Artist
                    case ItemType.ARTIST:
                        subscribers = _extract_subscribers(
                            subscribers=entry_item[key]["subtitle"][
                                "runs"][0]["text"]
                        )
                        item = ArtistItem(
                            item_title=item_title,
                            item_endpoint=endpoint,
                            thumbnail_url=thumbnail_url,
                            subscribers=subscribers
                        )

                    # -> Album
                    case ItemType.ALBUM:
                        release_year = entry_item[key]["subtitle"][
                            "runs"][-1]["text"]
                        item = AlbumItem(
                            item_title=item_title,
                            item_endpoint=endpoint,
                            thumbnail_url=thumbnail_url,
                            release_year=int(release_year)
                        )

                    # -> Video
                    case ItemType.VIDEO:
                        views = entry_item[key]["subtitle"]["runs"][-1]["text"]
                        item = VideoItem(
                            item_title=item_title,
                            item_endpoint=endpoint,
                            thumbnail_url=thumbnail_url,
                            length=None,
                            views=views
                        )

                    # -> Playlist
                    case ItemType.PLAYLIST:
                        item = PlaylistItem(
                            item_title=item_title,
                            item_endpoint=endpoint,
                            thumbnail_url=thumbnail_url,
                            length=None,
                            views=None
                        )

                    # -> Song
                    case ItemType.SONG:
                        item = SongItem(
                            item_title=item_title,
                            item_endpoint=endpoint,
                            thumbnail_url=thumbnail_url,
                            length=None,
                            reproductions=None,
                            album_item=None
                        )

                    # TODO -> Episode
                    case ItemType.EPISODE:
                        continue

                    # TODO -> Podcast
                    case ItemType.PODCAST:
                        continue

                    # TODO -> Profile
                    case ItemType.PROFILE:
                        continue

                    case _:
                        raise UnregisteredItemType()

            #  -> musicResponsiveListItemRenderer
            elif ShelfItemStructType.MUSIC_RESPONSIVE_LIST_ITEM.value in entry_item:
                key = ShelfItemStructType.MUSIC_RESPONSIVE_LIST_ITEM.value
                thumbnail_url = entry_item[key]["thumbnail"][
                    "musicThumbnailRenderer"]["thumbnail"][
                    "thumbnails"][-1]["url"]
                item_title = entry_item[key]["flexColumns"][0][
                    "musicResponsiveListItemFlexColumnRenderer"]["text"][
                    "runs"][0]["text"]
                match item_type:
                    # -> Artist (Verified)
                    case ItemType.ARTIST:
                        subscribers = _extract_subscribers(
                            subscribers=entry_item[key]["flexColumns"][1][
                                "musicResponsiveListItemFlexColumnRenderer"][
                                "text"]["runs"][-1]
                        )
                        endpoint = _extract_endpoint(
                            endpoint=entry_item[key]["navigationEndpoint"]
                        )
                        item = ArtistItem(
                            item_title=item_title,
                            item_endpoint=endpoint,
                            thumbnail_url=thumbnail_url,
                            subscribers=subscribers
                        )

                    # -> Album (Verified)
                    case ItemType.ALBUM:
                        release_year = entry_item[key]["flexColumns"][1][
                            "musicResponsiveListItemFlexColumnRenderer"][
                            "text"]["runs"][-1]["text"]
                        endpoint = _extract_endpoint(
                            endpoint=entry_item[key]["navigationEndpoint"]
                        )
                        item = AlbumItem(
                            item_title=item_title,
                            item_endpoint=endpoint,
                            thumbnail_url=thumbnail_url,
                            release_year=int(release_year)
                        )

                    # -> Video (Verified)
                    case ItemType.VIDEO:
                        length = entry_item[key]["flexColumns"][1][
                            "musicResponsiveListItemFlexColumnRenderer"][
                            "text"]["runs"][-1]["text"]
                        views = entry_item[key]["flexColumns"][1][
                            "musicResponsiveListItemFlexColumnRenderer"][
                            "text"]["runs"][-3]["text"]
                        endpoint = _extract_endpoint(
                                endpoint=entry_item[key]["flexColumns"][0][
                                    "musicResponsiveListItemFlexColumnRenderer"][
                                    "text"]["runs"][-1]["navigationEndpoint"]
                        )
                        item = VideoItem(
                            item_title=item_title,
                            item_endpoint=endpoint,
                            thumbnail_url=thumbnail_url,
                            length=length,
                            views=views
                        )

                    # -> Playlist (Verified)
                    case ItemType.PLAYLIST:
                        if shelf_type == ShelfType.FEATURED_PLAYLIST:
                            length = entry_item[key]["flexColumns"][1][
                                "musicResponsiveListItemFlexColumnRenderer"][
                                "text"]["runs"][-1]["text"]
                            views = None
                        elif shelf_type == ShelfType.COMMUNITY_PLAYLIST:
                            length = None
                            views = entry_item[key]["flexColumns"][1][
                                "musicResponsiveListItemFlexColumnRenderer"][
                                "text"]["runs"][-1]["text"]
                        else:
                            # TODO
                            length = None
                            views = None
                        endpoint = _extract_endpoint(
                            endpoint=entry_item[key]["navigationEndpoint"]
                        )
                        item = PlaylistItem(
                            item_title=item_title,
                            item_endpoint=endpoint,
                            thumbnail_url=thumbnail_url,
                            length=length,
                            views=views
                        )

                    # -> Song (Verified)
                    case ItemType.SONG:
                        length = entry_item[key]["flexColumns"][1][
                            "musicResponsiveListItemFlexColumnRenderer"][
                            "text"]["runs"][-1]["text"]
                        reproduction = entry_item[key]["flexColumns"][2][
                            "musicResponsiveListItemFlexColumnRenderer"][
                            "text"]["runs"][-1]["text"]
                        endpoint = _extract_endpoint(
                            endpoint=entry_item[key]["flexColumns"][0][
                                "musicResponsiveListItemFlexColumnRenderer"][
                                "text"]["runs"][-1]["navigationEndpoint"]
                        )
                        # TODO AlbumItem / ArtistItem[]
                        item = SongItem(
                            item_title=item_title,
                            item_endpoint=endpoint,
                            thumbnail_url=thumbnail_url,
                            length=length,
                            reproductions=reproduction
                        )

                    # TODO -> Episode
                    case ItemType.EPISODE:
                        continue

                    # TODO -> Podcast
                    case ItemType.PODCAST:
                        continue

                    # TODO -> Profile
                    case ItemType.PROFILE:
                        continue

                    case _:
                        raise UnregisteredItemType(item_type)
            else:
                raise KeyNotFound(f'Content: {entry_item.keys()}')

            shelf.append(item)
        shelves_list.append(shelf)
    return shelves_list


@handle
def extract_next_data(data: Dict) -> Container:
    # -> Single Column Music Watch Next Result
    data = data["contents"]
    if NextResultStrucType.SINGLE_COLUMN_MUSIC_WATCH_NEXT_RESULT.value in data:
        content = data["singleColumnMusicWatchNextResultsRenderer"][
            "tabbedRenderer"]["watchNextTabbedResultsRenderer"][
            "tabs"][0]["tabRenderer"]["content"][
            "musicQueueRenderer"]["content"]["playlistPanelRenderer"]
        contents = content["contents"]
        panel = Container(
            title=content["title"]
        )
    else:
        raise InvalidKey(data.keys())

    for entry in contents:
        # -> Playlist Panel Video
        if PanelItemStructType.PLAYLIST_PANEL_VIDEO.value in entry:
            key = PanelItemStructType.PLAYLIST_PANEL_VIDEO.value
            title = entry[key]["title"]["runs"][-1]["text"]
            endpoint = _extract_endpoint(
                entry[key]["navigationEndpoint"]
            )
            length = entry[key]["lengthText"]["runs"][-1]["text"]
            tmp = entry[key]["thumbnail"]["thumbnails"][-1]
            thumbnail_url = tmp["url"]
            width, height = tmp["width"], tmp["height"]
            # Another way to determine the item_type:
            #   if "likes" not in entry[key]["longBylineText"][
            #       "runs"][-1]["text"]
            related_data = _extract_item_related_data(
                data=entry[key]["longBylineText"]["runs"]
            )
            if width / height == 1:  # little hack for item type
                item = SongItem(
                    item_title=title,
                    item_endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    length=length,
                    album_item=related_data[1],
                    artist_items=related_data[0]
                )
            else:
                item = VideoItem(
                    item_title=title,
                    item_endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    length=length,
                    artist_items=related_data[0],
                    views=entry[key]["longBylineText"][
                        "runs"][-3]["text"]
                )

        # -> Automix Preview Video
        elif PanelItemStructType.AUTOMIX_PREVIEW_VIDEO.value in entry:
            continue
        else:
            raise KeyNotFound(entry.keys())

        panel.append(item)
    return panel


def _extract_endpoint(
        endpoint: Dict
) -> Endpoint:
    # -> Browse Endpoint
    if EndpointType.BROWSE_ENDPOINT.value in endpoint:
        endpoint_data = endpoint["browseEndpoint"]
        browse_id = endpoint_data["browseId"]
        browse_endpoint = BrowseEndpoint(
            browse_id=browse_id,
            params=endpoint_data.get("params", None)
        )
        return browse_endpoint

    # -> Watch Endpoint
    elif EndpointType.WATCH_ENDPOINT.value in endpoint:
        endpoint_data = endpoint["watchEndpoint"]
        video_id = endpoint_data["videoId"]
        watch_endpoint = WatchEndpoint(
            video_id=video_id,
            playlist_id=endpoint_data.get("playlist_id", None),
            params=endpoint_data.get("params", None)
        )
        return watch_endpoint

    # -> Search Endpoint
    elif EndpointType.SEARCH_ENDPOINT.value in endpoint:
        endpoint_data = endpoint["searchEndpoint"]
        query = endpoint_data["query"]
        search_endpoint = SearchEndpoint(
            query=query,
            params=endpoint_data.get("params", None)
        )
        return search_endpoint

    # -> Url Endpoint
    elif EndpointType.URL_ENDPOINT in endpoint:
        endpoint_data = endpoint["urlEndpoint"]
        url = endpoint_data["url"]
        url_endpoint = UrlEndpoint(
            url=url,
            params=endpoint_data.get("params", None)
        )
        return url_endpoint

    else:
        raise UnknownEndpoint(f"Endpoint: {endpoint}")


def _extract_item_related_data(
        data: List,
) -> (List[ArtistItem], AlbumItem):
    string = ' '.join([x["text"] for x in data])
    string_list = string.split(TextDivisorType.BULLET_POINT.value)
    try:
        release_year = int(string_list[-1].strip())
    except ValueError:
        release_year = None

    album_name = string_list[1].strip()
    artist_names = [x.strip() for x in string_list[0].split(' & ')]

    try:
        item_endpoint = _extract_endpoint(
            endpoint=data[len(artist_names) * 2]["navigationEndpoint"]
        )
    except KeyError:
        item_endpoint = None

    album_item = AlbumItem(
        item_title=album_name,
        item_endpoint=item_endpoint,
        thumbnail_url=None,
        release_year=release_year
    )
    artist_items = []
    for artist_name in artist_names:
        for entry in data:
            if entry["text"] == artist_name:
                try:
                    item_endpoint = _extract_endpoint(
                        endpoint=entry["navigationEndpoint"]
                    )
                except KeyError:
                    item_endpoint = None
                artist_items.append(
                    ArtistItem(
                        item_title=artist_name,
                        item_endpoint=item_endpoint,
                        thumbnail_url=None,
                        subscribers=None
                    )
                )
                break
    return artist_items, album_item


def _extract_related_data(
        data: Dict,
        item_type: ItemType
) -> (List[ArtistItem], AlbumItem, int, int, int):
    # TODO
    pass


def _extract_subscribers(subscribers: str) -> int:
    # TODO
    pass


def _extract_item_type(shelf_type: ShelfType) -> ItemType | None:
    match shelf_type:
        # -> Song
        case (
            ShelfType.SONG
        ) | (
            ShelfType.SONGS
        ) | (
            ShelfType.SINGLES
        ):
            return ItemType.SONG

        # -> Video
        case (
            ShelfType.VIDEO
        ) | (
            ShelfType.VIDEOS
        ):
            return ItemType.VIDEO

        # -> Playlist
        case (
            ShelfType.FEATURED_PLAYLIST
        ) | (
            ShelfType.COMMUNITY_PLAYLIST
        ) | (
            ShelfType.PLAYLIST
        ) | (
            ShelfType.FEATURED_ON
        ):
            return ItemType.PLAYLIST

        # -> Album
        case (
            ShelfType.ALBUM
        ) | (
            ShelfType.ALBUMS
        ):
            return ItemType.ALBUM

        # -> Artist
        case (
            ShelfType.ARTIST
        ) | (
            ShelfType.ARTISTS
        ) | (
            ShelfType.FANS_MIGHT_ALSO_LIKE
        ):
            return ItemType.ARTIST

        # -> Episode
        case (
            ShelfType.EPISODE
        ) | (
            ShelfType.EPISODES
        ):
            return ItemType.EPISODE

        # -> Profile
        case (
            ShelfType.PROFILES
        ):
            return ItemType.PROFILE

        # -> Podcast
        case (
            ShelfType.PODCASTS
        ):
            return ItemType.PODCAST

        # -> Top Result
        case ShelfType.TOP_RESULT:
            return None

        case _:
            raise UnregisteredShelfType(
                f"ShelfType: {shelf_type}"
            )
