# Trusted Ingest

A local-first, verifiable ingestion layer for turning heterogeneous source material into structured, traceable outputs suitable for downstream human or AI workflows.

## V0 target

The first milestone intentionally stays small: submit a document, process it with Docling, and receive Markdown plus a machine-readable provenance manifest. Deployment is containerized and environment-specific configuration remains outside this public repository.

Future adapters may cover additional sources such as exported conversations, but V0 prioritizes a reliable document path before adding queues, GPU routing or LLM enrichment.

## Security

This repository is public. Do not commit real documents, conversations, credentials, private network details or runtime data. See [AGENTS.md](AGENTS.md) and [SECURITY.md](SECURITY.md).
