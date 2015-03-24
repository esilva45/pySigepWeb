# -*- coding: utf-8 -*-
from suds import WebFault

from interface_servico import InterfaceServico
from ambiente import FabricaAmbiente
from consulta_cep_resposta import ConsultaCEPResposta
from usuario import Usuario


class ServicoAtendeCliente(InterfaceServico):

    AMBIENTE_PRODUCAO = FabricaAmbiente.AMBIENTE_PRODUCAO
    AMBIENTE_HOMOLOGACAO = FabricaAmbiente.AMBIENTE_HOMOLOGACAO

    GERADOR_ONLINE = True
    GERADOR_OFFLINE = False

    def __init__(self, nome_ambiente, obj_usuario):
        if not isinstance(obj_usuario, Usuario):
            raise TypeError

        self.obj_usuario = obj_usuario
        amb = FabricaAmbiente.get_ambiente(nome_ambiente)
        super(ServicoAtendeCliente, self).__init__(amb.url)

    def verifica_disponibilidade_servicos(self, lista_codigo_servicos,
                                          cep_origem, cep_destino):

        if not isinstance(lista_codigo_servicos, list):
            raise TypeError

        res = {}

        for codigo in lista_codigo_servicos:
            try:
                res[codigo] = self._service.verificaDisponibilidadeServico(
                    self.obj_usuario.codigo_admin, codigo, cep_origem,
                    cep_destino, self.obj_usuario.nome, self.obj_usuario.senha)
            except WebFault as exp:
                print exp.message

        return res

    def consulta_cep(self, cep):

        if not isinstance(cep, str):
            raise TypeError

        try:
            res = self._service.consultaCEP(cep)
            return ConsultaCEPResposta(res.bairro, res.cep, res.end, res.id,
                                       res.uf, res.complemento,
                                       res.complemento2)
        except WebFault as exp:
            print exp.message
            return None

    def consulta_status_cartao_postagem(self):
        try:
            status = self._service.getStatusCartaoPostagem(
                self.obj_usuario.num_cartao_postagem, self.obj_usuario.nome,
                self.obj_usuario.senha)
            return status
        except WebFault as exp:
            print exp.message
            return None

    def solicita_etiquetas(self, servico_id, qtd_etiquetas=1,
                           tipo_destinatario="C"):

        try:
            faixa_etiquetas = self._service.solicitaEtiquetas(
                tipo_destinatario, self.obj_usuario.cnpj, servico_id,
                qtd_etiquetas, self.obj_usuario.nome, self.obj_usuario.senha)

        except WebFault as exp:
            print exp.fault
            print '[ERRO] Em solicita_etiquetas(). ' + exp.message
            return None

        from etiqueta import Etiqueta

        etiqueta_inicial = faixa_etiquetas.split(',')[0]
        etiqueta_numero = int(etiqueta_inicial[2:10])
        etiqueta_prefixo = etiqueta_inicial[0:2]
        etiqueta_sufixo = etiqueta_inicial[10:]

        etiquetas = []

        for i in range(qtd_etiquetas):
            etq = Etiqueta()
            etq.etiqueta_sem_dig_verif = \
                etiqueta_prefixo + str(etiqueta_numero + i).zfill(8) +  \
                etiqueta_sufixo
            etiquetas.append(etq)

        return etiquetas

    def gera_digito_verificador_etiquetas(self, lista_etiquetas,
                                          gerador=GERADOR_ONLINE):

        if gerador == ServicoAtendeCliente.GERADOR_ONLINE:
            return self._gerador_online(lista_etiquetas)
        elif gerador == ServicoAtendeCliente.GERADOR_OFFLINE:
            return self._gerador_offline(lista_etiquetas)
        else:
            print u'[ERRO] Opção de gerador inválida!'
            return []

    def _gerador_online(self, lista_etiquetas):

        etq_str = ''

        for etq in lista_etiquetas:
            etq_str += etq + ','

        try:
            dig_verif_list = self._service.geraDigitoVerificadorEtiquetas(
                etq_str, self.obj_usuario.nome, self.obj_usuario.senha)
        except WebFault as exp:
            print exp.message
            return []

        return dig_verif_list

    @staticmethod
    def _gerador_offline(lista_etiquetas):

        from gerador_digito_verificador import GeradorDigitoVerificador

        dig_verif_list = []

        for i in range(len(lista_etiquetas)):
            dv = GeradorDigitoVerificador.gera_digito_verificador(
                lista_etiquetas[i].etiqueta_sem_dig_verif[2:10])
            dig_verif_list.append(dv)

        return dig_verif_list
