from typing import Final

CLOUD_BASE_URL: Final[str] = "http://www.petmate.fun/"
localhost_base_url: str  = "http://localhost:5173/"

class ATConfigurator:
    """AI trace configurator
    Use api key to connect with cloud serve or host local serve. Otherwise be unable to use anything
    about AT.
    User can get api key from cloud at `http://www.petmate.fun/`
    """

    def __init__(
        self,
        api_key: str | None,
        workspace: str | None,
        use_local: bool = False
    ):
       self._apikey = api_key
       self._workspace = workspace
       self._use_local = use_local

    def configure(self):
        """configure AT"""
        # TODO: skip configure when user configure one last time.

        if self.use_local is False:
            self._configure_cloud()
        else:
            self._configure_local

    def _configure_cloud(self):
        """configure AT cloud"""
        ...

    def _configure_local(self):
        """configure AT local"""
        ...

    @property
    def apikey(self) -> str:
        return self._apikey

    @property
    def workspace(self) -> str:
        return self._workspace

    @property
    def use_local(self) -> bool:
        return self._use_local
 