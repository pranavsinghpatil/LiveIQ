# [RESEARCH] Architecture

## Core Agents
- **Scout:** generates candidate research questions / hypotheses.
- **Critic:** evaluates, filters, and challenges Scout’s outputs.
- **Analyzer:** runs experiments, logs evidence.

## Pipelines
- **Data Pipeline:** ingestion, preprocessing, embedding generation.
- **Training Pipeline:** experiment orchestration, model training.
- **Analyzer Pipeline:** evaluation + results storage.

## Flow
Scout → Critic → Analyzer → Feedback loop (stored in logs/db)
