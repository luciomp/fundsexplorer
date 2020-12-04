from aiohttp import web

SECRET = '42399549-e526-48ab-bd46-126f83f04a4c'


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
        # Only GET method is allowed
        if request.method != 'GET' and request.method != 'OPTIONS':
            raise web.HTTPMethodNotAllowed(request.method, ['GET', 'OPTIONS'])
        # Only fii route is available
        if request.path != '/fii':
            raise web.HTTPNotFound()
        # OPTIONS response
        if request.method == 'OPTIONS':
            return web.json_response(headers = {
                'Access-Control-Allow-Headers': 'Authorization',
                'Access-Control-Allow-Origin': '*'
            })
        # Authentication is needed
        if request.headers.get('AUTHORIZATION') is None:
           raise web.HTTPForbidden()
        # Assert rigth secret
        if request.headers.get('AUTHORIZATION') != SECRET:
           raise web.HTTPUnauthorized()
        # Ok
        return web.json_response({
            'fiis': self.dbmng.getFiis()
        }, headers={
            'Access-Control-Allow-Origin': '*'
        })
