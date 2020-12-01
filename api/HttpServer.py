from aiohttp import web


class HttpServer:
    def __init__(self, dbmng):
        print('Starting HTTP Server')
        self.dbmng = dbmng
        self.server = None
        self.runner = None
        self.site = None

    async def run(self, h, p):
        print('Runnin HTTP Server')
        self.server = web.Server(self.handle)
        self.runner = web.ServerRunner(self.server)
        await self.runner.setup()
        self.site = web.TCPSite(self.runner, h, p)
        await self.site.start()

    async def handle(self, request):
        print(f'request: {request}')
        if request.method != 'GET':
            raise web.HTTPMethodNotAllowed()
        if request.path != '/fii':
            raise web.HTTPNotFound()
        # TODO: verificar token
        return web.json_response({
            'fiis': self.dbmng.getFiis()
        }, headers={
            'Access-Control-Allow-Origin': '*'
        })
