from .ytypes import EndpointType


class Endpoint:
    def __init__(
            self,
            params: str = None,
            endpoint_type: EndpointType = None,
    ) -> None:
        self.endpoint_type = endpoint_type
        self.params = params

    def __repr__(self):
        return f'endpoint_type={self.endpoint_type.value},params={self.params}'


class BrowseEndpoint(Endpoint):
    def __init__(
            self,
            browse_id: str = None,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.browse_id = browse_id
        self.endpoint_type = EndpointType.BROWSE_ENDPOINT

    def __repr__(self):
        return super().__repr__() + f',browse_id={self.browse_id}'


class SearchEndpoint(Endpoint):
    def __init__(
            self,
            query: str = None,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.query = query
        self.endpoint_type = EndpointType.SEARCH_ENDPOINT

    def __repr__(self):
        return super().__repr__() + f',query={self.query}'


class WatchEndpoint(Endpoint):
    def __init__(
            self,
            video_id: str = None,
            playlist_id: str = None,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.video_id = video_id
        self.playlist_id = playlist_id
        self.endpoint_type = EndpointType.WATCH_ENDPOINT

    def __repr__(self):
        return (
            super().__repr__() +
            f',video_id={self.video_id},playlist_id={self.playlist_id}'
        )


class UrlEndpoint(Endpoint):
    def __init__(
            self,
            url: str,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.url = url

    def __repr__(self):
        return super().__repr__() + f',url={self.url}'
