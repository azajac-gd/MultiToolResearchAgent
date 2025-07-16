import json
from pathlib import Path
from functools import cache

CONFIG_PATH = Path(__file__).parent.parent/"config"/ "agent_config.json"

@cache
def load_agent_config() -> dict:
    with CONFIG_PATH.open(encoding="utf-8") as f:
        return json.load(f)
