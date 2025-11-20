# loader.py
import json
from pathlib import Path
from .types import ATConfig

CONFIG_PATH = Path.home() / ".aitrace" / "config.json"


def load_config() -> ATConfig:
    """Load config from ~/.aitrace/config.json"""
    if CONFIG_PATH.exists():
        with CONFIG_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return ATConfig(**data)
    
    return ATConfig()  # default config

def save_config(config: ATConfig):
    """Save config to ~/.aitrace/config.json"""
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CONFIG_PATH.open("w", encoding="utf-8") as f:
        json.dump(config.model_dump(), f, indent=4)
