# Autonomous Financial Research Analyst Agent
An agentic AI system that autonomously researches and ranks investment opportunities 
by orchestrating multiple data sources, real-time news, sentiment analysis, and 
private document retrieval — delivering investment-grade reports in minutes.

## What It Does
This agent proactively gathers financial intelligence without being told what to look 
for. Given a company ticker or a list of companies, it autonomously:

- Fetches real-time stock prices and 3-year historical performance via Yahoo Finance
- Searches recent financial news and analyzes market sentiment using OpenAI
- Queries a private RAG-powered database of AI initiative analyst reports
- Synthesizes all data into a structured Buy / Hold / Sell recommendation with 
  confidence levels, source citations, and risk assessments

The agent handles tool failures gracefully — if one data source fails, it pivots to 
alternatives and flags the gap in its report rather than stopping.

## Tech Stack
| Tool | Purpose |
|---|---|
| LangGraph | Agent workflow — nodes, edges, state, routing |
| LangChain | Tool registration, message handling, LLM integration |
| OpenAI GPT-4o mini | LLM reasoning and sentiment analysis |
| Tavily Search API | Real-time financial news retrieval |
| yfinance | Yahoo Finance stock price and history data |
| ChromaDB | Vector database for semantic document search |
| OpenAI Embeddings | Converting documents to searchable vectors |
| PyPDF | Loading private analyst report PDFs into RAG pipeline |

## What I Learned
**Agentic AI Architecture** — The difference between a passive LLM and an autonomous 
agent comes down to goal-oriented prompting, tool access, and a loop that lets the 
agent keep working until it decides it has enough information. LangGraph's 
state-based graph made this loop explicit and controllable.

**RAG Pipeline** — Built a full retrieval-augmented generation pipeline from scratch: 
document loading → chunking → embedding → vector storage → semantic retrieval → 
grounded LLM response. This enables the agent to answer questions from private 
documents it was never trained on, with source citations.

**Tool Design Patterns** — Learned that LangChain's @tool decorator actively reads 
type hints and docstrings to enable autonomous tool selection. Writing clear tool 
interfaces directly shapes how reliably the agent uses them.

**Prompt Engineering for Agents** — Agent charters are more than system prompts. 
Explicit behavioral constraints (always check 3-year history, never stop on a single 
tool failure, always cite sources) measurably improve output quality and consistency.

**Error Resilience** — Designed each tool to return structured error dictionaries 
rather than raise exceptions, keeping the agent running and producing partial reports 
even when individual data sources fail.
