""" Scraping """
import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    WebDriverException,
    NoSuchElementException
)

OPTS = Options()
OPTS.add_argument('--headless')
OPTS.add_argument('--no-sandbox')
OPTS.add_argument('--disable-dev-shm-usage')
DRV = webdriver.Chrome(executable_path='lib/chromedriver', options=OPTS)


class ScrapingError(Exception):
    """ Scraping Error """
    pass


def login():
    """ Login """
    DRV.get(os.environ['WORK_LOGIN_URL'])
    DRV.find_element_by_id('contractId').send_keys(os.environ['WORK_ID'])
    DRV.find_element_by_id('authId').send_keys(os.environ['WORK_AUTH'])
    DRV.find_element_by_id('password').send_keys(os.environ['WORK_PASSWORD'])

    time.sleep(2)

    DRV.find_element_by_tag_name("button").click()


def transition_to_download():
    """ Transition To Download Page """
    DRV.get(os.environ['WORK_DW_URL'])
    DRV.execute_script("loadExportDialogForAttendance('01')")

    time.sleep(3)

    DRV.execute_script('downloadLayout()')


def close_driver():
    """ Close Driver """
    DRV.close()
    DRV.quit()


def scraping():
    """ Scraping

    @Exception ScrapingError: Scraping Error
    """
    try:
        login()
        transition_to_download()

        DRV.command_executor._commands["send_command"] = \
            ("POST", '/session/$sessionId/chromium/send_command')

        params = {
            'cmd': 'Page.setDownloadBehavior',
            'params': {
                'behavior': 'allow',
                'downloadPath': 'module'
            }
        }

        DRV.execute("send_command", params)

        time.sleep(5)

    except (NoSuchElementException, WebDriverException) as exc:
        raise ScrapingError(exc) from exc
    finally:
        close_driver()
