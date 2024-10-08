# Kia Motor Dealership Web Scraper

This Python script automates the process of scraping Kia motor dealership data from the [Kia India website](https://www.kia.com/in/buy/find-a-dealer.html) using Selenium. It collects details like dealer name, type, address, contact info (mobile, email, domain), and map location, then saves it into a CSV file.

## Features

- Scrapes dealership information from all states and cities in India.
- Handles errors like stale elements and intercepted clicks.
- Implements scrolling for large dropdowns and retries for failed actions.
- Logs actions and results to `kia_scraper.log`.
- Saves dealership data into `kia_moter_dealers.csv`.

## Prerequisites

- Python 3.x
- ChromeDriver installed
- Google Chrome installed

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/kia-dealership-scraper.git
   cd kia-dealership-scraper