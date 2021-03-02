from .model import Model


class Favorite(Model):
    __atts__ = {
        'DEVICEID': str,
        'CODIGODOFUNDO': str
    }
