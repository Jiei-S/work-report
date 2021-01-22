""" LINE Notification """
import os
import requests

import module.report

URL = os.environ['LINE_URL']
TOKEN = os.environ['LINE_TOKEN']
HEADERS = {'Authorization': 'Bearer '+ TOKEN}


def send_success():
    """ Scraping Success """
    requests.post(
        URL, headers=HEADERS, params={'message': report.TODAY},
        files={'imageFile': open('./module/report.png', 'rb')}
    )
    os.remove('./module/report.png')


def send_error(msg):
    """ Scraping Failed

    @param msg: error message
    """
    requests.post(URL, headers=HEADERS, params={'message': msg})
