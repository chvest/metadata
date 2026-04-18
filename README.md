# NATO Metadata Standards Comparison Tool

A local web application for detecting, generating, and comparing metadata standards used across NATO, EU, ISO, and NIST environments. Runs entirely offline (after the first page load caches CDN assets).

## Supported standards

| Domain | Standards |
|--------|-----------|
| NATO   | ADatP-5636 Ed.A V1, ADatP-4774, ADatP-4778 |
| EU     | Dublin Core / ISO 15836, DCAT-AP 2.1.1, DCAT-AP-SE 2.2.0, INSPIRE |
| ISO    | ISO 19115-1:2014, ISO 23081-1:2017 |
| NIST   | SP 800-60 Vol.1, IR 8112 |

## Features

- **Detect standard** — paste or upload a JSON/XML metadata record; get a ranked list of matching standards with field-by-field confidence scores
- **Generate metadata** — produce realistic example records in JSON or XML for any standard
- **Compatibility matrix** — interactive heatmap showing field-level coverage across all standard pairs
- **Compare two standards** — full side-by-side analysis: compatibility scores, conflict cards (blocking / data loss / transform required), field mappings, round-trip fidelity, and value-level issues
- **Reports** — per-standard HTML reports with crosswalk tables, interoperability conflicts, and a field coverage chart; downloadable as PDF
- **Suites** — grouped views for related standard families (e.g. NATO Metadata Infrastructure)
- **Methodology** — documented approach, evidence basis, and related academic literature
- **Dark mode** — persistent preference stored in the browser

---

## Requirements

- **Python 3.10 or newer** (3.11 / 3.12 recommended)
- **Internet access** on first use — Bootstrap 5.3 and Plotly.js are loaded from CDN and then browser-cached. See [Offline use](#offline-use) below if needed.

### Python packages

| Package | Version | Purpose |
|---------|---------|---------|
| `flask` | ≥ 3.0 | Web framework |
| `faker` | ≥ 25.0 | Realistic example metadata values |
| `plotly` | ≥ 5.20 | Field coverage chart in reports |
| `reportlab` | ≥ 4.1 | PDF report generation |
| `lxml` | ≥ 5.2 | XML parsing in the Detect page |

All versions are pinned in `requirements.txt`.

---

## Setup and running

### Windows

```bat
REM 1. Open a Command Prompt or PowerShell in the metadata-tool\ folder

REM 2. Create a virtual environment
python -m venv venv

REM 3. Activate it
venv\Scripts\activate

REM 4. Install dependencies
pip install -r requirements.txt

REM 5. Start the app
python app.py
```

### macOS / Linux

```bash
# 1. Open a terminal in the metadata-tool/ directory

# 2. Create a virtual environment
python3 -m venv venv

# 3. Activate it
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Start the app
python app.py
```

### Access the app

Open **http://127.0.0.1:5000** in your browser.

Press `Ctrl+C` in the terminal to stop the server.

---

## Subsequent runs

Once the virtual environment and packages are installed, only steps 3 and 5 are needed each time:

```bash
# Windows
venv\Scripts\activate
python app.py

# macOS / Linux
source venv/bin/activate
python app.py
```

---

## Making the app available on a local network

By default the server only listens on localhost. To reach it from other devices on the same network, edit the last line of `app.py`:

```python
# Change this:
app.run(host="127.0.0.1", port=5000, debug=False)

# To this:
app.run(host="0.0.0.0", port=5000, debug=False)
```

Then access the app at `http://<your-machine-ip>:5000` from any device on the network.

---

## Offline use

The app loads two libraries from CDN at runtime:

| Library | URL in `templates/base.html` |
|---------|------------------------------|
| Bootstrap 5.3 CSS | `https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css` |
| Bootstrap 5.3 JS  | `https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js` |

Plotly.js is loaded inline per report page from `https://cdn.plot.ly/`.

To run fully offline:

1. Download each file into `static/`
2. Update the `<link>` and `<script>` tags in `templates/base.html` to use `{{ url_for('static', filename='bootstrap.min.css') }}` etc.
3. For Plotly, set `include_plotlyjs='directory'` (or `'inline'`) in `engine/reporter.py` where the chart is built.

---

## Project structure

```
metadata-tool/
├── app.py                  # Flask routes and application entry point
├── requirements.txt        # Python package dependencies
│
├── engine/
│   ├── detector.py         # Detects which standard a metadata record conforms to
│   ├── generator.py        # Generates realistic example metadata records
│   └── reporter.py         # Builds HTML/PDF reports and Plotly charts
│
├── standards/
│   ├── base.py             # MetadataStandard base class and field definitions
│   ├── registry.py         # Central registry — instantiates all 11 standards
│   ├── crosswalk.py        # Field mappings, conflict entries, and value-level issues
│   ├── suites.py           # Standard suite groupings
│   ├── nato/               # ADatP-5636, ADatP-4774, ADatP-4778
│   ├── eu/                 # Dublin Core, DCAT-AP, DCAT-AP-SE, INSPIRE
│   ├── iso/                # ISO 19115-1, ISO 23081-1
│   └── nist/               # NIST SP 800-60, NIST IR 8112
│
├── templates/              # Jinja2 HTML templates
│   ├── base.html           # Navbar, footer, dark-mode toggle
│   ├── index.html          # Landing page
│   ├── detect.html         # Standard detection UI
│   ├── generate.html       # Metadata generation UI
│   ├── compare.html        # Compatibility matrix
│   ├── pairwise.html       # Two-standard deep comparison
│   ├── report.html         # Per-standard report
│   ├── suite.html          # Suite view
│   ├── tutorial.html       # Usage guide
│   └── methodology.html    # Methodology and literature
│
└── static/
    └── style.css           # Custom CSS including full dark mode overrides
```

---

## Troubleshooting

**Port 5000 already in use**
```bash
# Run on a different port
python app.py --port 8080   # or edit the port in app.py directly
```

**`ModuleNotFoundError`**
Make sure the virtual environment is activated before running (`venv\Scripts\activate` / `source venv/bin/activate`) and that `pip install -r requirements.txt` completed without errors.

**`lxml` fails to install on Windows**
Try installing the pre-built wheel:
```bat
pip install lxml --only-binary :all:
```

**`reportlab` fails to install**
Ensure you have a C compiler available, or install via a pre-built wheel:
```bat
pip install reportlab --only-binary :all:
```

**Blank / unstyled page**
The browser is blocking CDN requests. See [Offline use](#offline-use) above.
