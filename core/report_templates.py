from datetime import datetime

def generate_report_content(query: str, normalized_data: list) -> dict:
    """
    Groups and organizes normalized data into sections for the report.
    """
    sections = {
        "topic": query,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_records": len(normalized_data),
        "source_stats": {},
        "academic_papers": [],
        "repositories": [],
        "web_results": [],
        "other": []
    }
    
    # Calculate stats and group items
    for item in normalized_data:
        source = item["source"]
        sections["source_stats"][source] = sections["source_stats"].get(source, 0) + 1
        
        # Categorize by source type
        academic_sources = ["arxiv", "crossref", "openalex", "semantic_scholar"]
        repo_sources = ["github"]
        web_sources = ["wikipedia", "reddit"]
        
        if source in academic_sources:
            sections["academic_papers"].append(item)
        elif source in repo_sources:
            sections["repositories"].append(item)
        elif source in web_sources:
            sections["web_results"].append(item)
        else:
            sections["other"].append(item)
            
    return sections
