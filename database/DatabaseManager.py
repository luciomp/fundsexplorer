import sqlite3
from datetime import datetime
from models.Fii import Fii
from models.Favorite import Favorite


class DatabaseManager:
    def __init__(self, cstr):
        print('Starting Db Manager')
        self.conn = sqlite3.connect(cstr)
        self.checkTable()

    def checkTable(self):
        cur = self.conn.cursor()
        cur.execute(Fii.genCreateSQL())
        cur.execute(Favorite.genCreateSQL())
        self.conn.commit()

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

    def insertFavorite(self, deviceid, fii):
        cur = self.conn.cursor()
        cur.execute(f"insert into FAVORITE (DEVICEID, CODIGODOFUNDO) values ('{deviceid}', '{fii}')")
        self.conn.commit()

    def deleteFavorite(self, deviceid, fii):
        cur = self.conn.cursor()
        cur.execute(f"delete from FAVORITE where DEVICEID='{deviceid}' and CODIGODOFUNDO='{fii}'")
        self.conn.commit()

    def getFavorites(self, i: dict):
        cur = self.conn.cursor()
        return [i for i in cur.execute('select CODIGODOFUNDO from FAVORITE')]

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


if __name__ == '__main__':
    def do(*args):
        pass
    DatabaseManager.checkTable = do
    mng = DatabaseManager(r'database/db.sqlite')
    print(mng.getSetores())
    # for i in mng.getFiis():
    #     print(i)
