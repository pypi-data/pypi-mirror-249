# BasketballCrawler

Welcome to the Python package designed for web crawling. This project aims to scrape data from the website "https://www.krepsinis.net" related to basketball articles. The data is extracted using web scraping techniques and organized into a Pandas DataFrame.

## Installation

### Using a Package Manager

You can install the crawler as a package using pip:

```bash
pip install m1_project_agne
```
Or using poetry:

```bash
poetry add m1_project_agne
```

## Cloning the Repository

You can also clone the repository and install the dependencies using poetry:

```bash
git clone https://github.com/agnesema/m1_project_agne
cd m1_project_agne
poetry install
```
## Usage

To use this project, you can import the `crawl` function from `main.py` and call it with the desired parameters. Here is an example:

```python
from m1_project_agne.main import crawl

result = crawl(source="krepsinis", return_format="csv", time_limit=10, search_word="rytas")
print(result)
```
## Structure

The project is structured as follows:

- **m1_project_agne/:** Main package directory.
  - **__init__.py:** Package initialization file.
  - **krepsinis.py:** Crawler for the Krepsinis website.
  - **main.py:** Main script for the crawler package.
- **tests/:** Test scripts for the package.
  - **__init__.py:** Initialization file for tests.
  - **test.py:** Test scripts

 ## Licence

 This project is licensed under the MIT license.
