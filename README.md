# TLGG Search App

A Flask app that searches `tlgg.json` (title, context, section titles, and details).

Local app URL: `http://127.0.0.1:8501`

## Files

- `app.py` - Flask backend and search logic
- `templates/index.html` - web UI
- `data/tlgg.json` - default dataset
- `requirements.txt` - dependencies
- `Procfile` - production start command (`gunicorn app:app`)
- `run_local.sh` - one-command local startup

## Run locally (recommended)

```bash
cd /Users/pritika_timsina/Desktop/TLGG
./run_local.sh
```

Open: `http://127.0.0.1:8501`

## Manual local run

```bash
cd /Users/pritika_timsina/Desktop/TLGG
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## If app does not open

1. Verify server is running and shows `Running on http://127.0.0.1:8501` in terminal.
2. Check if port is busy:

```bash
lsof -iTCP:8501 -sTCP:LISTEN -n -P
```

3. If busy, run on another port:

```bash
PORT=8502 ./run_local.sh
```

4. Test endpoint directly:

```bash
curl "http://127.0.0.1:8501/api/search?q=ecosystem"
```

## Deploy (Render / Railway / Heroku-style)

1. Push this folder to GitHub.
2. Create a new Python web service from the repo.
3. Build command:

```bash
pip install -r requirements.txt
```

4. Start command:

```bash
gunicorn app:app
```

5. Optional env var if data file is elsewhere:

```bash
TLGG_DATA_PATH=/opt/render/project/src/data/tlgg.json
```
