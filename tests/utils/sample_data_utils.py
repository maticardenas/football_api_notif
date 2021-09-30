import json
import os
from pathlib import Path
from typing import Dict, Any


def get_sample_data_response(data_path: Path, json_file) -> Dict[str, Any]:
    json_path = os.path.join(data_path, json_file)

    with open(json_path, mode='r') as f:
        return json.load(f)["response"]
