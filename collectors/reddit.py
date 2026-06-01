from datetime import datetime
import requests

def collect(query: str) -> dict:
    url = "https://www.reddit.com/search.json"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(
        url,
        params={"q": query, "limit": 25, "sort": "relevance"},
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()

    raw_data = response.json()
    cleaned_posts = []
    posts = raw_data.get("data", {}).get("children", [])

    for item in posts:
        post = item.get("data", {})
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

    return {
        "query": query,
        "source": "reddit",
        "collected_at": datetime.now().isoformat(),
        "total_posts": len(cleaned_posts),
        "results": cleaned_posts,
    }
