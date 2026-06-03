def normalize_item(item: dict, source: str) -> dict:
    """
    Normalizes a single data item from any source into a standard format.
    """
    normalized = {
        "source": source,
        "title": "",
        "description": "",
        "url": ""
    }
    
    # Title resolution
    normalized["title"] = (
        item.get("title") or 
        item.get("name") or 
        item.get("full_name") or 
        "No Title"
    )
    
    # Description resolution
    normalized["description"] = (
        item.get("summary") or 
        item.get("description") or 
        item.get("abstract") or 
        item.get("selftext") or 
        ""
    )
    
    # URL resolution
    normalized["url"] = (
        item.get("url") or 
        item.get("html_url") or 
        item.get("pdf_url") or 
        item.get("permalink") or 
        ""
    )
    
    # Clean up strings (strip whitespace/newlines)
    for key in ["title", "description"]:
        if isinstance(normalized[key], str):
            normalized[key] = normalized[key].strip().replace("\n", " ")
            if len(normalized[key]) > 500: # Truncate very long descriptions for report
                normalized[key] = normalized[key][:497] + "..."

    return normalized

def parse_collector_data(data: dict) -> list:
    """
    Parses a collector's JSON output and returns a list of normalized items.
    """
    source = data.get("source", "unknown")
    results = data.get("results", [])
    
    if not isinstance(results, list):
        return []
        
    return [normalize_item(item, source) for item in results]
