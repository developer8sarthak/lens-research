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
    "accent": "#AF5FFF",  # Purple
    "fail": "#FF5F5F",    # Muted red
    "success": "white",
    "header": "white",
    "dim": "dim",
})

console = Console(theme=THEME)

def print_header():
    console.print("[accent]Lens.[/accent]")
    console.rule(style="dim")
    console.print()

@click.group()
@click.version_option(version="0.1.0", prog_name="lens")
def main():
    """Lens: Local AI-powered research agent."""
    pass

@main.command()
@click.argument("query")
def research(query):
    """Run research on a given query."""
    clean_query = query.strip()
    if not clean_query:
        console.print("[fail]Error: Query cannot be empty or just whitespace.[/fail]")
        return

    print_header()
    
    console.print("[dim]Research[/dim]")
    console.print(f"[white]{clean_query}[/white]")
    console.print()
    
    # 1. Create workspace
    workspace = create_workspace(clean_query)
    console.print("[dim]Workspace[/dim]")
    console.print(f"[white]{workspace['base']}[/white]")
    console.print()
    
    # 2. Execute collectors
    console.print("[dim]Collecting Sources[/dim]")
    console.print()

    execution_reports = []
    total_collectors = len(COLLECTORS)
    
    with Progress(
        SpinnerColumn(),
        BarColumn(bar_width=30),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}% ({task.completed}/{task.total})"),
        console=console
    ) as progress:
        task = progress.add_task("Collecting...", total=total_collectors)
        
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
    console.print("[dim]Results[/dim]")
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
            table.add_row(name, "success", str(count))
        else:
            failed += 1
            table.add_row(name, "[fail]failed[/fail]", "")
            
    console.print(table)
    console.print()
    
    # Summary
    console.print("[dim]Summary[/dim]")
    console.print()
    console.print(f"[dim]Sources[/dim]             {total_collectors}")
    console.print(f"[dim]Succeeded[/dim]           {succeeded}")
    console.print(f"[dim]Failed[/dim]              {failed}")
    console.print()
    
    console.print("[white]Research complete.[/white]")

if __name__ == "__main__":
    main()
