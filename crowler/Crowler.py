import string
from selenium import webdriver
import unicodedata


class DriverSessMng:
    def __init__(self, exec_path):
        self.exec_path = exec_path
        self.driver = None

    def __enter__(self):
        print('Connecting to the browser')
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')

        self.driver = webdriver.Chrome(
            executable_path=self.exec_path,
            service_args=['--verbose', '--log-path=chromedriver.log'],
            chrome_options=chrome_options)
        self.driver.set_page_load_timeout(60)

        return self.driver

    def __exit__(self, t, v, tb):
        print('Closing browser...')
        self.driver.close()
        self.driver.quit()
        self.driver = None


class Crowler:
    ic = string.whitespace + "();.'/"
    translator = str.maketrans(dict(zip(ic, ['' for i in ic])))

    def __init__(self, exec_path):
        print('Starting Crowler')
        self.exec_path = exec_path

    def _normalize(self, h):
        return unicodedata.normalize('NFD', h).\
            encode('ascii', 'ignore').\
            decode("utf-8").\
            translate(Crowler.translator)

    def _get_headers(self, table):
        print('Getting headers')
        hdr = table.find_element_by_tag_name('thead')
        hdr_line = hdr.find_element_by_tag_name('tr')
        return [self._normalize(hdrc.text)
                for hdrc in hdr_line.find_elements_by_tag_name('th')]

    def _get_fiis(self):
        print('Getting Fiis')
        with DriverSessMng(self.exec_path) as driver:
            driver.get('https://www.fundsexplorer.com.br/ranking')
            print('Page was loaded')
            table = driver.find_element_by_id("table-ranking")
            print('Table found')
            header = self._get_headers(table)
            body = table.find_element_by_tag_name('tbody')
            for ftbe in body.find_elements_by_tag_name('tr'):
                atts = [
                    v.get_attribute('data-index') or
                    v.get_attribute('data-order') or
                    v.get_attribute('data-valor') or
                    self._normalize(v.text).lower()
                    for v in ftbe.find_elements_by_tag_name('td')]
                # print(f'LEN: {len(header)} / {len(atts)}')
                yield dict(zip(header, atts))

    def get_fiis(self):
        return [i for i in self._get_fiis()]
