# -*- coding: utf-8 -*-
from tag_destinatario import TagDestinatario
from tag_nacional import TagNacional
from tag_dimensao_objeto import TagDimensaoObjeto
from etiqueta import Etiqueta
from servico_postagem import ServicoPostagem
from tag_servico_adicional import TagServicoAdicional
from tag_base import TagBase


class TagObjetoPostal(TagBase):

    def __init__(self, obj_destinatario, obj_destino_nacional,
                 obj_dimensao_objeto, obj_servico_postagem,
                 obj_servico_adicional, ob_etiqueta):

        if not isinstance(obj_destinatario, TagDestinatario):
            raise TypeError
        self.destinatario = obj_destinatario

        if not isinstance(obj_destino_nacional, TagNacional):
            raise TypeError
        self.destino_nacional = obj_destino_nacional

        if not isinstance(obj_dimensao_objeto, TagDimensaoObjeto):
            raise TypeError
        self.dimensao_objeto = obj_dimensao_objeto

        if not isinstance(obj_servico_postagem, ServicoPostagem):
            raise TypeError
        self.servico_postagem = obj_servico_postagem

        if not isinstance(obj_servico_adicional, TagServicoAdicional):
            raise TypeError
        self.servico_adicional = obj_servico_adicional

        if not isinstance(ob_etiqueta, Etiqueta):
            raise TypeError
        self.etiquetas = ob_etiqueta

        self.cubagem = 0.0
        self.peso = 0
        # self.data_postagem = date()
        self.status_processamento = ''
        self.valor_cobrado = 0.0
        self.codigo_objeto_cliente = 0
        self.numero_comprovante_de_postagem = 0

    def get_xml(self):

        xml = u'<objeto_postal>'
        xml += u'<numero_etiqueta>%s</numero_etiqueta>' % \
               self.etiquetas.etiqueta_com_dig_verif
        xml += u'<codigo_objeto_cliente/>%s<codigo_objeto_cliente/>' % \
               self.codigo_objeto_cliente
        xml += u'<codigo_servico_postagem>%s</codigo_servico_postagem>' % \
               self.servico_postagem.codigo()
        xml += u'<cubagem>%s</cubagem>' % str(self.cubagem)
        xml += u'<peso>%d</peso>' % self.peso
        xml += u'<rt1/>'
        xml += u'<rt2/>'
        xml += self.destinatario.get_xml()
        xml += self.destino_nacional.get_xml()
        xml += self.servico_adicional.get_xml()
        xml += self.dimensao_objeto.get_xml()
        xml += u'<data_postagem_sara/>'
        xml += u'<status_processamento>%s</status_processamento>' % \
               self.status_processamento
        xml += u'<numero_comprovante_postagem>%d</numero_comprovante_postagem' \
               u'>' % self.numero_comprovante_de_postagem
        xml += u'<valor_cobrado>%s<valor_cobrado/>' % str(self.valor_cobrado)
        xml += u'</objeto_postal>'

        return xml

