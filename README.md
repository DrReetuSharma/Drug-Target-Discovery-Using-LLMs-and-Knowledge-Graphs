# Drug Target Discovery Using LLMs and Knowledge Graphs
## Overview
### Developed a platform that integrates Large Language Models (LLMs) with knowledge graphs to enhance the extraction, representation, and usage of scientific knowledge in drug discovery.

## Key Contributions

### LLM Integration: Implemented open-source LLMs for natural language querying of biomedical data.
### Knowledge Graph Development:  Built a modular knowledge graph using Neo4j to represent drug-target interactions and biomedical entities.
### Data Pipeline: Designed robust pipelines for data ingestion, preprocessing, and integration from diverse biomedical datasets.
### APIs and User Interface: Developed APIs and a user-friendly web interface to allow researchers to query the knowledge graph using natural language.
### Collaboration: Worked with multidisciplinary teams to refine methods and validate outputs.

## Technologies Used
Programming Languages: Python
Frameworks and Tools: Neo4j, BioCypher, Docker, LangChain, LLM frameworks (e.g., llama-cpp)
Version Control: Git, GitHub

## Impact
Enabled more informed decisions in target selection for drug discovery.
Improved data sharing and analysis capabilities, supporting therapeutic hypothesis generation.


Drug-Target-Discovery-LLM/
├── data/
│   ├── raw/
│   │   └── dataset_HTN.csv
│   └── processed/
│       └── processed_HTN.csv
├── scripts/
│   ├── ingest.py
│   ├── preprocess.py
│   ├── eda.py
│   ├── build_graph.py
│   ├── common_queries.cypher
│   └── integration_data.py
├── src/
│   ├── __init__.py
│   ├── data_ingestion.py
│   ├── data_preprocessing.py
│   ├── eda_functions.py
│   ├── graph_construction.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── endpoints.py
│   │   └── utils.py
│   └── integration/
│       ├── __init__.py
│       ├── external_data_integration.py
│       └── config.py
├── notebooks/
│   ├── eda.ipynb
│   ├── build_graph.ipynb
│   └── integration_demo.ipynb
├── config/
│   ├── neo4j_config.conf
│   ├── docker/
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
├── tests/
│   ├── test_data_ingestion.py
│   ├── test_data_preprocessing.py
│   ├── test_eda_functions.py
│   ├── test_graph_construction.py
│   ├── test_api_endpoints.py
│   └── test_integration.py
├── docs/
│   ├── api_documentation.md
│   ├── user_guide.md
│   └── project_overview.md
├── .gitignore
├── README.md
└── requirements.txt
