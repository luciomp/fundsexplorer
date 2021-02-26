from aiohttp import web
from .fii import FiiResource
from .favorite import FavoriteResource


class HttpServer:
    SECRET = '42399549-e526-48ab-bd46-126f83f04a4c'
    methods = {
        'POST': 'add',
        'GET': 'list',
        'DELETE': 'delete',
        'PUT': 'updt'
    }

    def __init__(self, dbmng):
        print('Starting HTTP Server')
        self.server = None
        self.runner = None
        self.site = None
        self.resources = {
            'fii': FiiResource(dbmng),
            'favorite': FavoriteResource(dbmng)
        }

    async def run(self, h, p):
        print('Runnin HTTP Server')
        self.server = web.Server(self.handle)
        self.runner = web.ServerRunner(self.server)
        await self.runner.setup()
        self.site = web.TCPSite(self.runner, h, p)
        await self.site.start()

    def call(self, rsc, httpm, request):
        c = getattr(rsc, HttpServer.methods.get(httpm, 'err'), None)
        if callable(c):
            return c(request)
        else:
            raise web.HTTPMethodNotAllowed(httpm, ['OPTIONS'])

    async def handle(self, request):
        print(request)
        params = request.path.split('/')
        if len(params) < 2 or params[1] not in self.resources:
            raise web.HTTPNotFound()

        # OPTIONS response
        if request.method == 'OPTIONS':
            return web.json_response(headers={
                'Access-Control-Allow-Headers': 'Authorization',
                'Access-Control-Allow-Origin': '*'
            })

        # Authentication is needed
        if request.headers.get('AUTHORIZATION') is None:
            raise web.HTTPForbidden()

        # Assert rigth secret
        if request.headers.get('AUTHORIZATION') != HttpServer.SECRET:
            raise web.HTTPUnauthorized()

        resp = self.call(self.resources[params[1]], request.method, request)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        print(resp)
        return resp
