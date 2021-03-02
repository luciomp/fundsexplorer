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

    @classmethod
    def tablename(cls):
        return cls.__tablename__ if cls.__tablename__ else cls.__name__

    @classmethod
    def sql_create(cls):
        c = ','.join(f'{k} {sqlType(v)}' for k, v in cls.__atts__.items())
        return f'''CREATE TABLE IF NOT EXISTS {cls.tablename()} ({c},
            CREATEDAT TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP)'''

    @classmethod
    def sql_select(cls, d = None):
        keys = ','.join(cls.__atts__.keys())
        r = f'SELECT {keys} FROM {cls.tablename()}'
        if d:
            w = " and ".join([f"{k} = '{v}'" for k,v in d.items()])
            r += f' where {w}'
        return r

    @classmethod
    def sql_delete(cls, d = None):
        r = f'DELETE FROM {cls.tablename()}'
        if d:
            w = " and ".join([f"{k} = '{v}'" for k,v in d.items()])
            r += f' where {w}'
        return r

    def __init__(self, a):
        self.atts = {}
        if isinstance(a, dict):
            self.fromDict(a)
        elif isinstance(a, tuple):
            self.fromTuple(a)
        else:
            raise Exception('Ony dict or list are acceptable parameter types')

    def fromDict(self, d):
        for a, t in type(self).__atts__.items():
            assert a in d
            self.atts[a] = d[a]

    def fromTuple(self, d):
        for i, kv in enumerate(type(self).__atts__.items()):
            k, v = kv
            assert isinstance(d[i], v)
            self.atts[k] = d[i]

    def sql_insert(self):
        keys = ','.join(self.atts.keys())
        values = "','".join([str(i) for i in self.atts.values()])
        return f"""INSERT INTO {type(self).tablename()} ({keys})
                VALUES ('{values}')"""


if __name__ == '__main__':
    class Person(Model):
        __atts__ = {'name': str, 'age': int}

    class Car(Model):
        __atts__ = {'brand': str, 'km': int}

    print(Person.sql_create())
    print(Car.sql_create())
    print(Person.sql_select())
    print(Car.sql_select())
    p = Person({'name': 'lucio', 'age': 37})
    print(p.sql_insert())
    c = Car({'brand': 'BMW', 'km': 55000})
    print(c.sql_insert())
