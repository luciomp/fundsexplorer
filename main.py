from selenium import webdriver
import psycopg2
import string
import unicodedata
from datetime import datetime


class DatabaseManager:
    def __init__(self):
        print('Starting Db Manager')
        self.conn = psycopg2.connect(
            host='127.0.0.1',
            dbname='fundsfiidb',
            user='postgres',
            password='postgres')

    def insertFiis(self, fiis: list):
        print('Inserting FIIs')
        with self.conn.cursor() as cur:
            try:
                codexec = datetime.now().isoformat()
                for fii in fiis:
                    fii['CODIGOEXEC'] = codexec
                    print(f'Inserting fii: {fii}')
                    keys = ','.join(fii.keys())
                    values = "','".join(fii.values())
                    # print(f'Kyes: {keys}')
                    print(f'Values: {values}')
                    cur.execute(
                        f"INSERT INTO FII ({keys}) VALUES ('{values}')")
                self.conn.commit()
            except Exception as err:
                print(f'Error: {err}')
                self.conn.rollback()


class Crowler:
    ic = string.whitespace + "();.'/"
    translator = str.maketrans(dict(zip(ic, ['' for i in ic])))

    def __init__(self):
        print('Starting Crowler')
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')

        self.driver = webdriver.Chrome(
            executable_path='/usr/bin/chromedriver-86',
            chrome_options=chrome_options,
            service_args=['--verbose', '--log-path=/var/log/chromedriver.log'])
        self.driver.set_page_load_timeout(30)

    def close(self):
        print('Closing browser...')
        self.driver.close()
        self.driver.quit()

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

    def get_fiis(self):
        print('Getting Fiis')
        self.driver.get('https://www.fundsexplorer.com.br/ranking')
        table = self.driver.find_element_by_id("table-ranking")
        header = self._get_headers(table)
        body = table.find_element_by_tag_name('tbody')
        for ftbe in body.find_elements_by_tag_name('tr'):
            print('Getting Fii')
            atts = [
                v.get_attribute('data-index') or
                v.get_attribute('data-order') or
                v.get_attribute('data-valor') or
                self._normalize(v.text).lower()
                for v in ftbe.find_elements_by_tag_name('td')]
            print(f'LEN: {len(header)} / {len(atts)}')
            yield dict(zip(header, atts))


if __name__ == '__main__':
    try:
        crowler = Crowler()
        db = DatabaseManager()
        db.insertFiis(crowler.get_fiis())
    except Exception as err:
        print(f'Exception: {err}')
    finally:
        if crowler:
            crowler.close()
