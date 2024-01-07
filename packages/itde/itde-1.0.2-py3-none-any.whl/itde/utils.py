import re
from datetime import time
from datetime import date

from .ytypes import ShelfType
from .ytypes import ItemType

from .exceptions import UnregisteredShelfType
from .exceptions import UnexpectedState


def convert_number(string: str) -> int:
    # It works with:
    # - subscribers
    # - views
    # - reproductions

    match = re.search(r'(\d+\.\d+|\d+)([BMK])?', string)
    result = match.group()
    last_char = result[-1]
    try:
        if last_char.isupper():
            number = float(result[:-1])
            match last_char:
                case 'B':
                    return int(number * 1000000000)
                case 'M':
                    return int(number * 1000000)
                case 'K':
                    return int(number * 1000)
                case _:
                    raise ValueError(f"Unexpected character: {last_char}")
        else:
            return int(result)
    except ValueError as error:
        raise UnexpectedState(error)


def get_item_type(shelf_type: ShelfType) -> ItemType | None:
    match shelf_type:
        case (
             ShelfType.SONG
             ) | (
             ShelfType.SONGS
             ) | (
        ):
            return ItemType.SONG

        case (
             ShelfType.SINGLES
             ) | (
        ):
            return ItemType.SINGLE

        case (
             ShelfType.VIDEO
             ) | (
             ShelfType.VIDEOS
        ):
            return ItemType.VIDEO

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

        case (
             ShelfType.ALBUM
             ) | (
             ShelfType.ALBUMS
        ):
            return ItemType.ALBUM

        case (
             ShelfType.ARTIST
             ) | (
             ShelfType.ARTISTS
             ) | (
             ShelfType.FANS_MIGHT_ALSO_LIKE
        ):
            return ItemType.ARTIST

        case (
             ShelfType.EPISODE
             ) | (
             ShelfType.EPISODES
        ):
            return ItemType.EPISODE

        case ShelfType.PROFILES:
            return ItemType.PROFILE

        case ShelfType.PODCASTS:
            return ItemType.PODCAST

        case ShelfType.TOP_RESULT:
            return None

        case _:
            raise UnregisteredShelfType(
                f"ShelfType: {shelf_type}"
            )


def convert_length(length: str) -> time:
    # length: 1:23; 1:2:34
    try:
        time_list = [int(x) for x in length.split(":")]
        match len(time_list):
            case 3:
                return time(
                    hour=time_list[0],
                    minute=time_list[1],
                    second=time_list[2]
                )
            case 2:
                return time(
                    minute=time_list[0],
                    second=time_list[1]
                )
            case _:
                raise ValueError("Unexpected time format")
    except ValueError as error:
        raise UnexpectedState(error)


def convert_publication_date(publication_date: str) -> date:
    # format example: Jan 1, 1984
    try:
        month, day, year = publication_date.split()
        return date(
            month=convert_month(month),
            day=int(day[:-1]),
            year=int(year)
        )
    except ValueError as error:
        raise UnexpectedState(error)


def convert_month(month: str) -> int:
    match month.lower():
        case 'jan':
            return 1
        case 'feb':
            return 2
        case 'mar':
            return 3
        case 'apr':
            return 4
        case 'may':
            return 5
        case 'jun':
            return 6
        case 'jul':
            return 7
        case 'aug':
            return 8
        case 'sep':
            return 9
        case 'oct':
            return 10
        case 'nov':
            return 11
        case 'dec':
            return 12
        case _:
            raise UnexpectedState(
                f'Unexpected month: {month}'
            )
