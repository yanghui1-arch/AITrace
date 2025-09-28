import os
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
        api_key: str | None = None,
        workspace: str | None = None,
        use_local: bool = False,
        url: str | None = None 
    ):
        """Initialize ATConfigurator
        ATConfigurator duty is to configure apikey, workspace and whether user start local option.

        Args:
             api_key(str | None): AT api key. Default to `None`.
             worksapce(str | None): workspace. Default to `None`.
             use_local(bool): whether start local serve option. Default to `False`.
             url(str | None): connect url
        """

        self._apikey = api_key
        self._workspace = workspace
        self._use_local = use_local

        if url is None:
            self._url = CLOUD_BASE_URL if self._use_local is False else localhost_base_url
        else:
            self._url = url
        

    def configure(self):
        """configure AT"""
        # TODO: skip configure when user configure one last time.

        if self.use_local is False:
            self._configure_cloud()
        else:
            self._configure_local()

    def _configure_cloud(self):
        """configure AT cloud"""
        ...

    def _configure_local(self):
        """configure AT local"""
        # configure local doesn't need an apikey
        self._apikey = None
        raise NotImplementedError("It is not supported currently. Please wait for a few days and switch to use cloud serve. Thanks.")

    @property
    def apikey(self) -> str | None:
        return self._apikey

    @property
    def workspace(self) -> str | None:
        return self._workspace

    @property
    def use_local(self) -> bool:
        return self._use_local
    
    @property
    def url(self) -> str:
        return self._url

def _set_configuration_in_os(
    api_key:str | None,
    workspace: str | None
):
    """Set apikey and worksapce into OS enviroment.
    Only call it using cloud serve.

    Args:
        api_key(str | None): AT api key
        workspace(str | None): AT workspace
    """

    if api_key is not None:
        os.environ["AT_API_KEY"] = api_key
    if workspace is not None:
        os.environ["AT_WORKSPACE"] = workspace

def configure(
    api_key: str | None = None,
    workspace: str | None = None,
    use_local: bool = False,
    url: str | None = None 
):
    """Configure AT
    
    Args:
        api_key(str | None): AT api key. Default to `None`.
        worksapce(str | None): workspace. Default to `None`.
        use_local(bool): whether start local serve option. Default to `False`.
        url(str | None): connect url
    """

    configurator = ATConfigurator(
        api_key=api_key,
        workspace=workspace,
        use_local=use_local,
        url=url
    )
    configurator.configure()
