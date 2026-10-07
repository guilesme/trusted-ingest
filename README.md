# Trusted Ingest

A local-first, verifiable ingestion layer for turning heterogeneous source material into structured, traceable outputs suitable for downstream human or AI workflows.

## V0 target

V0 implements one minimal end-to-end path:

```text
document upload → Trusted Ingest API → Docling → Markdown + provenance manifest
```

The API accepts a supported document, converts it with Docling, and returns structured Markdown plus a machine-readable manifest containing source and output hashes, file metadata, engine, format, and UTC processing time. Runtime inputs and outputs stay outside Git.

## Run locally

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --port 8080
```

Health check:

```bash
curl http://127.0.0.1:8080/healthz
```

Process a document:

```bash
curl -F 'file=@./document.pdf' http://127.0.0.1:8080/v0/ingest
```

## Run with Compose

```bash
# Keep the default loopback bind for local use.
docker compose up --build
```

The bind address is environment-specific and can be changed outside Git with `TRUSTED_INGEST_BIND`. Do not commit real LAN addresses or infrastructure details.

## Tests

```bash
pytest -q
```

The tests use synthetic fixtures and mock the Docling conversion boundary. A container smoke test should be run separately when Docker and the Docling image build are available.

## Scope boundaries

V0 deliberately does not include Redis, distributed queues, GPU routing, LLM enrichment, WhatsApp ingestion, or private data. Those are later milestones and must not block this path.

## Security

This repository is public. Never commit real documents, conversations, credentials, private network details, runtime outputs, or client data. See [AGENTS.md](AGENTS.md) and [SECURITY.md](SECURITY.md).
