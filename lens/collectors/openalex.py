from datetime import datetime
import requests

def collect(query: str) -> dict:
    url = "https://api.openalex.org/works"
    params = {"search": query, "per-page": 25}

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    raw_data = response.json()
    papers = []

    for work in raw_data.get("results", []):
        authors = []
        for authorship in work.get("authorships", []):
            author = authorship.get("author", {})
            if author:
                authors.append(author.get("display_name"))

        institutions = []
        for authorship in work.get("authorships", []):
            for institution in authorship.get("institutions", []):
                name = institution.get("display_name")
                if name and name not in institutions:
                    institutions.append(name)

        papers.append(
            {
                "title": work.get("title"),
                "publication_year": work.get("publication_year"),
                "cited_by_count": work.get("cited_by_count"),
                "authors": authors,
                "institutions": institutions,
                "doi": work.get("doi"),
                "openalex_id": work.get("id"),
                "type": work.get("type"),
                "language": work.get("language"),
                "open_access": work.get("open_access", {}).get("is_oa"),
                "pdf_url": work.get("open_access", {}).get("oa_url"),
            }
        )

    return {
        "query": query,
        "source": "openalex",
        "collected_at": datetime.now().isoformat(),
        "total_results": len(papers),
        "results": papers,
    }
