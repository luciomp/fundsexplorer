import sqlite3
from datetime import datetime
from models.Fii import Fii
from models.Favorite import Favorite


class DatabaseManager:
    def __init__(self, cstr):
        print('Starting Db Manager')
        self.conn = sqlite3.connect(cstr)
        self.run_sql(Fii.sql_create())
        self.run_sql(Favorite.sql_create())

    def run_sql(self, sql):
        cur = self.conn.cursor()
        r = [i for i in cur.execute(sql)]
        self.conn.commit()
        return r

    def _cleanFiis(self):
        print('Cleaning Old Fiis')
        try:
            cur = self.conn.cursor()
            cur.execute(f'''DELETE FROM {Fii.__tablename__}
                WHERE CODIGOEXEC NOT IN (
                    SELECT distinct(CODIGOEXEC) FROM {Fii.__tablename__}
                        order by CODIGOEXEC desc
                        limit 60
            )''')
            print(f'Deleted {cur.rowcount} row(s)')
            self.conn.commit()
        except Exception as err:
            print(f'Error: {err}')
            self.conn.rollback()

    def _insertFiis(self, fiis: list):
        print('Inserting FIIs')
        try:
            cur = self.conn.cursor()
            codexec = datetime.now().isoformat()
            for fii in fiis:
                print(f"Inserting fii: {fii['CODIGODOFUNDO']}")
                fii['CODIGOEXEC'] = codexec
                cur.execute(Fii(fii).toSQL())
            self.conn.commit()
        except Exception as err:
            print(f'Error: {err}')
            self.conn.rollback()

    def insertFiis(self, fiis: list):
        self._cleanFiis()
        self._insertFiis(fiis)

    def getFiis(self):
        print('Getting FIIs')
        cur = self.conn.cursor()
        return [Fii(i).atts for i in cur.execute(
            f'''{Fii.genSelectSQL()} WHERE CODIGOEXEC in (
                select MAX(CODIGOEXEC) FROM {Fii.__tablename__})'''
        )]

    def getLastExecution(self):
        print('Getting Last Execution')
        cur = self.conn.cursor()
        cur.execute(f'SELECT max(CREATEDAT) from {Fii.__tablename__}')
        r = cur.fetchone()[0]
        return datetime.strptime(r, '%Y-%m-%d %H:%M:%S')\
            if r else datetime.fromtimestamp(0)

    def getSetores(self):
        print('Getting Setores')
        cur = self.conn.cursor()
        cur.execute(f'SELECT distinct(setor) from {Fii.__tablename__}')
        return cur.fetchall()
