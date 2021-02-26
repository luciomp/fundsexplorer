def sqlType(v):
    if v == int:
        return 'INTEGER'
    if v == float:
        return 'REAL'
    if v == str:
        return 'TEXT'
    raise Exception(f'type "{v}" is not supported')


class Model:
    __tablename__ = ''
    __atts__ = {}

    def genCreateSQL():
        c = ','.join(f'{k} {sqlType(v)}' for k, v in Model.__atts__.items())
        return f'''CREATE TABLE IF NOT EXISTS {Fii.__tablename__} ({c},
            CREATEDAT TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP)'''

    def genSelectSQL():
        keys = ','.join(Fii.__atts__.keys())
        return f'SELECT {keys} FROM {Fii.__tablename__}'

    def __init__(self, a):
        self.atts = {}
        if isinstance(a, dict):
            self.fromDict(a)
        elif isinstance(a, tuple):
            self.fromTuple(a)
        else:
            raise Exception('Ony dict or list are acceptable parameter types')

    def fromDict(self, d):
        for a, t in Fii.__atts__.items():
            assert a in d
            self.atts[a] = d[a]

    def fromTuple(self, d):
        for i, kv in enumerate(Fii.__atts__.items()):
            k, v = kv
            assert isinstance(d[i], v)
            self.atts[k] = d[i]

    def toSQL(self):
        keys = ','.join(self.atts.keys())
        values = "','".join(self.atts.values())
        return f"INSERT INTO {Fii.__tablename__} ({keys}) VALUES ('{values}')"


if __name__ == '__main__':
    print(Fii.genCreateSQL())
    print(Fii.genSelectSQL())
