from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from time import sleep
from constant import *
import tools
from bs4 import BeautifulSoup
import pandas as pd
import json
import os
import logging

import tkinter as tk
from tkinter import simpledialog

# GUI popup to manually enter OTP
def get_otp_popup():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    otp = simpledialog.askstring("OTP Input", "Enter OTP:")
    return otp

MIN_CELL_ID:int = 0  # Global variable to track the last processed row

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Parser:
    """Parser class to handle parsing of JNF data"""

    def __init__(self, driver: webdriver.Chrome):
        '''Initialize the parser'''
        self.driver = driver

    def parse_jnf_ids(self, jnf_text: str) -> tuple:
        '''Parse the JNF IDs from the text'''
        jnf_id, com_id, year = [t.split('"')[1] for t in jnf_text.split("(")[1].split(")")[0].split(",")]
        return jnf_id, com_id, year

    def parse_jnf(self, text: str) -> dict:
        '''Parse the JNF text and return a dictionary of key-value pairs'''
        lines = text.strip().splitlines()
        jd_buffer = []  # Buffer for job description section
        flat_json = {}  # Final dictionary to hold parsed data

        section = None
        key = None
        buffer = []  # Temporary buffer for flat section lines

        def flush(buffer, key):
            '''Helper to save buffered lines into the dictionary'''
            if key:
                flat_json[key.rstrip(":").strip()] = "\n".join(buffer).strip()

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Detect section change markers
            if line == CDCJNFElements.CTC_TEXT_DELIMETER:
                section = CDCJNFElements.JD_SECTION_DELIMETER
                jd_buffer = []
                continue
            elif line == CDCJNFElements.OTHER_DETAILS_DELIMETER:
                section = CDCJNFElements.FLAT_SECTION_DELIMETER
                continue
            elif line == CDCJNFElements.SELECTION_DETAILS_DELIMETER:
                section = CDCJNFElements.FLAT_SECTION_DELIMETER
                flush(buffer, key)
                key, buffer = None, []
                continue

            # Handle lines based on current section
            if section == CDCJNFElements.JD_SECTION_DELIMETER:
                jd_buffer.append(line)
            elif section == CDCJNFElements.FLAT_SECTION_DELIMETER:
                if line.endswith(":"):
                    flush(buffer, key)
                    key, buffer = line, []
                else:
                    buffer.append(line)

        flush(buffer, key)  # Flush any remaining buffer
        flat_json[CDCJNFElements.JD_SECTION_DELIMETER] = "\n".join(jd_buffer).strip()
        return flat_json

    def set_min_cell_id(self, filename: str) -> None:
        '''Set the minimum cell ID to avoid duplicates'''
        global MIN_CELL_ID
        if not os.path.exists(filename):
            MIN_CELL_ID = 0
        else:
            df = pd.read_json(filename)
            if df.empty:
                MIN_CELL_ID = 0
            else:
                last_row = df.iloc[-1]
                MIN_CELL_ID = int(last_row['id'])
        return None

    def save_jnf_as_json(self, data: dict, filename: str) -> None:
        '''Save the JNF data as a JSON file'''
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                f.write('[]')
        with open(filename, 'r+') as f:
            file_data = json.load(f)
            file_data.append(data)
            f.seek(0)
            json.dump(file_data, f, indent=4)

    def get_jnf_content(self, jnf_id: str, com_id: str, year: str) -> dict:
        '''Get the detailed JNF content from the ERP portal'''
        self.driver.get(CDCJNFElements.JNF_LINK.format(Credentials.USERNAME, year, com_id, jnf_id))
        detail_soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        detail_text = detail_soup.get_text(separator="\n", strip=True)
        parsed_content = self.parse_jnf(detail_text)
        self.driver.back()
        return parsed_content

    def get_jnf_table_data(self):
        '''Parse the JNF table data by scrolling and extracting rows'''
        i = 0
        seen_ids = set()
        scroll = self.driver.find_element(By.ID, JNFTableElements.TABLE_ID)

        while i < JNFTableElements.SCROLL_COUNT:
            # Scroll down to load more entries
            scroll.send_keys(Keys.PAGE_DOWN)
            sleep(JNFTableElements.SLEEP_DURATION)

            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            table = soup.find('table', {'id': JNFTableElements.TABLE_ID})
            if not table:
                logging.error("Table not found...")
                continue

            # Iterate through table rows
            for row in table.find_all('tr', id=True):
                row_id = row.get('id')
                if row_id in seen_ids:
                    continue
                seen_ids.add(row_id)

                try:
                    # Extract basic info from row
                    id_cell = row.find('td', {'aria-describedby': JNFTableElements.ID_CELL}).text.strip()
                    if int(id_cell) <= MIN_CELL_ID:
                        continue
                    company_cell = row.find('td', {'aria-describedby': JNFTableElements.COMPANY_CELL}).text.strip()
                    designation_td = row.find('td', {'aria-describedby': JNFTableElements.DESIGNATION_CELL})
                    designation_text = designation_td.text.strip()

                    designation_link_tag = designation_td.find('a')
                    designation_link = designation_link_tag['onclick'] if designation_link_tag else ''

                    ctc_cell = row.find('td', {'aria-describedby': JNFTableElements.CTC_CELL}).text.strip()

                    row_data = {
                        "id": id_cell,
                        "company_name": company_cell,
                        "role": designation_text,
                        "ctc": ctc_cell
                    }

                    # Get detailed content and merge
                    jnf_id, com_id, year = self.parse_jnf_ids(designation_link)
                    contents = self.get_jnf_content(jnf_id, com_id, year)

                    combined = row_data.copy()
                    combined.update(contents)

                    self.save_jnf_as_json(combined, ParserConstants.JSON_SAVE_PATH)

                except AttributeError:
                    logging.error(f"Error parsing row with ID {row_id}. Skipping this row...")
                    continue

            i += 1  # Move to next scroll iteration
    
