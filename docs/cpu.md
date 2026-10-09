# Optional CPU image

The `cpu` Docker build target is intended for CPU hosts such as the N100.
It avoids unused CUDA dependencies and GPU infrastructure. It does not change
the ingestion API, Docling configuration, or the default Compose build.

`constraints-cpu.txt` pins `torch==2.14.1+cpu` and
`torchvision==0.29.1+cpu`. The first install uses only the explicit PyTorch CPU
index, `https://download.pytorch.org/whl/cpu`, to obtain these wheels. The second
install uses the existing application requirements and normal pip index with
those same constraints, preventing replacement with CUDA-enabled packages.
No other dependency ranges have changed. This is not a full dependency lock:
other packages still resolve within the existing ranges. Missing or incompatible
CPU wheels must fail the build; do not silently substitute other versions.

## Build and validate in isolation

From the repository root, on a host with compatible Python 3.12 CPU wheels:

```bash
docker build --target cpu -t trusted-ingest:cpu .
docker run --rm --entrypoint python trusted-ingest:cpu -c 'import torch, torchvision; assert torch.__version__ == "2.14.1+cpu"; assert torchvision.__version__ == "0.29.1+cpu"; assert torch.version.cuda is None; assert not torch.cuda.is_available(); print(torch.__version__, torchvision.__version__, "CPU-only")'
docker run --rm --entrypoint pip trusted-ingest:cpu check
docker run --rm --name trusted-ingest-cpu-eval -p 127.0.0.1:8081:8080 trusted-ingest:cpu
```

In another terminal, check `http://127.0.0.1:8081/healthz` and submit a synthetic
document to `/v0/ingest`. The separate port and container name permit evaluation
without replacing the default service, which remains bound to `127.0.0.1:8080`.
No GPU device flags or runtime volume are needed. Docling may download model assets on first conversion; a health
check alone does not validate conversion or Markdown fidelity.

Keep the inherited single Uvicorn worker and send evaluation requests serially
on the N100. Conversion remains synchronous within the existing async handler;
this variant adds no workers, parallel request processing, or queues. This does
not force every internal library to use a single CPU thread.

## Default and rollback

The final Docker stage remains `default`, with the original unconstrained
`pip install -r requirements.txt`. Existing `docker compose up --build` therefore
retains the original dependency selection (including CUDA dependencies where
resolved). The CPU target is opt-in and does not modify `compose.yaml`.
Stop the foreground evaluation container with Ctrl-C. For a later deployment,
retain the prior image for exact rollback; rebuilding `--target default` restores
the original build recipe but its broad dependency ranges are not an exact lock.

## Reported isolated benchmark

Reference: `work_id=HERMES-20261008-475E1F`,
`correlation_id=TRUSTED-INGEST-D5-20261008` (2026-10-08).
These figures were supplied from a successful isolated evaluation, not a
production promotion or a benchmark rerun of this source change.

| Measurement | CPU image | Current CUDA image in that evaluation |
| --- | ---: | ---: |
| Image size (bytes) | 1,816,941,948 | 6,575,649,072 |
| 1-page fixture, reported warm time (seconds) | 3.299 | 3.960 |
| 10-page fixture, reported warm time (seconds) | 20.651 | 19.768 |

There were three warm runs per fixture per image. The supplied summary does
not identify the aggregation statistic or provide individual samples. Markdown
matched the expected fixture markers/content. These results support a smaller
CPU image with similar observed conversion times; they do not establish cold
start performance, concurrent throughput, or fidelity on other documents.
