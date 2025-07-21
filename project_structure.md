
```
regscout/
├── main.py                      # Entry point (CLI or API server)
├── config/
│   ├── settings.yaml            # API keys, paths, model choices
│   ├── agents.yaml              # Agent roles, goals (if CrewAI)
├── agents/
│   └── ordinance_agent.py       # Main RegScout AI agent logic (class-based)
├── pipeline/
│   ├── chunker.py               # Chunking + metadata injection
│   ├── summarizer.py            # Summarization engine (OpenAI or local)
│   ├── embedder.py              # Embedding wrapper (OpenAI or Hugging Face)
│   ├── retriever.py             # Qdrant query + reranker
├── tools/
│   ├── html_parser.py           # Municode-specific parsing
│   ├── table_utils.py           # Table to sentence or summarizer
├── data/
│   └── raw/                     # Raw scraped HTML/text
│   └── chunks/                  # Prepared embedding chunks
├── ui/
│   └── cli.py                   # Optional CLI interface
│   └── web.py                   # Optional FastAPI app
└── utils/
    └── logger.py                # Logging setup

```