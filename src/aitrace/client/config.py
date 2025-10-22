from dataclasses import dataclass
from typing import Any, Dict

# TODO: update it before deploy
DEFAULT_HOST_URL = "http://localhost:8080/api/v0"
DEFAULT_PROJECT_NAME = "Default project"
DEFAULT_API_KEY = "<DEFAULT_LOCAL_API_KEY>"

@dataclass
class ClientConfig:
    headers: Dict[str, Any]
    host_url: str = DEFAULT_HOST_URL
    project_name: str = DEFAULT_PROJECT_NAME
    apikey: str = DEFAULT_API_KEY

def build_client_config(
    project_name: str | None,
    host_url: str | None,
    apikey: str | None,
) -> ClientConfig:
    if project_name is None:
        import warnings
        warnings.warn(f"[AITrace] Project name is empty. AITrace will set it `{DEFAULT_PROJECT_NAME}`.")
        project_name = DEFAULT_PROJECT_NAME
    if host_url is None:
        import warnings
        warnings.warn(f"[AITrace] host_url is empty. AITrace will set it `{DEFAULT_HOST_URL}`")
        host_url = DEFAULT_HOST_URL
    if apikey is None:
        import os
        if os.environ.get('AITRACE_API_KEY', None) is None:
            import warnings
            warnings.warn(f"[AITrace] apikey is empty. AITrace will set it `{DEFAULT_API_KEY}`")
            apikey = DEFAULT_API_KEY
        else:
            apikey = os.environ.get('AITRACE_API_KEY')
    
    headers={
        "Authorization": f"Bearer {apikey}",
        "Content-Type": "application/json"
    }

    return ClientConfig(
        host_url=host_url,
        project_name=project_name,
        apikey=apikey,
        headers=headers
    )
