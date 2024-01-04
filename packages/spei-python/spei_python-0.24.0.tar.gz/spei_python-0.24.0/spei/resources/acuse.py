from pydantic import BaseModel

from spei.types import CodigoErrorAcuse, TipoRespuestaAcuse
from spei.utils import to_snake_case  # noqa: WPS347


class Resultado(BaseModel):
    codigo: CodigoErrorAcuse
    descripcion: str

    class Config:  # noqa: WPS306, WPS431
        use_enum_values = True


class Acuse(BaseModel):
    cda_id: str
    mensaje_id: str
    tipo_respuesta: TipoRespuestaAcuse
    resultado_enlace_cep: Resultado
    resultado_banxico: Resultado

    class Config:  # noqa: WPS306, WPS431
        use_enum_values = True

    @classmethod
    def parse_xml(cls, mensaje_element):
        acuse_element = mensaje_element.find('acuse')

        cda_data = cls._find_mensaje_attributes(mensaje_element, acuse_element)
        enlace_cep_data = cls._find_enlace_cep_attributes(acuse_element)
        banxico_data = cls._find_banxico_attributes(acuse_element)

        return cls._build_acuse(acuse_element, cda_data, enlace_cep_data, banxico_data)

    @classmethod
    def _find_enlace_cep_attributes(cls, acuse_element):
        resultado_element = acuse_element.find('resultadoEnlaceCep')
        return {
            'codigo': resultado_element.attrib['codigo'],
            'descripcion': resultado_element.attrib['descripcion'],
        }

    @classmethod
    def _find_banxico_attributes(cls, acuse_element):
        resultado_element = acuse_element.find('resultadoBanxico')
        return {
            'codigo': resultado_element.attrib['codigo'],
            'descripcion': resultado_element.attrib['descripcion'],
        }

    @classmethod
    def _find_mensaje_attributes(cls, mensaje_element, acuse_element):
        return {
            'tipo_respuesta': mensaje_element.attrib['tipoRespuesta'],
            'cda_id': acuse_element.attrib['idCda'],
            'mensaje_id': acuse_element.attrib['idMensaje'],
        }

    @classmethod
    def _build_acuse(cls, acuse_element, cda_data, enlace_cep_data, banxico_data):
        for element in acuse_element.getchildren():
            tag = to_snake_case(element.tag)
            if tag == 'resultado_enlace_cep':
                cda_data[tag] = Resultado(**enlace_cep_data)
                continue
            if tag == 'resultado_banxico':
                cda_data[tag] = Resultado(**banxico_data)
                continue
            if tag in cls.__fields__:
                cda_data[tag] = element.text

        return cls(**cda_data)
