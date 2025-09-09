
├─ README.md
├─ requirements.txt
├─ src/
│  ├─ main.py                # orchestrator / CLI
│  ├─ config.yaml            # experiment config
│  ├─ pipelines/
│  │  ├─ __init__.py
│  │  ├─ data_pipeline.py
│  │  ├─ trainer.py
│  │  ├─ analyzer.py
│  ├─ embeddings/
│  │  ├─ __init__.py
│  │  ├─ classical.py        # SBERT wrapper
│  │  └─ quantum.py          # PennyLane circuits
│  ├─ agents/                # later: scout, critic, analyzer agent wrappers
│  │  ├─ __init__.py
│  │  └─ scout.py
│  └─ utils/
│     ├─ logging_utils.py
│     └─ seed.py
└─ notebooks/
   └─ quick-experiment.ipynb

[quant-research-agent/]- our project initial name n purpose