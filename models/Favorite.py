def sqlType(v):
    if v == int:
        return 'INTEGER'
    if v == float:
        return 'REAL'
    if v == str:
        return 'TEXT'
    raise Exception(f'type "{v}" is not supported')


class Favorite:
    __tablename__ = 'FAVORITE'
    __atts__ = {
        'DEVICEID': str,
        'CODIGODOFUNDO': str
    }

    def genCreateSQL():
        c = ','.join(f'{k} {sqlType(v)}' for k, v in Favorite.__atts__.items())
        return f'''CREATE TABLE IF NOT EXISTS {Favorite.__tablename__} ({c},
            CREATEDAT TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP)'''

    def genSelectSQL():
        keys = ','.join(Favorite.__atts__.keys())
        return f'SELECT {keys} FROM {Favorite.__tablename__}'

    def __init__(self, a):
        self.atts = {}
        if isinstance(a, dict):
            self.fromDict(a)
        elif isinstance(a, tuple):
            self.fromTuple(a)
        else:
            raise Exception('Ony dict or list are acceptable parameter types')

    def fromDict(self, d):
        for a, t in Favorite.__atts__.items():
            assert a in d
            self.atts[a] = d[a]

    def fromTuple(self, d):
        for i, kv in enumerate(Favorite.__atts__.items()):
            k, v = kv
            assert isinstance(d[i], v)
            self.atts[k] = d[i]

    def toSQL(self):
        keys = ','.join(self.atts.keys())
        values = "','".join(self.atts.values())
        return f"INSERT INTO {Favorite.__tablename__} ({keys}) VALUES ('{values}')"


if __name__ == '__main__':
    print(Favorite.genCreateSQL())
    print(Favorite.genSelectSQL())
