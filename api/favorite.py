from aiohttp import web


class FavoriteResource:
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    def __init__(self, dbmng):
        self.dbmng = dbmng

    # POST /favorito/{deviceid}/{FII}
    def add(self, request):
        params = request.path.split('/')
        if len(params) != 4:
            raise web.HTTPBadRequest()
        self.dbmng.insertFavorite(params[2], params[3])
        return web.Response(status=201)

    # GET favorite/{deviceid}
    def list(self, request):
        params = request.path.split('/')
        if len(params) != 3:
            raise web.HTTPBadRequest()
        return web.json_response({
            'favorites': self.dbmng.getFavorites(params[2])
        })

    # DELETE favorito/{deviceid}/{FII}
    def delete(self, request):
        params = request.path.split('/')
        if len(params) != 4:
            raise web.HTTPBadRequest()
        self.dbmng.deleteFavorite(params[2], params[3])
        return web.Response(status=200)
