import logging

from typing import List
from typing import Callable
from typing import Dict

from .utils import convert_length
from .utils import convert_number
from .utils import get_item_type

from .endpoints import Endpoint
from .endpoints import BrowseEndpoint
from .endpoints import WatchEndpoint
from .endpoints import UrlEndpoint
from .endpoints import SearchEndpoint

from .containers import CardShelf
from .containers import Shelf
from .containers import Container

from .exceptions import UnknownEndpoint
from .exceptions import InvalidKey
from .exceptions import UnregisteredItemType
from .exceptions import KeyNotFound
from .exceptions import UnexpectedState

from .items import Item
from .items import AlbumItem
from .items import VideoItem
from .items import ArtistItem
from .items import PlaylistItem
from .items import SongItem
from .items import SingleItem
from .items import EPItem
from .items import PodcastItem
from .items import ProfileItem
from .items import EpisodeItem

from .ytypes import EndpointType
from .ytypes import ShelfItemStructType
from .ytypes import PanelItemStructType
from .ytypes import SearchResultStrucType
from .ytypes import BrowseResultStrucType
from .ytypes import NextResultStrucType
from .ytypes import SectionType
from .ytypes import ShelfStructType
from .ytypes import ShelfType
from .ytypes import ItemType

logger = logging.getLogger(__name__)


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
def extract(data: Dict) -> List[Shelf] | Container:
    shelves_list: List[Shelf] = []
    contents, title = _extract_contents(data)

    if title:
        container = Container(title)
        for entry_item in contents:
            item = _extract_item(entry_item)
            if item:
                container.append(item)
        return container

    for entry in contents:
        shelf_extraction_result = _extract_shelf(entry)
        if not shelf_extraction_result:
            continue
        shelf, entry_contents = shelf_extraction_result
        item_type = get_item_type(shelf.shelf_type)

        for entry_item in entry_contents:
            item = _extract_item(
                entry_item=entry_item,
                item_type=item_type
            )
            shelf.append(item)
        shelves_list.append(shelf)

    return shelves_list


def _extract_shelf(entry: Dict) -> (Shelf, List[Dict]):
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

    elif ShelfStructType.MUSIC_CARD_SHELF.value in entry:
        key = ShelfStructType.MUSIC_CARD_SHELF.value
        # It should be a 'Top Result' type
        entry_contents = entry[key].get("contents", [])
        thumbnail_url = entry[key]["thumbnail"][
            "musicThumbnailRenderer"]["thumbnail"][
            "thumbnails"][-1]["url"]
        item_title = entry[key]["title"]["runs"][-1]["text"]
        endpoint = _extract_endpoint(
            endpoint=entry[key]["title"]["runs"][-1][
                "navigationEndpoint"]
        )
        item_type = ItemType(
            entry[key]["subtitle"]["runs"][0]["text"]
        )
        shelf = CardShelf(
            item_title=item_title,
            item_endpoint=endpoint,
            item_type=item_type,
            thumbnail_url=thumbnail_url,
        )

    elif ShelfStructType.GRID.value in entry:
        key = ShelfStructType.GRID.value
        entry_contents = entry[key]["contents"]
        shelf = None
    elif (
            SectionType.ITEM_SECTION.value in entry or
            ShelfStructType.MUSIC_DESCRIPTION_SHELF.value in entry
    ):
        return None

    else:
        raise KeyNotFound(entry.keys())

    return shelf, entry_contents


