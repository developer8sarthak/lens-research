from datetime import datetime
import requests

def collect(query: str) -> dict:
    url = "https://api.github.com/search/repositories"
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "ResearchAgent"}

    response = requests.get(
        url,
        params={"q": query, "sort": "stars", "order": "desc", "per_page": 25},
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()

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

    return {
        "query": query,
        "source": "github",
        "collected_at": datetime.now().isoformat(),
        "total_results": len(repositories),
        "results": repositories,
    }
