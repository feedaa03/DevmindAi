# DevMind AI — Local development and public experimental deployment

The project now consists of a static interface (Netlify) and an API interface with FastAPI (Render). The current Python analyzer is real but preliminary and based on static rules; there are no real LLM or RAG models or actual Pull Request creation yet.

## Local running on macOS

Open Terminal in the project folder. Run the interface in the first window:

```bash

python3 -m http.server 5500 --directory frontend

```

In a second window:

```bash

cd backend

python3 -m venv .venv

source .venv/bin/activate

python -m pip install -r requirements.txt

uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

```

Open http://127.0.0.1:5500. The local interface configuration is located in `frontend/config.js`.

## General publication

### 1. Publish the Backend on Render

1. Push the project folder to the GitHub repository.

2. In Render, choose New > Blueprint, then choose the repository that contains `render.yaml`.

3. Add the value of `ALLOWED_ORIGINS` after creating a Netlify site, such as `https://your-site-name.netlify.app` (without a forward slash at the end).

4. After publishing, test `https://YOUR-API.onrender.com/health`.

### 2. Connect the interface to the cloud API endpoint

Modify `frontend/config.js` to contain the real API link:

```js

window.DEVMIND_CONFIG = {

API_BASE_URL: 'https://YOUR-API.onrender.com'

};

```

Do not put any secret keys in this file; it is sent to every visitor.

### 3. Publish the interface on Netlify

Import the GitHub repository in Netlify. Setting up `netlify.toml` specifies `frontend` as the publishing directory. After any modifications and pushing it to GitHub, Netlify will automatically rebuild the site if the repository linking is enabled.

## What is actually working now

- `GET /health` to check the service.

- `POST /analyze` to receive a `.py` file with a maximum of 200 KB and analyze basic rules such as bare `eval` and `except:`, long functions and final newlines.

- The interface calls the API and displays the actual analysis results.

- Set up a separate API address in `frontend/config.js`.

## Still experimental or incomplete

- Control panel numbers and some repair/test cards in the design are illustrative data, not live statistics. Do not rely on them as actual measurements.
