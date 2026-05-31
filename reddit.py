import json
from datetime import datetime
from pathlib import Path

import requests

query = input("Enter your query: ")

url = "https://www.reddit.com/search.json"

headers = {"User-Agent": "Mozilla/5.0"}

try:
    response = requests.get(
        url,
        params={"q": query, "limit": 25, "sort": "relevance"},
        headers=headers,
        timeout=30,
    )

    print("Status:", response.status_code)

    if response.status_code != 200:
        print(response.text[:1000])
        exit()

    raw_data = response.json()

    cleaned_posts = []

    posts = raw_data["data"]["children"]

    for item in posts:
        post = item["data"]

        cleaned_posts.append(
            {
                "id": post.get("id"),
                "title": post.get("title"),
                "subreddit": post.get("subreddit"),
                "author": post.get("author"),
                "score": post.get("score"),
                "upvote_ratio": post.get("upvote_ratio"),
                "comments": post.get("num_comments"),
                "created_utc": post.get("created_utc"),
                "permalink": "https://reddit.com" + post.get("permalink", ""),
                "url": post.get("url"),
                "domain": post.get("domain"),
                "selftext": post.get("selftext", ""),
                "nsfw": post.get("over_18"),
                "is_video": post.get("is_video"),
            }
        )

    output = {
        "query": query,
        "source": "reddit",
        "collected_at": datetime.now().isoformat(),
        "total_posts": len(cleaned_posts),
        "results": cleaned_posts,
    }

    Path("workspace").mkdir(exist_ok=True)

    with open("workspace/reddit.json", "w", encoding="utf-8") as file:
        json.dump(output, file, indent=4, ensure_ascii=False)

    print(f"\nCollected {len(cleaned_posts)} posts")
    print("Saved to workspace/reddit.json")

except Exception as e:
    print("Error:", e)
