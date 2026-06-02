# Lens Research

An open-source research engine for the curious minds.

Lens Research is my attempt to build a tool that helps me (and hopefully others) gather, organize, and make sense of information from the web. Whether you're diving into academic papers, tracking GitHub repositories, or exploring global events, this project is designed to automate the boring stuff so you can focus on what matters: discovering insights.

---

## Why This Project?

I’ve always been fascinated by how much knowledge is out there—scattered across Wikipedia, arXiv, GitHub, and more—but manually collecting and organizing it is tedious. So, I built Lens Research to:

- Fetch data from multiple sources in one place.
- Save time by automating repetitive research tasks.
- Stay modular so anyone can add new sources or tweak existing ones.

This isn’t just a tool for me; it’s an open invitation for others to contribute, improve, and build upon it.

---

## What Can It Do Right Now?

Lens Research currently supports:

- Wikipedia: Extract articles, references, and metadata.
- GitHub: Fetch repositories, issues, and user activity.
- arXiv: Download and parse academic papers.
- OpenAlex & Crossref: Access scholarly works and citations.
- GDELT: Monitor global events and trends.

It’s 100% Python, easy to extend, and built to handle both small and large-scale research tasks.

---

## How to Use It

### 1. Get Started

Clone the repo and install the dependencies:


git clone https://github.com/developer8sarthak/lens-research.git
cd lens-research
pip install -r requirements.txt
2. Configure (If Needed)

Some sources (like GitHub) require API keys.
Create a .env file in the project root:

- GITHUB_TOKEN=your_token_here
- CROSSREF_EMAIL=your_email@example.com

3. Run It : 
python main.py

This will fetch data from all enabled sources and save it in a structured format.

## Adding New Sources

Want to add a new data source? It’s simple:

Create a new file in `collectors/` (e.g., `twitter.py`), follow the existing structure, and register it in `core/config.py`.

### Example:

```python
from core.base_collector import BaseCollector

class TwitterCollector(BaseCollector):
    def fetch(self):
        pass
```
MIT License

Connect With Me

GitHub: developer8sarthak

Email: sarthak19developer@gmail.com
