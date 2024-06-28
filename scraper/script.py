from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from time import sleep
from constant import *
import tools
from bs4 import BeautifulSoup
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Scraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get(ScraperConstants.URL)
        self.element = tools.FindElement(self.driver)
        self.alert = tools.AcceptAlert(self.driver)
        self.locator = tools.Locator()
    
    def login(self):
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
        # Enter the OTP
        self.element.find((By.ID, LoggingElements.OTP)).send_keys(input("Enter OTP: "))
        self.element.find((By.ID, LoggingElements.LOGIN_FORM_SUBMIT_BUTTON)).click()

    def get_cdc_page(self):
        '''Get the CDC page'''
        # Click on the CDC tab
        self.element.find(self.locator.by_element('href', CDCElements.HREF)).click()
        # Click Student section
        self.element.find(self.locator.by_text(CDCElements.STUDENT_PANEL_NAME)).click()
        # Click on the Application panel    
        self.element.find(self.locator.by_text(CDCElements.APPLICATION_PANEL_NAME)).click()

        # Switch to the contianer of the appication panel
        self.driver.get(CDCElements.APPLICATION_CONTAINER_URL)

    def scrape_notic(self):
        ...

    def scrape_data(self, page_source:str):
        soup = BeautifulSoup(page_source, 'html.parser')
        table = soup.find('table')
        table_data = []
        for row in table.find_all('tr'):
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            table_data.append(cols)
        
        df = pd.DataFrame(table_data)
        # save to excel
        df.to_excel('data.xlsx', index=False)

        

