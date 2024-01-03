from lxml import etree

from spei.resources import Acuse


class MensajeElement(object):
    def __new__(cls, acuse, acuse_cls: Acuse = Acuse):
        mensaje = etree.fromstring(  # noqa: S320
            bytes(acuse.text, encoding='cp850'),
        )
        return acuse_cls.parse_xml(mensaje)


class AcuseElement(object):
    def __new__(cls, body):
        return body.find('{http://www.praxis.com.mx/}acuse')


class BodyElement(object):
    def __new__(cls, mensaje):
        return mensaje.find(
            '{http://schemas.xmlsoap.org/soap/envelope/}Body',
        )


class AcuseResponse(object):
    def __new__(cls, acuse):
        mensaje = etree.fromstring(acuse)  # noqa: S320
        return MensajeElement(AcuseElement(BodyElement((mensaje))))
