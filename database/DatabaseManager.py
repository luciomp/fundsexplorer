import sqlite3
from datetime import datetime
from models.Fii import Fii


class DatabaseManager:
    def __init__(self, cstr):
        print('Starting Db Manager')
        self.conn = sqlite3.connect(cstr)
        self.checkTable()

    def checkTable(self):
        cur = self.conn.cursor()
        cur.execute(Fii.genCreateSQL())
        self.conn.commit()

    def insertFiis(self, fiis: list):
        print('Inserting FIIs')
        try:
            # TODO: keep onyl 30 executions
            cur = self.conn.cursor()
            codexec = datetime.now().isoformat()
            for fii in fiis:
                fii['CODIGOEXEC'] = codexec
                sql = Fii(fii).toSQL()
                print(f"Inserting fii: {fii['CODIGODOFUNDO']}")
                cur.execute(sql)
            self.conn.commit()
        except Exception as err:
            print(f'Error: {err}')
            self.conn.rollback()

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


if __name__ == '__main__':
    def do(*args):
        pass
    DatabaseManager.checkTable = do
    mng = DatabaseManager(r'database/db.sqlite')
    print(mng.getSetores())
    # for i in mng.getFiis():
    #     print(i)
