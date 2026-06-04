import click
import re
from rich.console import Console
from rich.theme import Theme
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn
from lens.core.registry import COLLECTORS
from lens.core.workspace import create_workspace, save_json
from lens.core.collector_manager import run_collectors
from lens.core.report_generator import generate_reports

# Define color palette
THEME = Theme({
    "accent": "#E0B0FF",      # Mauve: Primary accents and highlights
    "secondary": "#CCCCFF",   # Periwinkle: Secondary info and structure
    "fail": "#FF5F5F",        # Red: Failure states
    "success": "white",       # White: Main content and results
    "dim": "dim",
})

console = Console(theme=THEME)

def print_header():
    console.print("[accent]Lens.[/accent]")
    console.rule(style="secondary")
    console.print()

@click.group()
@click.version_option(version="0.1.1", prog_name="lens")
def main():
    """Lens: Local AI-powered research agent."""
    pass

@main.command()
@click.option("-q", "--query", help="Query text to research.")
@click.argument("query_arg", required=False)
def research(query, query_arg):
    """Run research on a given query."""
    clean_query = (query or query_arg or "").strip()
    if not clean_query:
        console.print("[fail]Error: Query cannot be empty. Use -q 'query' or provide it as an argument.[/fail]")
        return

    print_header()
    
    console.print("[secondary]Research[/secondary]")
    console.print(f"[white]{clean_query}[/white]")
    console.print()
    
    # 1. Create workspace
    workspace = create_workspace(clean_query)
    console.print("[secondary]Workspace[/secondary]")
    console.print(f"[white]{workspace['base']}[/white]")
    console.print()
    
    # 2. Execute collectors
    console.print("[secondary]Collecting Sources[/secondary]")
    console.print()

    execution_reports = []
    total_collectors = len(COLLECTORS)
    
    with Progress(
        SpinnerColumn(style="accent"),
        BarColumn(bar_width=30, complete_style="accent", finished_style="accent"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}% ({task.completed}/{task.total})", style="secondary"),
        console=console
    ) as progress:
        task = progress.add_task("[secondary]Collecting...[/secondary]", total=total_collectors)
        
        for report in run_collectors(COLLECTORS, clean_query):
            execution_reports.append(report)
            progress.advance(task)
            
    console.print()

    # 3. Save results
    for report in execution_reports:
        if report["status"] == "success":
            file_path = workspace["raw"] / f"{report['collector']}.json"
            save_json(file_path, report["data"])
    
    # 4. Generate reports
    generate_reports(workspace)
    
    # Results Table
    console.print("[secondary]Results[/secondary]")
    console.print()
    table = Table(box=None, expand=False, show_header=False)
    
    succeeded = 0
    failed = 0
    
    for report in execution_reports:
        name = report['collector']
        if report["status"] == "success":
            succeeded += 1
            data = report["data"]
            if isinstance(data, dict) and "results" in data:
                count = len(data["results"])
            elif isinstance(data, list):
                count = len(data)
            else:
                count = 0
            table.add_row(f"[white]{name}[/white]", "[accent]success[/accent]", f"[secondary]{count}[/secondary]")
        else:
            failed += 1
            table.add_row(f"[white]{name}[/white]", "[fail]failed[/fail]", "")
            
    console.print(table)
    console.print()
    
    # Summary
    console.print("[secondary]Summary[/secondary]")
    console.print()
    console.print(f"[secondary]Sources[/secondary]             [white]{total_collectors}[/white]")
    console.print(f"[secondary]Succeeded[/secondary]           [white]{succeeded}[/white]")
    console.print(f"[secondary]Failed[/secondary]              [fail]{failed}[/fail]")
    console.print()
    
    absolute_path = workspace['base'].resolve()
    console.print(f"[secondary]Session ID[/secondary]          [white]{workspace['name']}[/white]")
    console.print(f"[secondary]Path[/secondary]                [white]{absolute_path}[/white]")
    console.print()

    console.print(f"[accent]Workspace ready:[/accent] [white]{absolute_path}[/white]")


if __name__ == "__main__":
    main()
