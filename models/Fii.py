from .model import Model


class Fii(Model):
    __tablename__ = 'FII'
    __atts__ = {
        'CODIGODOFUNDO': str,
        'SETOR': str,
        'PRECOATUAL': float,
        'LIQUIDEZDIARIA': float,
        'DIVIDENDO': float,
        'DIVIDENDYIELD': float,
        'DY3MACUMULADO': float,
        'DY6MACUMULADO': float,
        'DY12MACUMULADO': float,
        'DY3MMEDIA': float,
        'DY6MMEDIA': float,
        'DY12MMEDIA': float,
        'DYANO': float,
        'VARIACAOPRECO': float,
        'RENTABPERIODO': float,
        'RENTABACUMULADA': float,
        'PATRIMONIOLIQ': float,
        'VPA': float,
        # 'PVPA': float,
        'DYPATRIMONIAL': float,
        'VARIACAOPATRIMONIAL': float,
        'RENTABPATRNOPERIODO': float,
        'RENTABPATRACUMULADA': float,
        'VACANCIAFISICA': float,
        'VACANCIAFINANCEIRA': float,
        'QUANTIDADEATIVOS': int,
        'CODIGOEXEC': str
    }
