

class NotShardStaticException(Exception):
    pass


class NotDiffusibleException(Exception):
    pass


class InvalidDatabaseAliasException(Exception):
    pass


class NotExistsOriginalDataException(Exception):
    pass


class TooManySyncItemsException(Exception):
    pass


class DontExecuteException(Exception):
    pass


class DontLinkException(Exception):
    pass
