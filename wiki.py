import html
import json
from pathlib import Path

import requests

SEARCH_URL = "https://en.wikipedia.org/w/api.php"
SUMMARY_URL = "https://en.wikipedia.org/api/rest_v1/page/summary/"

headers = {"User-Agent": "ResearchAgent/1.0"}

query = input("Enter your query: ")

try:
    search_params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json",
    }

    search_response = requests.get(
        SEARCH_URL, params=search_params, headers=headers, timeout=10
    )

    search_response.raise_for_status()

    search_data = search_response.json()

    search_results = search_data.get("query", {}).get("search", [])[:5]

    results = []

    for item in search_results:
        title = item.get("title", "")

        try:
            summary_response = requests.get(
                SUMMARY_URL + title.replace(" ", "_"), headers=headers, timeout=10
            )

            if summary_response.status_code != 200:
                continue

            summary_data = summary_response.json()

            results.append(
                {
                    "title": summary_data.get("title"),
                    "pageid": summary_data.get("pageid"),
                    "summary": html.unescape(summary_data.get("extract", "")),
                    "description": summary_data.get("description", ""),
                    "url": summary_data.get("content_urls", {})
                    .get("desktop", {})
                    .get("page", ""),
                }
            )

        except Exception as e:
            print(f"Failed to fetch summary for {title}: {e}")

    output = {
        "query": query,
        "source": "wikipedia",
        "total_results": len(results),
        "results": results,
    }

    Path("workspace").mkdir(exist_ok=True)

    with open("workspace/wiki.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    print(f"\nCollected {len(results)} articles")
    print("Saved to workspace/wiki.json")

except Exception as e:
    print(f"Error: {e}")
