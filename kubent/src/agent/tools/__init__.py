from typing import Dict
from .toolkits import Tool
from .search import SearchGoogle

__all__ = ["Tool"]

"""TOOL_KITS is a collection of all tools.
Every tool will be added in TOOL_KITS.
"""
TOOL_KITS:Dict[str, Tool] = {
    "search_google": SearchGoogle()
}