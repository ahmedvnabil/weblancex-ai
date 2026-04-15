# WeblanceX Starter Template

Flask + Tailwind CSS + HTMX + Alpine.js. No build tools, no JS frameworks, CDN-first.

## Quick Start

```bash
cp .env.example .env
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000`.

## Stack

- **Python 3.12 + Flask** — backend, Jinja2 templates
- **Tailwind CSS** — utility styling via CDN
- **HTMX** — server-driven UI updates (HTML fragments)
- **Alpine.js** — client-side interactivity (toggles, modals)

## Production

```bash
docker build -t weblancex-app .
docker run -p 5000:5000 -e SECRET_KEY=your-secret weblancex-app
```

Or deploy to Railway with the included `Procfile`.

## Structure

```
app.py              # Routes and app config
templates/
  base.html         # Layout with CDN imports
  index.html        # Landing page
  partials/         # HTMX fragments
requirements.txt    # Python deps
Dockerfile          # Production container
Procfile            # Railway/Heroku process file
```
