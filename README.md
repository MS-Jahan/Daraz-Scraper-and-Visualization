# Daraz Product Scraping and Analysis

This project scrapes product data given a specific category url from the Daraz e-commerce website (specifically Daraz Bangladesh) and performs analysis and visualization on the collected data. It uses Python libraries like `DrissionPage`, `Pandas`, and `Matplotlib` for web scraping, data manipulation, and visualization, respectively. The scraped data is stored in a MySQL database.

## Features

*   Scrapes product information from Daraz from a specific category url (name, image, price, discount, rating, reviews, location, etc.).
*   Stores the scraped data in a MySQL database.
*   Performs data analysis using Pandas (descriptive statistics, price analysis, discount analysis, rating analysis, location analysis, correlation analysis).
*   Generates visualizations using Matplotlib (histograms, scatter plots, bar charts, box plots).
*   Creates an HTML report with the analysis results and embedded visualizations.

## Requirements

*   Python 3.7+ (tested with 3.12)
*   DrissionPage
*   Pandas
*   Matplotlib
*   MySQL Connector/Python

## Quick Run using Docker
```bash
git clone https://github.com/MS-Jahan/Daraz-Scraper-and-Visualization.git && cd Daraz-Scraper-and-Visualization && docker-compose up --build
``` 

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/MS-Jahan/Daraz-Scraper-and-Visualization.git
    ```
2.  Change directory:
    ```bash
    cd Daraz-Scraper-and-Visualization
    ```
2.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
3.  Set up the MySQL database:
    *   Create a new database named "products".
    *   Create a table named "products" with the appropriate columns (see `database.py`).
    *   Update the database credentials in `config.py`.

## Usage

1.  Update the `USER_INPUTTED_URL` and check other variables in `main.py` with the Daraz category URL you want to scrape.
2.  Change database credentials in `config.py`.
3.  Run `main.py`:
    ```bash
    python3 main.py
    ```
3.  The script will scrape the data, store it in the database, perform analysis, generate visualizations, and create an HTML report named `daraz_report.html`.

## Project Structure

*   `main.py`: Main script that orchestrates the scraping, analysis, and report generation.
*   `helpers.py`: Helper functions for web scraping.
*   `database.py`: Class for interacting with the MySQL database.
*   `config.py`: Stores database credentials.
*   `data_prep.py`: Functions for data extraction and cleaning using Pandas.
*   `data_analysis.py`: Functions for performing data analysis using Pandas.
*   `data_visualization.py`: Functions for creating visualizations using Matplotlib.
*   `report_generator.py`: Function for generating the HTML report.

## Contributing

Contributions are welcome! Please feel free to open issues or pull requests.

## License

This project is licensed under the MIT License.