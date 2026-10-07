from __future__ import annotations

import hashlib
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI(title="Trusted Ingest", version="0.1.0")

_ALLOWED_SUFFIXES = {".pdf", ".docx", ".pptx", ".xlsx", ".html", ".md", ".txt"}


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _convert_to_markdown(source: Path) -> str:
    """Convert one local document with Docling and return structured Markdown."""
    from docling.document_converter import DocumentConverter

    result = DocumentConverter().convert(str(source))
    return result.document.export_to_markdown()


def _build_manifest(filename: str, content_type: str | None, source: bytes, markdown: str) -> dict[str, Any]:
    return {
        "manifest_version": "0.1",
        "status": "success",
        "source": {
            "filename": filename,
            "content_type": content_type or "application/octet-stream",
            "size_bytes": len(source),
            "sha256": _sha256(source),
        },
        "processing": {
            "engine": "docling",
            "output_format": "markdown",
            "markdown_sha256": _sha256(markdown.encode("utf-8")),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
    }


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok", "service": "trusted-ingest"}


@app.post("/v0/ingest")
async def ingest(file: UploadFile = File(...)) -> JSONResponse:
    filename = Path(file.filename or "upload").name
    suffix = Path(filename).suffix.lower()
    if suffix not in _ALLOWED_SUFFIXES:
        raise HTTPException(status_code=415, detail=f"unsupported file type: {suffix or '[none]'}")

    source = await file.read()
    if not source:
        raise HTTPException(status_code=422, detail="uploaded document is empty")

    with tempfile.TemporaryDirectory(prefix="trusted-ingest-") as workdir:
        source_path = Path(workdir) / filename
        source_path.write_bytes(source)
        try:
            markdown = _convert_to_markdown(source_path)
        except Exception as exc:  # noqa: BLE001 - API boundary must return a clear failure.
            raise HTTPException(status_code=422, detail=f"Docling conversion failed: {exc}") from exc

    manifest = _build_manifest(filename, file.content_type, source, markdown)
    return JSONResponse({"markdown": markdown, "manifest": manifest})
