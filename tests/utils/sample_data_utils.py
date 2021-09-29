import json
from pathlib import Path
from typing import Dict, Any


def get_sample_data_response(data_path: Path, json_file) -> Dict[str, Any]:
    json_path = data_path.joinpath(json_file)

    with json_path.open(mode='r') as f:
        return json.load(f)["response"]
