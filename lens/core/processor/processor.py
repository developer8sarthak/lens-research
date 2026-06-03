from .deduplicator import deduplicate
from .ranker import rank_records
from .categorizer import categorize_records
from .selector import select_top_results

def process_research_data(query: str, records: list, limit_per_category: int = 10) -> list:
    """
    Executes the research processing pipeline.
    """
    if not records:
        return []
        
    # 1. Deduplicate
    processed = deduplicate(records)
    
    # 2. Rank by relevance to query
    processed = rank_records(query, processed)
    
    # 3. Categorize
    processed = categorize_records(processed)
    
    # 4. Select top results per category
    processed = select_top_results(processed, limit=limit_per_category)
    
    return processed
