# Lens

Lens is a local AI research agent that takes a query, performs structured research, and stores results in a persistent workspace.

## Installation

```bash
pip install lensdev
```

## Usage

Run a research task:

```bash
lens research -q "how do vector databases work"
```

## Workspace System

Every run generates a workspace:

`workspace/<session_id>/`

Example:

`workspace/session_20260604_143210/`

### Structure:

- `report.md` (Main research report)
- `sources.json` (Combined raw data from all collectors)
- `meta.json` (Session metadata: query, timestamp, version)
- `raw/` (Individual collector results)

## CLI Commands

### Run research:

```bash
lens research -q "query"
```

**Output:**
```text
Lens.
────────────────────────────────────────────────────────────────────────────────

Research
your query

Collecting Sources
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% (7/7)

Research complete.
Workspace saved at: workspace/session_20260604_143210/
```

### List sessions:

```bash
lens list
```

**Output:**
```text
 Session ID                        
 session_20260604_143210
 session_20260604_104908
```

### Resume session:

```bash
lens resume <session_id>
```

**Output:**
```text
Resuming session: session_20260604_143210
Query: how do vector databases work
Path: /path/to/workspace/session_20260604_143210
Re-generating reports...
Reports re-generated.
```

## Output Behavior

After completion:

```
Research complete.
Workspace saved at: workspace/<session_id>/
```

## Philosophy

Lens turns research into structured, persistent workspaces instead of temporary terminal output.

---
**GitHub:** [https://github.com/developer8sarthak/lens-research](https://github.com/developer8sarthak/lens-research)  
**PyPI:** [https://pypi.org/project/lensdev/](https://pypi.org/project/lensdev/)  
**Documentation:** [https://lensdev.pages.dev/](https://lensdev.pages.dev/)
