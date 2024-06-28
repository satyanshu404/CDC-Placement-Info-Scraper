from dataclasses import dataclass, field

@dataclass
class ScraperConstants:
    URL:str = 'https://erp.iitkgp.ac.in'

@dataclass
class Credentials:
    USERNAME:str = ""
    PASSWORD:str = ""
    QUESTION: dict = field(default_factory=lambda: {
        '': '',
        '': '',
        '': ''
    })

@dataclass
class FindElementConstants:
    WAIT_DURATION:int = 60
    SCRIPT:str = "arguments[0].scrollIntoView(true);"

@dataclass
class AcceptAlertConstants:
    WAIT_DURATION:int = 60
    SCRIPT:str = "arguments[0].scrollIntoView(true);"
    
@dataclass
class LoggingElements:
    USER_ID:str = 'user_id'
    PASSWORD:str = 'password'
    QUESTION:str = 'question'
    ANSWER:str = 'answer'
    GET_OTP:str = 'getotp'
    OTP:str = 'otp'
    LOGIN_FORM_SUBMIT_BUTTON:str = 'loginFormSubmitButton'


@dataclass
class CDCElements:
    HREF:str = '//*[@href="menulist.htm?module_id=26"]'
    STUDENT_PANEL_NAME:str = 'Student'
    APPLICATION_PANEL_NAME:str = 'Application of Placement/Internship'
    APPLICATION_CONTAINER_URL:str = ''

    