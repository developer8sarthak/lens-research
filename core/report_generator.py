import json
import os
from pathlib import Path
from core.report_parsers import parse_collector_data
from core.report_templates import generate_report_content
from core.report_exporters import export_txt, export_md, export_html
from core.processor.processor import process_research_data

def generate_reports(workspace_info: dict):
    """
    Orchestrates the report generation process.
    """
    raw_dir = Path(workspace_info["raw"])
    reports_dir = Path(workspace_info["base"]) / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    all_normalized_data = []
    
    # 1. Discover and parse all JSON files in raw directory
    for file_path in raw_dir.glob("*.json"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                normalized_items = parse_collector_data(data)
                all_normalized_data.extend(normalized_items)
        except Exception as e:
            # Log error and continue (Failure Tolerance)
            error_log = Path(workspace_info["logs"]) / "report_generation_errors.log"
            with open(error_log, "a", encoding="utf-8") as f:
                f.write(f"Failed to process {file_path.name}: {str(e)}\n")
            continue

    if not all_normalized_data:
        return None

    # 1.5 Process research data (Deduplicate, Rank, Categorize, Select)
    processed_data = process_research_data(workspace_info["query"], all_normalized_data)

    # 2. Generate structured report content
    report_content = generate_report_content(workspace_info["query"], processed_data)
    
    # 3. Export to different formats
    outputs = {
        "report.txt": export_txt(report_content),
        "report.md": export_md(report_content),
        "report.html": export_html(report_content)
    }
    
    # 4. Save files
    saved_paths = []
    for filename, content in outputs.items():
        save_path = reports_dir / filename
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(content)
        saved_paths.append(save_path)
        
    return saved_paths
