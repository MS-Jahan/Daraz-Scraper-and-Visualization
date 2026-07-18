# Daraz Product Scraping and Analysis

Scrape product listings from a Daraz Bangladesh category URL, store them in MySQL, then run Pandas analysis and Matplotlib visualizations into an HTML report.

![Project overview](docs/screenshots/hero.png)

## Overview

End-to-end pipeline: scrape → MySQL → clean/analyze → charts → `daraz_report.html`. Useful as a data-scraping + visualization portfolio piece. Prefer Docker for a one-command run.

## Links

- **Repo:** https://github.com/MS-Jahan/Daraz-Scraper-and-Visualization
- **Live demo:** none (local / Docker). Output artifact: `daraz_report.html` after a successful run
- **Sample data:** `products-sample.json`, `sample-output.json`

## Key Features

- Scrape category pages (name, image, price, discount, rating, reviews, location, …)
- Persist products in MySQL
- Pandas analysis (descriptive stats, price/discount/rating/location, correlations)
- Matplotlib charts (histograms, scatter, bar, box)
- HTML report with embedded visualizations

## Tech Stack

**Python 3.7+** (tested 3.12) · **Scraping:** DrissionPage · **Data:** Pandas, NumPy · **Viz:** Matplotlib · **DB:** MySQL (`mysql-connector-python`) · **Packaging:** Docker / Docker Compose

## Dependencies

Install from `requirements.txt`. Core packages:

- `DrissionPage`, `pandas`, `matplotlib`, `numpy`, `pillow`
- `mysql-connector-python`, `requests`, `lxml`, `httpx`

```bash
pip install -r requirements.txt
```

## Quick Run (Docker)

```bash
git clone https://github.com/MS-Jahan/Daraz-Scraper-and-Visualization.git
cd Daraz-Scraper-and-Visualization
docker-compose up --build
```

## How to Run Locally

```bash
git clone https://github.com/MS-Jahan/Daraz-Scraper-and-Visualization.git
cd Daraz-Scraper-and-Visualization
pip install -r requirements.txt
```

1. Create MySQL database/table `products` (see `database.py`).
2. Set DB credentials in `config.py`.
3. Set `USER_INPUTTED_URL` (and related vars) in `main.py` to a Daraz category URL.
4. Run:

```bash
python3 main.py
```

The script scrapes, stores, analyzes, plots, and writes `daraz_report.html`.

## Project Structure

| File | Role |
| :--- | :--- |
| `main.py` | Orchestrates scrape → analyze → report |
| `helpers.py` | Scraping helpers |
| `database.py` | MySQL access |
| `config.py` | DB credentials |
| `data_prep.py` / `data_analysis.py` / `data_visualization.py` | Pandas + Matplotlib |
| `report_generator.py` | HTML report |

## License

MIT
