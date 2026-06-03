from datetime import datetime
import requests

def collect(query: str) -> dict:
    url = "https://api.crossref.org/works"
    params = {"query": query, "rows": 25}
    headers = {"User-Agent": "ResearchAgent/1.0"}

    response = requests.get(url, params=params, headers=headers, timeout=30)
    response.raise_for_status()

    raw_data = response.json()
    papers = []

    for item in raw_data.get("message", {}).get("items", []):
        authors = []
        for author in item.get("author", []):
            full_name = (
                author.get("given", "") + " " + author.get("family", "")
            ).strip()
            if full_name:
                authors.append(full_name)

        papers.append(
            {
                "title": item.get("title", [""])[0] if item.get("title") else "",
                "doi": item.get("DOI"),
                "publisher": item.get("publisher"),
                "type": item.get("type"),
                "authors": authors,
                "citation_count": item.get("is-referenced-by-count"),
                "journal": (
                    item.get("container-title", [""])[0]
                    if item.get("container-title")
                    else ""
                ),
                "published": item.get("created", {}).get("date-time"),
                "url": item.get("URL"),
            }
        )

    return {
        "query": query,
        "source": "crossref",
        "collected_at": datetime.now().isoformat(),
        "total_results": len(papers),
        "results": papers,
    }