def _extract_contents(data: Dict) -> (List[Dict], str | None):
    contents_data = data["contents"]
    if BrowseResultStrucType.SINGLE_COLUMN_BROWSE_RESULTS.value in contents_data:
        tmp: Dict = contents_data["singleColumnBrowseResultsRenderer"][
            "tabs"][0]["tabRenderer"]["content"][
            "sectionListRenderer"]

        if ShelfStructType.GRID.value in tmp["contents"][0]:
            contents = tmp["contents"][0]["gridRenderer"][
                "items"]
            title = data["header"]["musicHeaderRenderer"][
                "title"]["runs"][0]["text"]
        else:
            contents = tmp["contents"]
            title = None

    elif SearchResultStrucType.TABBED_SEARCH_RESULTS.value in contents_data:
        tmp: Dict = contents_data["tabbedSearchResultsRenderer"][
            "tabs"][0]["tabRenderer"]["content"][
            "sectionListRenderer"]
        contents = tmp["contents"]
        title = None

    elif NextResultStrucType.SINGLE_COLUMN_MUSIC_WATCH_NEXT_RESULT.value in contents_data:
        tmp = contents_data["singleColumnMusicWatchNextResultsRenderer"][
            "tabbedRenderer"]["watchNextTabbedResultsRenderer"][
            "tabs"][0]["tabRenderer"]["content"][
            "musicQueueRenderer"]
        if 'content' not in tmp:  # -> Empty content case
            return None
        contents = tmp["content"]["playlistPanelRenderer"]["contents"]
        title = tmp["content"]["playlistPanelRenderer"]["title"]

    else:
        raise KeyNotFound(contents_data.keys())

    return contents, title


