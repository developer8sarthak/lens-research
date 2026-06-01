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
        
        # Categorize by processed category
        category = item.get("category", "Other")
        
        if category == "Academic Papers":
            sections["academic_papers"].append(item)
        elif category == "Repositories":
            sections["repositories"].append(item)
        elif category in ["Knowledge Sources", "News", "Companies", "People"]:
            # Grouping web-like results for the standard template sections
            sections["web_results"].append(item)
        else:
            sections["other"].append(item)
            
    return sections
