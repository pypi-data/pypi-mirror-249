class SearchEngineBaseException(BaseException):
    """ Base exception class for the Search Engine """


class InvalidKey(SearchEngineBaseException):
    """ """


class KeyNotFound(SearchEngineBaseException):
    """ """


class UnknownElement(SearchEngineBaseException):
    """ """


class UnknownEndpoint(UnknownElement):
    """ """


class UnregisteredElement(SearchEngineBaseException):
    """ """


class UnregisteredShelfType(UnregisteredElement):
    """ """


class UnregisteredItemType(UnregisteredElement):
    """ """
