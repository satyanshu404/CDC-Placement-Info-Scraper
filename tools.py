from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import constant

class FindElement:
    '''FindElement class is a wrapper class for WebDriverWait and execute_script method of selenium.webdriver.Chrome'''
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.duration: int = constant.FindElementConstants.WAIT_DURATION
        self.script: str = constant.FindElementConstants.SCRIPT
    
    def find(self, locator:tuple):
        '''find the element based on the locator
           Args: locator: tuple: (By, str)
           for example: (By.ID, 'id')
           Returns: WebElement'''
        element = WebDriverWait(self.driver, self.duration).until(
            EC.element_to_be_clickable(locator)
        )
        self.driver.execute_script(self.script, element)
        return element 
    
class AcceptAlert:
    '''Accept the alert popup if present'''
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.duration: int = constant.AcceptAlertConstants.WAIT_DURATION

    def accept(self):
        WebDriverWait(self.driver, self.duration).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert.accept()

class Locator:
    def __init__(self):
        pass
    def by_id(self, element_text: str) -> tuple:
        return (By.ID, element_text)
    
    def by_xpath(self, element_text: str) -> tuple:
        return (By.XPATH, element_text)
    
    def by_link_text(self, element_text: str) -> tuple:
        return (By.LINK_TEXT, element_text)
    
    def by_class_name(self, element_text: str) -> tuple:
        return (By.CLASS_NAME, element_text)
    
    def by_name(self, element_text: str) -> tuple:
        return (By.NAME, element_text)
    
    def by_text(self, element_text: str) -> tuple:
       return (By.XPATH, f"//*[contains(text(), '{element_text}')]")
    
    def by_element(self, element:str, text:str) -> tuple:
        return (By.XPATH, f'//*[@{element}={text}]')
    
    def by_css(self, element_text: str) -> tuple:
        return (By.CSS_SELECTOR, element_text)