def select_top_results(records: list, limit: int = 10) -> list:
    """
    Keeps only the top N results per category.
    Assumes records are already ranked by score.
    """
    if not records:
        return []
        
    category_counts = {}
    selected_records = []
    
    for record in records:
        category = record.get("category", "Other")
        count = category_counts.get(category, 0)
        
        if count < limit:
            selected_records.append(record)
            category_counts[category] = count + 1
            
    return selected_records
