from enum import Enum


class SearchResultStrucType(Enum):
    TABBED_SEARCH_RESULTS = "tabbedSearchResultsRenderer"


class BrowseResultStrucType(Enum):

    SINGLE_COLUMN_BROWSE_RESULTS = "singleColumnBrowseResultsRenderer"


class NextResultStrucType(Enum):

    SINGLE_COLUMN_MUSIC_WATCH_NEXT_RESULT = "singleColumnMusicWatchNextResultsRenderer"


class PanelStructType(Enum):

    PLAYLIST_PANEL = "playlistPanelRenderer"


class ShelfStructType(Enum):

    GRID = "gridRenderer"
    MUSIC_SHELF = "musicShelfRenderer"
    MUSIC_CARD_SHELF = "musicCardShelfRenderer"
    MUSIC_CAROUSEL_SHELF = "musicCarouselShelfRenderer"
    MUSIC_DESCRIPTION_SHELF = "musicDescriptionShelfRenderer"


class SectionType(Enum):
    ITEM_SECTION = "itemSectionRenderer"


class PanelItemStructType(Enum):
    PLAYLIST_PANEL_VIDEO = "playlistPanelVideoRenderer"
    PLAYLIST_EXPANDABLE_MESSAGE = "playlistExpandableMessageRenderer"
    AUTOMIX_PREVIEW_VIDEO = "automixPreviewVideoRenderer"


class ShelfItemStructType(Enum):
    MUSIC_TWO_ROW_ITEM = "musicTwoRowItemRenderer"
    MUSIC_RESPONSIVE_LIST_ITEM = "musicResponsiveListItemRenderer"


class ShelfType(Enum):
    TOP_RESULT = "Top result"
    SONG = "Song"
    VIDEO = "Video"
    PLAYLIST = "Playlist"
    ALBUM = "Album"
    ARTIST = "Artist"
    EPISODE = "Episode"
    SONGS = "Songs"
    VIDEOS = "Videos"
    COMMUNITY_PLAYLIST = "Community playlists"
    FEATURED_PLAYLIST = "Featured playlists"
    ALBUMS = "Albums"
    ARTISTS = "Artists"
    SINGLES = "Singles"
    EPISODES = "Episodes"
    PODCASTS = "Podcasts"
    PROFILES = "Profiles"
    FEATURED_ON = "Featured on"
    FANS_MIGHT_ALSO_LIKE = "Fans might also like"


class ItemType(Enum):
    SONG = "Song"
    SINGLE = "Single"
    VIDEO = "Video"
    PLAYLIST = "Playlist"
    ALBUM = "Album"
    EP = "EP"
    ARTIST = "Artist"
    EPISODE = "Episode"
    PROFILE = "Profile"
    PODCAST = "Podcast"


class EndpointType(Enum):
    WATCH_ENDPOINT = "watchEndpoint"
    BROWSE_ENDPOINT = "browseEndpoint"
    SEARCH_ENDPOINT = "searchEndpoint"
    URL_ENDPOINT = "urlEndpoint"


class IconType(Enum):
    ARTIST = "ARTIST"
    ALBUM = "ALBUM"
    SHARE = "SHARE"
    FLAG = "FLAG"
    MIX = "MIX"
    REMOVE = "REMOVE"
    QUEUE_PLAY_NEXT = "QUEUE_PLAY_NEXT"
    FAVORITE = "FAVORITE"
    UNFAVORITE = "UNFAVORITE"
    ADD_TO_REMOTE_QUEUE = "ADD_TO_REMOTE_QUEUE"
    ADD_TO_PLAYLIST = "ADD_TO_PLAYLIST"


class TextDivisorType(Enum):
    BULLET_POINT = '\u2022'
