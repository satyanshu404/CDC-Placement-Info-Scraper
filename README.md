<div align="center">

# CDC Placement Scraper

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)
![Selenium 4.32.0](https://img.shields.io/badge/selenium-4.32.0-red)
![BeautifulSoup 0.0.2](https://img.shields.io/badge/beautifulsoup-0.0.2-green)

</div>

---

## Overview

This project provides a simple web scraper for extracting placement information from the CDC website. It uses `BeautifulSoup` and `requests` for parsing web content, and `selenium` for dynamic page interaction.

**Disclaimer:**  
This project is intended for educational purposes and to get the idea about how the placement season works.
It is not intended for any malicious or unethical use. The scraper is designed to be used responsibly and ethically, respecting the terms of service of the target website. 

Always ensure you have permission to scrape a website before doing so, and be mindful of the load you place on their servers. This project is provided "as-is" without any warranty or guarantee of functionality. Use it at your own risk, and always follow best practices for web scraping.


This project is not affiliated with or endorsed by the CDC or any other organization. The information provided in this project is for educational purposes only and should not be considered as professional advice. 

The authors of this project are not responsible for any consequences arising from the use of this project.

---

## Getting Started

### Setup

To begin, clone the repository:

```bash
git clone https://github.com/satyanshu404/CDC-Placement-Info-Scraper.git
```
Navigate to the project directory:
```bash
cd CDC-Placement-Info-Scraper
```

Make sure you have Python 3.9+ installed. You can download it from the official Python website: [Python Downloads](https://www.python.org/downloads/).


Install the required dependencies:
```bash
pip install -r requirements.txt
```

This will install the required libraries: 
- `selenium`
- `beautifulsoup4`
- `requests`

You also need to install the Chrome WebDriver. You can download it from the official website: [Chrome WebDriver](https://sites.google.com/chromium.org/driver/downloads). Make sure to download the version that matches your Chrome browser version.

You can check your Chrome version by going to `chrome://settings/help` in your Chrome browser.
After downloading the WebDriver, make sure to add it to your system's PATH environment variable. This will allow the scraper to find the WebDriver executable when running the script.

## Credientials Setup
To run the scraper, you need to set up your credentials. Create a file named `.env` in the project directory and add the following lines:

```env
ERP_USERNAME=""
ERP_PASSWORD=""
ERP_QUESTION_1=""
ERP_ANSWER_1=""
ERP_QUESTION_2=""
ERP_ANSWER_2=""
ERP_QUESTION_3=""
ERP_ANSWER_3=""
```
Replace the empty strings with your actual credentials. The scraper will use these credentials to log in to the CDC website and access the placement information.


## Usage
To start scraping placement data from the CDC website, run:
```bash
python scraper.py
```

This will generate a file named `placement_data.json` in the project directory.


To convert the JSON file into an Excel spreadsheet:
```bash
python convert_json_to_xlsx.py
```
This will create a file named `placement_data.xlsx` in the same directory.

# For Developers

To modify or extend the functionality of the scraper, you can update the following files:

- **`scraper.py`** – Contains the core web scraping logic.
- **`convert_json_to_xlsx.py`** – Responsible for converting scraped JSON data into XLSX format.

The codebase is well-structured and thoroughly commented, making it easy to understand and customize.

If the target website's HTML structure changes in the future, you can update the selectors in **`constants.py`**. This file holds all the HTML tags and class names used by the scraper, allowing you to adapt quickly without altering the main logic.


# Contributing

We welcome contributions of all kinds! If you’d like to help improve this project:

- Open an issue for bug reports, feature requests, or suggestions.
- Submit a pull request with your proposed changes.

Before contributing, Please follow the existing code style and conventions to maintain consistency.

Feedback and ideas for improvement are appreciated. Feel free to get involved by opening an issue or contributing code.







