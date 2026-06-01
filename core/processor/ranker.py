import re

def calculate_score(query: str, title: str, description: str) -> int:
    """
    Calculates a relevance score from 0 to 100 based on keyword overlap.
    """
    if not query:
        return 0
        
    query_words = set(re.findall(r'\w+', query.lower()))
    if not query_words:
        return 0
        
    title_words = set(re.findall(r'\w+', title.lower()))
    desc_words = set(re.findall(r'\w+', description.lower()))
    
    # Weighting
    title_matches = len(query_words.intersection(title_words))
    desc_matches = len(query_words.intersection(desc_words))
    
    # Title match score (max 70 points)
    title_score = (title_matches / len(query_words)) * 70
    
    # Description match score (max 30 points)
    desc_score = (desc_matches / len(query_words)) * 30
    
    final_score = min(100, int(title_score + desc_score))
    return final_score

def rank_records(query: str, records: list) -> list:
    """
    Scores and sorts records based on relevance to the query.
    """
    for record in records:
        score = calculate_score(
            query, 
            record.get("title", ""), 
            record.get("description", "")
        )
        record["score"] = score
        
    # Sort by score descending
    return sorted(records, key=lambda x: x.get("score", 0), reverse=True)