class Scraper:
    def __init__(self) -> None:
        '''Initialize the scraper'''
        self.options = self.add_options()
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(ScraperConstants.URL)
        self.element = tools.FindElement(self.driver)
        self.alert = tools.AcceptAlert(self.driver)
        self.locator = tools.Locator()
        self.parser = Parser(self.driver)
        self.jnf_data = []

    def add_options(self) -> None:
        '''Add options to the webdriver'''
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        return options
    
    def login(self) -> None:
        '''Login to ERP portal'''
        # Enter the username and password
        self.element.find(self.locator.by_id(LoggingElements.USER_ID)).send_keys(Credentials.USERNAME)
        self.element.find((By.ID, LoggingElements.PASSWORD)).send_keys(Credentials.PASSWORD)
        # get the question and answer it
        question = self.element.find((By.ID, LoggingElements.QUESTION)).text.lower()
        logging.log(logging.INFO, f"Question: {question}")
        self.element.find((By.ID, LoggingElements.ANSWER)).send_keys(Credentials().QUESTION[question])
        
        # Click on the getotp button
        self.element.find((By.ID, LoggingElements.GET_OTP)).click()
        self.alert.accept()
        # Wait for the OTP popup to appear
        otp_value = get_otp_popup()
        print("OTP Entered:", otp_value)
        self.element.find((By.NAME, LoggingElements.OTP)).send_keys(otp_value)
        self.element.find((By.ID, LoggingElements.LOGIN_FORM_SUBMIT_BUTTON)).click()

    def get_cdc_page(self) -> None:
        '''Get the CDC page'''
        # Click on the CDC tab
        # element.find(locator.by_element('href', CDCElements.HREF)).click()
        self.element.find(self.locator.by_text(CDCElements.CDC_TEXT)).click()
        # Click Student section
        self.element.find(self.locator.by_text(CDCElements.STUDENT_PANEL_NAME)).click()
        # Click on the Application panel    
        self.element.find(self.locator.by_text(CDCElements.APPLICATION_PANEL_NAME)).click()

        # Switch to the contianer of the appication panel
        self.driver.get(CDCElements.APPLICATION_CONTAINER_URL)


    def get_jnf_data(self) -> None:
        '''Get the JNF data'''
        self.parser.get_jnf_table_data()
        logging.info(f"All JNF data has been saved to {ParserConstants.JSON_SAVE_PATH}")
        self.driver.quit()

    def run(self) -> None:
        '''Run the scraper'''
        self.login()
        self.get_cdc_page()
        sleep(5)
        self.parser.set_min_cell_id(ParserConstants.JSON_SAVE_PATH)
        logging.info(f"Minimum cell ID set to {MIN_CELL_ID}...")
        self.get_jnf_data()
        logging.info("Scraping completed...")


if __name__ == "__main__":
    scraper = Scraper()
    scraper.run()


    



        

