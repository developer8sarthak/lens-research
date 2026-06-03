import difflib

def normalize_title(title: str) -> str:
    if not title:
        return ""
    return "".join(e for e in title.lower() if e.isalnum())

def are_similar(t1: str, t2: str, threshold: float = 0.85) -> bool:
    if not t1 or not t2:
        return False
    return difflib.SequenceMatcher(None, t1, t2).ratio() > threshold

def deduplicate(records: list) -> list:
    """
    Detects and merges duplicate records based on title similarity.
    """
    if not records:
        return []

    unique_records = []
    
    for record in records:
        title = record.get("title", "").strip()
        if not title:
            unique_records.append(record)
            continue
            
        is_duplicate = False
        for existing in unique_records:
            if are_similar(normalize_title(title), normalize_title(existing.get("title", ""))):
                # Merge source info
                existing_sources = existing.get("sources", [existing["source"]])
                if record["source"] not in existing_sources:
                    existing_sources.append(record["source"])
                existing["sources"] = existing_sources
                
                # Keep the longer description if available
                if len(record.get("description", "")) > len(existing.get("description", "")):
                    existing["description"] = record["description"]
                
                is_duplicate = True
                break
        
        if not is_duplicate:
            record["sources"] = [record["source"]]
            unique_records.append(record)
            
    return unique_records
