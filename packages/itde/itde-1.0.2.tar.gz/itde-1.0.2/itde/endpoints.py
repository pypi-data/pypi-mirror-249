from .ytypes import EndpointType


class Endpoint:
    def __init__(
            self,
            params: str = None,
            endpoint_type: EndpointType = None,
    ) -> None:
        self.endpoint_type: EndpointType = endpoint_type
        self.params: str = params

    def __repr__(self):
        return (
            'Endpoint{'
            f'endpoint_type={self.endpoint_type.value}, '
            f'params={self.params}'
            '}'
        )


class BrowseEndpoint(Endpoint):
    def __init__(
            self,
            browse_id: str = None,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.browse_id: str = browse_id
        self.endpoint_type: EndpointType = EndpointType.BROWSE_ENDPOINT

    def __repr__(self):
        return (
            super().__repr__()[:-1] +
            f', browse_id={self.browse_id}'
            '}'
        )


class SearchEndpoint(Endpoint):
    def __init__(
            self,
            query: str = None,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.query: str = query
        self.endpoint_type: EndpointType = EndpointType.SEARCH_ENDPOINT

    def __repr__(self):
        return (
            super().__repr__()[:-1] +
            f', query={self.query}'
            '}'
        )


class WatchEndpoint(Endpoint):
    def __init__(
            self,
            video_id: str = None,
            playlist_id: str = None,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.video_id: str = video_id
        self.playlist_id: str = playlist_id
        self.endpoint_type: EndpointType = EndpointType.WATCH_ENDPOINT

    def __repr__(self):
        return (
            super().__repr__()[:-1] +
            f', video_id={self.video_id}'
            f', playlist_id={self.playlist_id}'
            '}'
        )


class UrlEndpoint(Endpoint):
    def __init__(
            self,
            url: str,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.url: str = url

    def __repr__(self):
        return (
            super().__repr__()[:-1] +
            f',url={self.url}'
            '}'
        )
