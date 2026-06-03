import time
from lens.collectors import arxiv, semantic_scholar, reddit

def test_collector(name, collector_func, query="AI"):
    print(f"Testing {name}...")
    try:
        result = collector_func.collect(query)
        print(f"  {name} success! Results: {len(result.get('results', []))}")
    except Exception as e:
        print(f"  {name} failed: {e}")
    time.sleep(2) # Respect rate limits

if __name__ == "__main__":
    test_collector("ArXiv", arxiv)
    test_collector("Semantic Scholar", semantic_scholar)
    test_collector("Reddit", reddit)
