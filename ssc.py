import json
from datetime import datetime
from pathlib import Path

import requests

query = input("Enter your query: ")

url = "https://api.semanticscholar.org/graph/v1/paper/search"

params = {
    "query": query,
    "limit": 25,
    "fields": "title,abstract,year,citationCount,influentialCitationCount,authors,fieldsOfStudy,url",
}

try:
    response = requests.get(url, params=params, timeout=30)

    print("Status:", response.status_code)

    if response.status_code != 200:
        print(response.text)
        exit()

    raw_data = response.json()

    papers = []

    for paper in raw_data.get("data", []):
        authors = []

        for author in paper.get("authors", []):
            authors.append(author.get("name"))

        papers.append(
            {
                "title": paper.get("title"),
                "abstract": paper.get("abstract"),
                "year": paper.get("year"),
                "citation_count": paper.get("citationCount"),
                "influential_citation_count": paper.get("influentialCitationCount"),
                "authors": authors,
                "fields_of_study": paper.get("fieldsOfStudy", []),
                "url": paper.get("url"),
            }
        )

    output = {
        "query": query,
        "source": "semantic_scholar",
        "collected_at": datetime.now().isoformat(),
        "total_results": len(papers),
        "results": papers,
    }

    Path("workspace").mkdir(exist_ok=True)

    with open("workspace/semantic_scholar.json", "w", encoding="utf-8") as file:
        json.dump(output, file, indent=4, ensure_ascii=False)

    print(f"\nCollected {len(papers)} papers")
    print("Saved to workspace/semantic_scholar.json")

except Exception as e:
    print("Error:", e)
