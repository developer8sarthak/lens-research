from collectors.wiki import collect as wiki_collect
from collectors.github import collect as github_collect
from collectors.arxiv import collect as arxiv_collect
from collectors.openalex import collect as openalex_collect
from collectors.crossref import collect as crossref_collect
from collectors.reddit import collect as reddit_collect
from collectors.semantic_scholar import collect as ssc_collect

COLLECTORS = {
    "wikipedia": wiki_collect,
    "github": github_collect,
    "arxiv": arxiv_collect,
    "openalex": openalex_collect,
    "crossref": crossref_collect,
    "reddit": reddit_collect,
    "semantic_scholar": ssc_collect
}
