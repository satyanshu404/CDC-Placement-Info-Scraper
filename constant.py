from dataclasses import dataclass, field
import os
from dotenv import load_dotenv

load_dotenv(override=True)

@dataclass
class ScraperConstants:
    URL:str = 'https://erp.iitkgp.ac.in'

@dataclass
class Credentials:
    USERNAME:str = os.getenv('ERP_USERNAME')
    PASSWORD:str = os.getenv('ERP_PASSWORD')
    QUESTION: dict = field(default_factory=lambda: {
        os.getenv('ERP_QUESTION_1'): os.getenv('ERP_ANSWER_1'),
        os.getenv('ERP_QUESTION_2'): os.getenv('ERP_ANSWER_2'),
        os.getenv('ERP_QUESTION_3'): os.getenv('ERP_ANSWER_3')
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
    OTP:str = 'email_otp'
    LOGIN_FORM_SUBMIT_BUTTON:str = 'loginFormSubmitButton'

@dataclass
class CDCElements:
    HREF:str = '//*[@href="menulist.htm?module_id=26"]'
    CDC_TEXT:str = 'CDC'
    STUDENT_PANEL_NAME:str = 'Student'
    APPLICATION_PANEL_NAME:str = 'Application of Placement/Internship'
    APPLICATION_CONTAINER_CLASS_NAME:str = 'text-default'
    APPLICATION_CONTAINER_URL:str = 'https://erp.iitkgp.ac.in/TrainingPlacementSSO/TPStudent.jsp'

@dataclass
class JNFTableElements:
    SCROLL_COUNT:int = 350
    SLEEP_DURATION:int = 2
    TABLE_ID:str = 'grid37'
    ID_CELL: str = 'grid37_rn'
    COMPANY_CELL: str = 'grid37_companyname'
    DESIGNATION_CELL: str = 'grid37_designation'
    CTC_CELL: str = 'grid37_ctc'
    JNF_ID_CELL: str = 'grid37_jnf_id'
    

@dataclass
class CDCJNFElements:
    CTC_TEXT_DELIMETER:str = 'Job Description'
    OTHER_DETAILS_DELIMETER:str = 'Other Details'
    SELECTION_DETAILS_DELIMETER:str = 'Selection Details'
    #  no need to change the following 
    JNF_LINK:str = 'https://erp.iitkgp.ac.in/TrainingPlacementSSO/JnfMoreDet.jsp?mode=jnfMoreDet&rollno={}&year={}&com_id={}&jnf_id={}'
    JD_SECTION_DELIMETER:str = 'jd'
    FLAT_SECTION_DELIMETER:str = 'flat'

@dataclass
class ParserConstants:
    JSON_SAVE_PATH:str = 'data.json'