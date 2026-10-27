# DevMind AI API

FastAPI MVP that statically inspects uploaded Python files. It does not execute uploaded code.

## Local run

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

- `GET /health`
- `POST /analyze` with multipart field `file` (.py only; max 200 KB)

For cloud deployment, set `ALLOWED_ORIGINS` to a comma-separated list of exact frontend origins, e.g. `https://your-site.netlify.app`.
