import json
from datetime import datetime
from pathlib import Path

import requests

query = input("Enter your query: ")

url = "https://api.github.com/search/repositories"

headers = {"Accept": "application/vnd.github+json", "User-Agent": "ResearchAgent"}

try:
    response = requests.get(
        url,
        params={"q": query, "sort": "stars", "order": "desc", "per_page": 25},
        headers=headers,
        timeout=30,
    )

    print("Status:", response.status_code)

    if response.status_code != 200:
        print(response.text)
        exit()

    raw_data = response.json()

    repositories = []

    for repo in raw_data.get("items", []):
        repositories.append(
            {
                "name": repo.get("name"),
                "full_name": repo.get("full_name"),
                "description": repo.get("description"),
                "owner": repo.get("owner", {}).get("login"),
                "language": repo.get("language"),
                "stars": repo.get("stargazers_count"),
                "forks": repo.get("forks_count"),
                "watchers": repo.get("watchers_count"),
                "open_issues": repo.get("open_issues_count"),
                "topics": repo.get("topics", []),
                "created_at": repo.get("created_at"),
                "updated_at": repo.get("updated_at"),
                "html_url": repo.get("html_url"),
            }
        )

    output = {
        "query": query,
        "source": "github",
        "collected_at": datetime.now().isoformat(),
        "total_results": len(repositories),
        "results": repositories,
    }

    Path("workspace").mkdir(exist_ok=True)

    with open("workspace/github.json", "w", encoding="utf-8") as file:
        json.dump(output, file, indent=4, ensure_ascii=False)

    print(f"\nCollected {len(repositories)} repositories")
    print("Saved to workspace/github.json")

except Exception as e:
    print("Error:", e)