def _extract_item(
        entry_item: Dict,
        item_type: ItemType = None
) -> Item | None:
    if ShelfItemStructType.MUSIC_RESPONSIVE_LIST_ITEM.value in entry_item:
        key = ShelfItemStructType.MUSIC_RESPONSIVE_LIST_ITEM.value
        thumbnail_url = entry_item[key]["thumbnail"][
            "musicThumbnailRenderer"]["thumbnail"][
            "thumbnails"][-1]["url"]
        item_title = entry_item[key]["flexColumns"][0][
            "musicResponsiveListItemFlexColumnRenderer"]["text"][
            "runs"][0]["text"]
        if not item_type:
            try:
                item_type = ItemType(
                    entry_item[key]["flexColumns"][1][
                        "musicResponsiveListItemFlexColumnRenderer"]["text"][
                        "runs"][0]["text"]
                )
            except ValueError:
                item_type = ItemType.SONG
        match item_type:
            case ItemType.ARTIST:
                subscribers = convert_number(
                    string=entry_item[key]["flexColumns"][1][
                        "musicResponsiveListItemFlexColumnRenderer"][
                        "text"]["runs"][-1]["text"]
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

            case ItemType.VIDEO:
                length = entry_item[key]["flexColumns"][1][
                    "musicResponsiveListItemFlexColumnRenderer"][
                    "text"]["runs"][-1]["text"]
                views = convert_number(
                    string=entry_item[key]["flexColumns"][1][
                        "musicResponsiveListItemFlexColumnRenderer"][
                        "text"]["runs"][-3]["text"]
                )
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

            case ItemType.PLAYLIST:
                try:
                    length = int(
                        entry_item[key]["flexColumns"][1][
                            "musicResponsiveListItemFlexColumnRenderer"][
                            "text"]["runs"][-1]["text"]
                    )
                except (KeyError, IndexError, ValueError):
                    length = None
                try:
                    views = convert_number(
                        string=entry_item[key]["flexColumns"][1][
                            "musicResponsiveListItemFlexColumnRenderer"][
                            "text"]["runs"][-1]["text"]
                    )
                except (KeyError, IndexError, ValueError):
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

            case ItemType.SINGLE:
                release_year = entry_item[key]["flexColumns"][1][
                    "musicResponsiveListItemFlexColumnRenderer"][
                    "text"]["runs"][-1]["text"]
                endpoint = _extract_endpoint(
                    endpoint=entry_item[key]["navigationEndpoint"]
                )
                item = SingleItem(
                    item_title=item_title,
                    item_endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    release_year=int(release_year)
                )

            case ItemType.SONG:
                try:
                    length = convert_length(
                        length=entry_item[key]["flexColumns"][1][
                            "musicResponsiveListItemFlexColumnRenderer"][
                            "text"]["runs"][-1]["text"]
                    )
                except UnexpectedState:
                    length = None
                try:
                    reproduction = convert_number(
                        string=entry_item[key]["flexColumns"][2][
                            "musicResponsiveListItemFlexColumnRenderer"][
                            "text"]["runs"][-1]["text"]
                    )
                except IndexError:
                    reproduction = None
                endpoint = _extract_endpoint(
                    endpoint=entry_item[key]["flexColumns"][0][
                        "musicResponsiveListItemFlexColumnRenderer"][
                        "text"]["runs"][-1]["navigationEndpoint"]
                )
                item = SongItem(
                    item_title=item_title,
                    item_endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    length=length,
                    reproductions=reproduction,
                    artist_items=None,
                    album_item=None
                )

            case ItemType.EPISODE:
                endpoint = _extract_endpoint(
                    endpoint=entry_item[key]["flexColumns"][0][
                        "musicResponsiveListItemFlexColumnRenderer"][
                        "text"]["runs"][-1]["navigationEndpoint"]
                )
                item = EpisodeItem(
                    item_title=item_title,
                    item_endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    publication_date=None,
                    artist_items=None
                )

            case ItemType.PODCAST:
                endpoint = _extract_endpoint(
                    endpoint=entry_item[key]["navigationEndpoint"]
                )
                item = PodcastItem(
                    item_title=item_title,
                    item_endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    artist_items=None
                )

            case ItemType.PROFILE:
                item_handle = entry_item[key]["flexColumns"][1][
                    "musicResponsiveListItemFlexColumnRenderer"][
                    "text"]["runs"][-1]["text"]
                item = ProfileItem(
                    item_title=item_title,
                    item_endpoint=None,
                    thumbnail_url=thumbnail_url,
                    handle=item_handle
                )

            case _:
                raise UnregisteredItemType(item_type)

    elif ShelfItemStructType.MUSIC_TWO_ROW_ITEM.value in entry_item:
        key = ShelfItemStructType.MUSIC_TWO_ROW_ITEM.value
        thumbnail_url = entry_item[key]["thumbnailRenderer"][
            "musicThumbnailRenderer"]["thumbnail"][
            "thumbnails"][-1]["url"]
        item_title = entry_item[key]["title"]["runs"][0]["text"]
        endpoint = _extract_endpoint(
            endpoint=entry_item[key]["navigationEndpoint"]
        )
        if not item_type:
            try:
                item_type = ItemType(
                    entry_item[key]["subtitle"]["runs"][0]["text"]
                )
            except ValueError:
                item_type = ItemType.SINGLE
        match item_type:
            case ItemType.ARTIST:
                subscribers = convert_number(
                    string=entry_item[key]["subtitle"][
                        "runs"][0]["text"]
                )
                item = ArtistItem(
                    item_title=item_title,
                    item_endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    subscribers=subscribers
                )

            case ItemType.ALBUM:
                release_year = int(
                    entry_item[key]["subtitle"][
                        "runs"][-1]["text"]
                )
                sub_type = ItemType(
                    entry_item[key]["subtitle"][
                        "runs"][0]["text"]
                )
                match sub_type:
                    case ItemType.ALBUM:
                        item = AlbumItem(
                            item_title=item_title,
                            item_endpoint=endpoint,
                            thumbnail_url=thumbnail_url,
                            artist_items=None,
                            release_year=release_year
                        )

                    case ItemType.EP:
                        item = EPItem(
                            item_title=item_title,
                            item_endpoint=endpoint,
                            thumbnail_url=thumbnail_url,
                            artist_items=None,
                            release_year=release_year
                        )
                    case _:
                        raise UnregisteredItemType(sub_type)

            case ItemType.EP:
                release_year = int(
                    entry_item[key]["subtitle"][
                        "runs"][-1]["text"]
                )
                item = EPItem(
                    item_title=item_title,
                    item_endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    artist_items=None,
                    release_year=release_year
                )

            case ItemType.VIDEO:
                views = convert_number(
                    string=entry_item[key]["subtitle"]["runs"][-1]["text"]
                )
                item = VideoItem(
                    item_title=item_title,
                    item_endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    length=None,
                    views=views
                )

            case ItemType.PLAYLIST:
                item = PlaylistItem(
                    item_title=item_title,
                    item_endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    length=None,
                    views=None
                )

            case ItemType.SINGLE:
                release_year = int(
                    entry_item[key]["subtitle"][
                        "runs"][-1]["text"]
                )
                item = SingleItem(
                    item_title=item_title,
                    item_endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    release_year=int(release_year)
                )

            case ItemType.SONG:
                item = SongItem(
                    item_title=item_title,
                    item_endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    length=None,
                    reproductions=None,
                    album_item=None
                )

            case (
                ItemType.EPISODE |
                ItemType.PODCAST |
                ItemType.PROFILE
            ):
                raise UnexpectedState(item_type)

            case _:
                raise UnregisteredItemType(item_type)

    elif PanelItemStructType.PLAYLIST_PANEL_VIDEO.value in entry_item:
        key = PanelItemStructType.PLAYLIST_PANEL_VIDEO.value
        item_title = entry_item[key]["title"]["runs"][-1]["text"]
        endpoint = _extract_endpoint(
            entry_item[key]["navigationEndpoint"]
        )
        length = convert_length(
            length=entry_item[key]["lengthText"]["runs"][-1]["text"]
        )
        tmp = entry_item[key]["thumbnail"]["thumbnails"][-1]
        thumbnail_url = entry_item[key]["thumbnail"][
            "thumbnails"][-1]["url"]
        width, height = tmp["width"], tmp["height"]
        if width / height == 1:
            item = SongItem(
                item_title=item_title,
                item_endpoint=endpoint,
                thumbnail_url=thumbnail_url,
                length=length,
                album_item=None,
                artist_items=None
            )
        else:
            try:
                views = convert_number(
                    string=entry_item[key]["longBylineText"][
                        "runs"][-3]["text"]
                )
            except (KeyError, IndexError):
                views = None
            item = VideoItem(
                item_title=item_title,
                item_endpoint=endpoint,
                thumbnail_url=thumbnail_url,
                length=length,
                artist_items=None,
                views=views
            )
    elif (
            PanelItemStructType.AUTOMIX_PREVIEW_VIDEO.value in entry_item or
            PanelItemStructType.PLAYLIST_EXPANDABLE_MESSAGE.value in entry_item
    ):
        return None
    else:
        raise KeyNotFound(f'Content: {entry_item.keys()}')
    return item


def _extract_endpoint(endpoint: Dict) -> Endpoint:
    if EndpointType.BROWSE_ENDPOINT.value in endpoint:
        endpoint_data = endpoint["browseEndpoint"]
        browse_id = endpoint_data["browseId"]
        browse_endpoint = BrowseEndpoint(
            browse_id=browse_id,
            params=endpoint_data.get("params", None)
        )
        return browse_endpoint

    elif EndpointType.WATCH_ENDPOINT.value in endpoint:
        endpoint_data = endpoint["watchEndpoint"]
        video_id = endpoint_data["videoId"]
        watch_endpoint = WatchEndpoint(
            video_id=video_id,
            playlist_id=endpoint_data.get("playlist_id", None),
            params=endpoint_data.get("params", None)
        )
        return watch_endpoint

    elif EndpointType.SEARCH_ENDPOINT.value in endpoint:
        endpoint_data = endpoint["searchEndpoint"]
        query = endpoint_data["query"]
        search_endpoint = SearchEndpoint(
            query=query,
            params=endpoint_data.get("params", None)
        )
        return search_endpoint

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
