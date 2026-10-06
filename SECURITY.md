# Security and Data-Handling Policy

Trusted Ingest is developed in a public repository. Source control must contain code and synthetic test material only.

## Public-repository rule
Assume anything committed can be permanently copied even if later deleted. Secrets or private data accidentally committed must be treated as exposed and handled outside Git; deleting a later commit is not sufficient.

## Allowed
- source code and public documentation;
- synthetic/anonymized fixtures that cannot identify real people or environments;
- configuration templates containing only safe placeholder values;
- public upstream project references and dependency metadata.

## Prohibited
- secrets and credentials;
- private infrastructure addressing/topology;
- client/condominium source documents;
- WhatsApp exports or personal data;
- runtime inputs/outputs, derived private datasets, logs or caches.

## Development checks
Before push/PR:
1. inspect the complete diff;
2. confirm fixtures are synthetic;
3. confirm configuration contains placeholders only;
4. run automated secret scanning when available.

CI guardrails supplement review; they do not replace it.
