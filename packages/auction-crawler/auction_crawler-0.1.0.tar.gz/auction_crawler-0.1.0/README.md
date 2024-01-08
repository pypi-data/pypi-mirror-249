# Auction crawler project

## Description

Auction crawler project is a Python package to crawl a website with forest auctions. This project utilizes Python 
3.12, along with requests, selenium libraries. It focuses on data extraction from certain website.

## Installation

### Using a package manager
You can install forest auction crawler as a package: Using pip:

```sh
pip install auction_crawler
```

Or using 'poetry':

```sh
poetry add auction_crawler
```

### Cloning the repository
Also, you can clone this repository and install dependencies using 'poetry':

```sh
git clone https://github.com/vytenisdam/auction_crawler
cd auction_crawler
poetry install
```

## Usage

### As a module

```python
from auction_crawler.main import crawl_site

print(crawl_site('csv', scroll_time=40))
```

## Structure

The project is structured as follows:

- `auction_crawler/`: Main package directory.
  - `__init__.py`: Package initialization file.
  - `main.py`: Main script for the auction crawler package.
  - `csv_write.py`: Script for writing crawled data to csv file.
  - `selenium_crawl.py`: Separate functions that make the crawler work.
- `tests/`: Tests directory.
  - `__init__.py`: Initialization file for tests.
  - `tests_main.py`: Test scripts for the package