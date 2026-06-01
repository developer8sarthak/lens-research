import json
import sys
from pathlib import Path
from core.registry import COLLECTORS
from core.workspace import create_workspace, save_json
from core.collector_manager import run_collectors
from core.report_generator import generate_reports

def print_progress(iteration, total, prefix='', length=30):
    """Prints a cozy and minimal progress bar."""
    percent = int(100 * (iteration / total))
    filled_length = int(length * iteration // total)
    bar = '█' * filled_length + '░' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} {bar} {percent}% ({iteration}/{total})')
    sys.stdout.flush()
    if iteration == total:
        sys.stdout.write('\n')

def main():
    print("=== Research Agent Refactored ===")
    query = input("Enter your research query: ").strip()
    
    if not query:
        print("Query cannot be empty.")
        return

    # 1. Create workspace
    print(f"\n[*] Creating workspace for: {query}")
    workspace = create_workspace(query)
    
    # 2. Execute collectors in parallel with animation
    print(f"[*] Researching across {len(COLLECTORS)} sources...")
    
    execution_reports = []
    total_collectors = len(COLLECTORS)
    
    # Initialize progress bar
    print_progress(0, total_collectors, prefix='Progress:')
    
    for i, report in enumerate(run_collectors(COLLECTORS, query), 1):
        execution_reports.append(report)
        print_progress(i, total_collectors, prefix='Progress:')
    
    # 3. Save results and generate metadata
    success_count = 0
    failed_count = 0
    
    metadata = {
        "query": query,
        "timestamp": workspace["timestamp"],
        "collectors": []
    }
    
    for report in execution_reports:
        collector_name = report["collector"]
        status = report["status"]
        
        collector_meta = {
            "name": collector_name,
            "status": status
        }
        
        if status == "success":
            success_count += 1
            data = report["data"]
            file_path = workspace["raw"] / f"{collector_name}.json"
            save_json(file_path, data)
            collector_meta["results_count"] = data.get("total_results") or data.get("total_posts") or 0
        else:
            failed_count += 1
            error_log_path = workspace["logs"] / f"{collector_name}_error.log"
            with open(error_log_path, "w", encoding="utf-8") as f:
                f.write(f"Error: {report['error']}\n\n")
                f.write(report["traceback"])
            collector_meta["error"] = report["error"]
            
        metadata["collectors"].append(collector_meta)
    
    # Save metadata.json
    save_json(workspace["base"] / "metadata.json", metadata)
    
    # 4. Final summary
    print("\n=== Execution Summary ===")
    print(f"Workspace: {workspace['base']}")
    print(f"Total Collectors: {len(COLLECTORS)}")
    print(f"Succeeded: {success_count}")
    print(f"Failed: {failed_count}")
    
    print("\nDetails:")
    for c in metadata["collectors"]:
        res = f" ({c.get('results_count', 0)} results)" if "results_count" in c else ""
        print(f" - {c['name']}: {c['status']}{res}")
    
    print("\n[*] Generating reports...")
    report_paths = generate_reports(workspace)
    if report_paths:
        print(f"[*] Reports saved in: {workspace['base']}/reports/")
        for path in report_paths:
            print(f" - {path.name}")
    
    print("\n[*] Research run complete.")

if __name__ == "__main__":
    main()
