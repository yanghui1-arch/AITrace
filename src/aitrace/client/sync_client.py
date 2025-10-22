import httpx
import functools
from .config import ClientConfig, build_client_config
from ..models import Step, Trace

class SyncClient:
    """SyncClient is to communicate with server.
    It works sync now. TODO: Later add an async work function.
    Currently it supports track step, trace and conversation.
    """

    def __init__(
        self,
        project_name: str | None = None,
        host_url: str | None = None,
        apikey: str | None = None,
    ):
        client_config = build_client_config(
            project_name=project_name,
            host_url=host_url,
            apikey=apikey
        )
        self._project_name = client_config.project_name
        self._host_url = client_config.host_url
        self._apikey = client_config.apikey

        self._client = httpx.Client(
            base_url=client_config.host_url,
            headers=client_config.headers
        )

    def track_trace(self, ):
        pass

    def track_step(self, ):
        pass

    @property
    def project_name(self):
        return self._project_name
    
    @property
    def host_url(self):
        return self._host_url


@functools.lru_cache()
def get_cached_sync_client() -> SyncClient:
    client = SyncClient()

    return client