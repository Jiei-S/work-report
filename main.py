""" Run """
from module.scraping import (
    scraping, ScrapingError
)
from module.report import make_report
from module.line import (
    send_success, send_error
)


def run():
    """ run """
    try:
        scraping()
        make_report()
        send_success()
    except ScrapingError as exc:
        send_error(f'Scraping Failed: {exc}')
    except Exception as exc:
        send_error(exc)


if __name__ == "__main__":
    run()
