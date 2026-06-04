# lensdev

### A local AI-powered research agent designed for developers and students.

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![PyPI version](https://img.shields.io/badge/PyPI-0.1.1-orange.svg)](https://pypi.org/project/lensdev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**lensdev** is a powerful, lightweight Python library that acts as your personal research assistant. It automates the process of gathering information from across the web, academic journals, and developer platforms, providing you with a structured report in seconds.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Requirements](#requirements)
- [Installation Guide](#installation-guide)
- [Quick Start](#quick-start)
- [Command-Line Usage](#command-line-usage)
- [Supported Sources](#supported-sources)
- [Output Formats](#output-formats)
- [Troubleshooting](#troubleshooting)

---

## Overview

In the era of information overload, **lensdev** helps you cut through the noise. Whether you are a student starting a thesis or a developer exploring a new library, lensdev gathers high-quality data from multiple reliable sources simultaneously.

### Why lensdev?
- **Local First**: Your queries and results stay on your machine.
- **Fast and Efficient**: Parallel collection from multiple sources.
- **AI-Powered**: Smart ranking and categorization to ensure relevance.
- **Offline Capable**: Browse your generated reports anytime without an active connection.

---

## Key Features

- **Multi-Source Collection**: Gather data from Wikipedia, GitHub, arXiv, and more.
- **Automated Summarization**: Get the gist of your research without reading every link.
- **Intelligent Processing**: Built-in deduplication and relevance ranking.
- **Clean Reports**: Beautifully formatted reports in Markdown, HTML, and Plain Text.
- **Developer Friendly**: Simple CLI and easy-to-read source code.

---

## Requirements

- **Python**: 3.10 or higher
- **Operating System**: Windows, macOS, or Linux
- **Dependencies**: 
  - click (CLI interface)
  - requests (API interactions)
  - beautifulsoup4 (Web scraping)
  - rich (Terminal styling)

---

## Installation Guide

### Via pip (Recommended)
```bash
pip install lensdev
```

### From Source
If you want to contribute or use the latest development version:
```bash
git clone https://github.com/developer8sarthak/lens-research.git
cd lens-research
pip install -e .
```

---

## Quick Start

After installation, you can run your first research query immediately.

```bash
lens research "Quantum Computing basics"
```

### Understanding the Output
Once the research is complete, lensdev provides a unique Session ID and creates a structured workspace directory with an absolute path:

```text
Session ID: quantum_computing_20260604_120000
Path: C:\Users\Username\lens-research\workspace\quantum_computing_20260604_120000

Workspace ready: C:\Users\Username\lens-research\workspace\quantum_computing_20260604_120000
```

The workspace directory contains:
1. **Raw Data**: JSON files from each collector in the `raw/` subfolder.
2. **Reports**: Your processed findings in `.md`, `.html`, and `.txt` formats within the `reports/` subfolder.
3. **Logs**: Error logs and execution details in the `logs/` subfolder.

---

## Command-Line Usage

The primary entry point is the lens command.

### Research Subcommand
Search for any topic across all supported collectors.

```bash
# Using the -q flag
lens research -q "AI coding agents"

# Using positional argument
lens research "Open source LLMs frameworks"
```

| Flag | Shorthand | Description |
|------|-----------|-------------|
| --query | -q | The topic or keyword to research |
| --help | -h | Show help message and exit |

### Other Commands
```bash
# Check version
lens --version

# View help
lens --help
```

---

## Supported Sources

Lens currently aggregates data from:
- **Wikipedia**: General knowledge and summaries.
- **GitHub**: Repositories, code, and developer tools.
- **arXiv**: Academic pre-prints and research papers.
- **OpenAlex**: Global index of scholarly papers.
- **Crossref**: Metadata for millions of scholarly works.
- **Reddit**: Community discussions and real-world opinions.
- **Semantic Scholar**: AI-powered scientific literature search.

---

## Output Formats

Every research session generates a structured report in three formats:
- **Markdown (.md)**: Perfect for documentation and GitHub.
- **HTML (.html)**: Interactive and visually appealing for browsers.
- **Text (.txt)**: Simple and portable.

Reports include sections for Academic Papers, Repositories, and Web Results, each ranked by relevance.

---

## Troubleshooting

- **Empty Results**: Ensure you have an active internet connection as most collectors rely on web APIs.
- **Installation Errors**: Make sure you are using Python 3.10+. Check with `python --version`.
- **Command Not Found**: Ensure your pip scripts directory is in your system's PATH.

---

Built by [Sarthak](https://github.com/developer8sarthak)
