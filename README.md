# Amazon Product Scraper

This Python script scrapes product information from Amazon's `Electronics` section (example link provided) and saves it to a CSV file. The script uses Selenium to control a web browser, retrieve product details, and handle anti-bot mechanisms such as random delays, user-agent rotation, and headless browsing.

## Features

- Rotates user agents to avoid detection.
- Randomly pauses and mimics user behavior to reduce chances of being blocked.
- Extracts product details including:
  - Product Name
  - Price
  - Rating
  - Seller Name
  - Stock Status
- Saves extracted data into `products_data.csv`.

## Prerequisites

- Python 3.6+
- Google Chrome browser
