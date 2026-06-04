import json
import os
from datetime import datetime
from pathlib import Path

def create_workspace(query: str) -> dict:
    # Clean query for folder name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    workspace_name = f"session_{timestamp}"
    
    base_dir = Path("workspace") / workspace_name
    raw_dir = base_dir / "raw"
    logs_dir = base_dir / "logs"
    
    raw_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    return {
        "base": base_dir,
        "raw": raw_dir,
        "logs": logs_dir,
        "name": workspace_name,
        "query": query,
        "timestamp": timestamp
    }

def save_json(path: Path, data: dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
