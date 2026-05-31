import json
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

import requests

query = input("Enter your query: ")

url = "http://export.arxiv.org/api/query"

params = {"search_query": f"all:{query}", "start": 0, "max_results": 25}

try:
    response = requests.get(url, params=params, timeout=30)

    print("Status:", response.status_code)

    if response.status_code != 200:
        print(response.text)
        exit()

    root = ET.fromstring(response.text)

    namespace = {"atom": "http://www.w3.org/2005/Atom"}

    papers = []

    for entry in root.findall("atom:entry", namespace):
        authors = []

        for author in entry.findall("atom:author", namespace):
            authors.append(author.find("atom:name", namespace).text)

        paper = {
            "title": entry.find("atom:title", namespace).text.strip(),
            "summary": entry.find("atom:summary", namespace).text.strip(),
            "published": entry.find("atom:published", namespace).text,
            "updated": entry.find("atom:updated", namespace).text,
            "authors": authors,
            "url": entry.find("atom:id", namespace).text,
        }

        papers.append(paper)

    output = {
        "query": query,
        "source": "arxiv",
        "collected_at": datetime.now().isoformat(),
        "total_results": len(papers),
        "results": papers,
    }

    Path("workspace").mkdir(exist_ok=True)

    with open("workspace/arxiv.json", "w", encoding="utf-8") as file:
        json.dump(output, file, indent=4, ensure_ascii=False)

    print(f"\nCollected {len(papers)} papers")
    print("Saved to workspace/arxiv.json")

except Exception as e:
    print("Error:", e)
