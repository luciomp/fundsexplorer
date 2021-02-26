from database.DatabaseManager import DatabaseManager
from crowler.Crowler import Crowler
from api.HttpServer import HttpServer
import asyncio
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

EXEC_PATH = r'/usr/local/bin/chromedriver'
# EXEC_PATH = r'.\bin\chromedriver.exe'
SQLITE_DBPATH = r'database/db.sqlite'
PG_CSTR = r'host=127.0.0.1 dbname=fundsfiidb user=postgres password=postgres'
CROWLER_PERIOD = 12
SLEEP_INTERVAL = 900


class App:
    def __init__(self):
        self.db = None
        self.crowler = None
        self.api_server = None
        self.crowlerExecutor = ThreadPoolExecutor(max_workers=1)

    async def crowlerTask(self):
        while True:
            print('Running Crowler Task')
            try:
                last_exec = self.db.getLastExecution()
                now = datetime.now()
                if last_exec < now - timedelta(hours=CROWLER_PERIOD):
                    loop = asyncio.get_running_loop()
                    fiis = await loop.run_in_executor(
                        self.crowlerExecutor, self.crowler.get_fiis)
                    self.db.insertFiis(fiis)
            except asyncio.CancelledError:
                print('Crowler task signaled to stop')
                break
            except Exception as err:
                print('Exception running crowler task: ' + str(err))
            finally:
                await asyncio.sleep(SLEEP_INTERVAL)

    async def run(self):
        self.db = DatabaseManager(SQLITE_DBPATH)
        self.api_server = HttpServer(self.db)
        self.crowler = Crowler(EXEC_PATH)
        await self.api_server.run('0.0.0.0', 8080)
        await self.crowlerTask()


if __name__ == '__main__':
    try:
        app = App()
        asyncio.run(app.run())
    except KeyboardInterrupt:
        print('System signaled to stop')
    except Exception as err:
        print(f'Exception: {err}')
