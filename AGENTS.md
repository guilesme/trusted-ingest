# AGENTS.md

## Repository visibility
This repository is PUBLIC. Treat every tracked file, commit, issue, pull request, log excerpt, fixture, screenshot, and example as internet-public.

These rules apply to every contributor and automation, including ChatGPT, Hermes agents (Max, Atlas, Dexter, Severino and others), coding agents, CI jobs, and future integrations.

## Non-negotiable safety rules
Never commit or publish:
- credentials, API keys, tokens, cookies, passwords, private keys, certificates, or populated .env files;
- real private-network IPs, host addressing, VLAN/subnet details, internal DNS names, or sensitive homelab topology;
- real Condomínio Astro, Nel, client, resident, employee, or supplier documents/data unless explicitly sanitized for public release;
- real WhatsApp exports, conversations, phone numbers, names, attachments, or derived datasets containing personal/confidential data;
- production uploads, parsed outputs, caches, logs, database dumps, embeddings/vector stores, or temporary processing artifacts containing source data.

Use synthetic/anonymized fixtures only. Examples must use placeholders such as 192.0.2.0/24, example.com, dummy tokens, and invented people/organizations.

## Configuration boundary
Repository code must be environment-agnostic. Deployment-specific addressing and secrets belong outside this public repository. Commit only templates such as .env.example with safe fake values.

## Data handling
Raw input and generated output are runtime data, not source code. Keep them outside Git. Tests must not require private datasets. If a real document is needed for local validation, it must remain untracked.

## Architecture direction
Trusted Ingest is a reusable, verifiable ingestion layer. V0 should stay small:
1. accept a document;
2. process it with Docling;
3. return Markdown plus a machine-readable manifest;
4. preserve provenance/verifiability;
5. run locally via containers/Compose.

Do not add Redis, distributed queues, GPU routing, LLM enrichment, or other infrastructure to V0 unless evidence from testing requires it.

## Agent workflow
Before any commit, inspect the diff for sensitive information. If uncertain whether content is safe for a public repository, do not commit it; escalate to the project owner.

Application work is primarily coordinated by Max. Sirius/container/network deployment work is primarily coordinated by Atlas. Dexter and all other agents follow the same repository rules. Role assignment never overrides these safety requirements.

Prefer PRs and reviewable changes over direct changes to main.
