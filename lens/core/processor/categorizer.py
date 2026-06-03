def categorize_record(record: dict) -> str:
    """
    Determines the category of a record based on source and content keywords.
    """
    source = record.get("source", "").lower()
    title = record.get("title", "").lower()
    description = record.get("description", "").lower()
    
    # Academic Papers
    academic_sources = ["arxiv", "crossref", "openalex", "semantic_scholar"]
    if source in academic_sources or "abstract" in description or "journal" in description:
        return "Academic Papers"
        
    # Repositories
    repo_sources = ["github"]
    if source in repo_sources or "repository" in description or "source code" in description:
        return "Repositories"
        
    # News
    if "news" in source or "breaking" in title or "daily" in title:
        return "News"
        
    # Companies
    company_keywords = ["inc.", "corp", "corporation", "limited", "ltd"]
    if any(k in title for k in company_keywords):
        return "Companies"
        
    # People
    if "biography" in description or "born" in description or "profile" in description:
        return "People"
        
    # Knowledge Sources
    knowledge_sources = ["wikipedia", "reddit"]
    if source in knowledge_sources:
        return "Knowledge Sources"
        
    return "Other"

def categorize_records(records: list) -> list:
    """
    Adds a category field to every record.
    """
    for record in records:
        record["category"] = categorize_record(record)
    return records
