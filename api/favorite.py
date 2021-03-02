from aiohttp import web
from models.Favorite import Favorite
import sqlite3


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
        f = Favorite({
            'deviceid': params[2],
            'codigodofundo': params[3]
        })
        try:
            self.dbmng.run_sql(f.sql_insert())
            return web.Response(status=201)
        except sqlite3.IntegrityError:
            return web.Response(status=422)

    # GET favorite/{deviceid}
    def list(self, request):
        params = request.path.split('/')
        if len(params) != 3:
            raise web.HTTPBadRequest()
        r = self.dbmng.run_sql(Favorite.sql_select({
            'deviceid': params[2]
        }))
        return web.json_response({
            'favorites': [Favorite(i).atts for i in r]
        })

    # DELETE favorito/{deviceid}/{FII}
    def delete(self, request):
        params = request.path.split('/')
        if len(params) != 4:
            raise web.HTTPBadRequest()
        self.dbmng.run_sql(Favorite.sql_delete({
            'deviceid': params[2],
            'codigodofundo': params[3]
        }))
        return web.Response(status=200)
