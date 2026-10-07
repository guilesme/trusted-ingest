import app.main as main
from fastapi.testclient import TestClient


client = TestClient(main.app)


def test_healthz():
    response = client.get('/healthz')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok', 'service': 'trusted-ingest'}


def test_ingest_returns_markdown_and_manifest(monkeypatch):
    def fake_convert(path):
        assert path.name == 'synthetic.txt'
        assert path.read_text() == 'Synthetic document for tests.'
        return '# Synthetic document\n\nThis is safe fixture content.\n'

    monkeypatch.setattr(main, '_convert_to_markdown', fake_convert)
    response = client.post(
        '/v0/ingest',
        files={'file': ('synthetic.txt', b'Synthetic document for tests.', 'text/plain')},
    )

    assert response.status_code == 200
    body = response.json()
    assert body['markdown'].startswith('# Synthetic document')
    assert body['manifest']['status'] == 'success'
    assert body['manifest']['processing']['engine'] == 'docling'
    assert body['manifest']['source']['filename'] == 'synthetic.txt'
    assert len(body['manifest']['source']['sha256']) == 64
    assert len(body['manifest']['processing']['markdown_sha256']) == 64


def test_ingest_rejects_unsupported_type():
    response = client.post('/v0/ingest', files={'file': ('payload.exe', b'nope', 'application/octet-stream')})
    assert response.status_code == 415


def test_ingest_reports_conversion_failure(monkeypatch):
    monkeypatch.setattr(main, '_convert_to_markdown', lambda path: (_ for _ in ()).throw(RuntimeError('synthetic failure')))
    response = client.post('/v0/ingest', files={'file': ('synthetic.txt', b'content', 'text/plain')})
    assert response.status_code == 422
    assert 'Docling conversion failed' in response.json()['detail']
