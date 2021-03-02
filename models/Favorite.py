from .model import Model, sqlType

class Favorite(Model):
    __atts__ = {
        'deviceid': str,
        'codigodofundo': str
    }

    @classmethod
    def sql_create(cls):
        c = ','.join(f'{k} {sqlType(v)}' for k, v in cls.__atts__.items())
        return f'''CREATE TABLE IF NOT EXISTS {cls.tablename()} ({c},
            CREATEDAT TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY(DEVICEID, CODIGODOFUNDO))'''
