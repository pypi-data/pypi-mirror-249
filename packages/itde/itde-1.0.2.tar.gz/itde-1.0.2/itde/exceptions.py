class ITDEBaseException(BaseException):
    """ InnerTube Data Extractor Base Exception """


class InvalidKey(ITDEBaseException, KeyError):
    """ """


class KeyNotFound(ITDEBaseException, KeyError):
    """ """


class UnknownElement(ITDEBaseException):
    """ """


class UnknownEndpoint(UnknownElement):
    """ """


class UnexpectedState(ITDEBaseException):
    """ """


class UnregisteredElement(ITDEBaseException):
    """ """


class UnregisteredShelfType(UnregisteredElement):
    """ """


class UnregisteredItemType(UnregisteredElement):
    """ """
