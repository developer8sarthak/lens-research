def export_txt(data: dict) -> str:
    lines = [
        "=== RESEARCH REPORT ===",
        f"Topic: {data['topic']}",
        f"Date:  {data['timestamp']}",
        f"Total Records: {data['total_records']}",
        "",
        "--- SOURCE STATISTICS ---"
    ]
    for src, count in data["source_stats"].items():
        lines.append(f"- {src.capitalize()}: {count} records")
    
    def add_section_txt(title, items):
        if not items: return
        lines.append(f"\n--- {title.upper()} ---")
        for item in items:
            lines.append(f"\n[{item['source'].upper()}] {item['title']}")
            if item['url']: lines.append(f"URL: {item['url']}")
            if item['description']: lines.append(f"Summary: {item['description'][:200]}...")

    add_section_txt("Academic Papers", data["academic_papers"])
    add_section_txt("Repositories", data["repositories"])
    add_section_txt("Web Results", data["web_results"])
    add_section_txt("Other Findings", data["other"])
    
    lines.append("\n=== END OF REPORT ===")
    return "\n".join(lines)

def export_md(data: dict) -> str:
    lines = [
        f"# Research Report: {data['topic']}",
        f"**Generated on:** {data['timestamp']}",
        "",
        "## Summary",
        f"- **Total Records:** {data['total_records']}",
        "- **Sources Used:** " + ", ".join([s.capitalize() for s in data["source_stats"].keys()]),
        "",
        "## Source Breakdown",
        "| Source | Records |",
        "| :--- | :--- |"
    ]
    for src, count in data["source_stats"].items():
        lines.append(f"| {src.capitalize()} | {count} |")
    
    def add_section_md(title, items):
        if not items: return
        lines.append(f"\n## {title}")
        for item in items:
            lines.append(f"\n### {item['title']}")
            lines.append(f"- **Source:** {item['source'].capitalize()}")
            if item['url']: lines.append(f"- **URL:** [{item['url']}]({item['url']})")
            if item['description']: lines.append(f"\n> {item['description']}")
            lines.append("\n---")

    add_section_md("Academic Papers", data["academic_papers"])
    add_section_md("Repositories", data["repositories"])
    add_section_md("Web Results", data["web_results"])
    add_section_md("Other Findings", data["other"])
    
    return "\n".join(lines)

def export_html(data: dict) -> str:
    html = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        f"<title>Research Report - {data['topic']}</title>",
        "<style>",
        "body { font-family: sans-serif; line-height: 1.6; color: #333; max-width: 900px; margin: 40px auto; padding: 20px; }",
        "h1 { color: #2c3e50; border-bottom: 2px solid #eee; }",
        "h2 { color: #34495e; margin-top: 40px; border-left: 5px solid #3498db; padding-left: 10px; }",
        "h3 { color: #2980b9; }",
        ".meta { color: #7f8c8d; font-size: 0.9em; }",
        ".item { margin-bottom: 30px; padding: 15px; background: #f9f9f9; border-radius: 5px; }",
        "blockquote { font-style: italic; color: #555; border-left: 3px solid #ccc; margin: 10px 0; padding-left: 15px; }",
        "table { width: 100%; border-collapse: collapse; margin: 20px 0; }",
        "th, td { text-align: left; padding: 12px; border-bottom: 1px solid #eee; }",
        "th { background: #f4f4f4; }",
        "</style>",
        "</head>",
        "<body>",
        f"<h1>Research Report: {data['topic']}</h1>",
        f"<p class='meta'>Generated on: {data['timestamp']}</p>",
        "<h2>Summary</h2>",
        "<table>",
        "<tr><th>Metric</th><th>Value</th></tr>",
        f"<tr><td>Total Records</td><td>{data['total_records']}</td></tr>",
        f"<tr><td>Sources Used</td><td>{', '.join([s.capitalize() for s in data['source_stats'].keys()])}</td></tr>",
        "</table>",
        "<h2>Source Breakdown</h2>",
        "<table>",
        "<tr><th>Source</th><th>Count</th></tr>"
    ]
    
    for src, count in data["source_stats"].items():
        html.append(f"<tr><td>{src.capitalize()}</td><td>{count}</td></tr>")
    
    html.append("</table>")
    
    def add_section_html(title, items):
        if not items: return
        html.append(f"<h2>{title}</h2>")
        for item in items:
            html.append("<div class='item'>")
            html.append(f"<h3>{item['title']}</h3>")
            html.append(f"<p class='meta'>Source: {item['source'].capitalize()}</p>")
            if item['url']: html.append(f"<p>URL: <a href='{item['url']}'>{item['url']}</a></p>")
            if item['description']: html.append(f"<blockquote>{item['description']}</blockquote>")
            html.append("</div>")

    add_section_html("Academic Papers", data["academic_papers"])
    add_section_html("Repositories", data["repositories"])
    add_section_html("Web Results", data["web_results"])
    add_section_html("Other Findings", data["other"])
    
    html.append("</body></html>")
    return "\n".join(html)
