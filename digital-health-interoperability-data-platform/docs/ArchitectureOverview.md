Architecture Overview
Data Source: Synthetic FHIR bundles (Patient, Encounter, Observation)

Raw Layer: Store raw JSON files

Staging Layer: Normalize FHIR → tabular format using Python

Core Layer: PostgreSQL schema with optimized tables

Orchestration: Airflow DAGs for ingestion, transformation, loading

Governance: DSGVO compliance, pseudonymization, data quality checks

ML Pipeline: Feature engineering + risk prediction model

LLM Pipeline: Optional summarization of clinical notes

Advanced: OMOP mapping, Docker, CI/CD, monitoring dashboard