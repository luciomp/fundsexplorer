from aiohttp import web


class FiiResource:
    def __init__(self, dbmng):
        self.dbmng = dbmng

    def list(self, request):
        return web.json_response({
            'fiis': self.dbmng.getFiis()
        })
