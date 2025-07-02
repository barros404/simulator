from sqlalchemy import Column, Integer, BigInteger, String, Date, DECIMAL, CHAR, VARCHAR, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Log(Base):
    __tablename__ = "log"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(String(255), nullable=False)
    criado_em = Column(DateTime, default=func.now())
class PVPlanoPagamentoSob(Base):
    __tablename__ = "pv_plano_pagamento_sob"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_beneficiario = Column(BigInteger, nullable=False)
    id_segurado_fk = Column(Integer, nullable=False)
    Nome = Column(String(40), nullable=False)
    data_nascimento = Column(Date)
    id_grau_parentesco_fk = Column(Integer)
    status = Column(String(9))
    total_subsidio_titular = Column(DECIMAL(15, 2))
    total_pensao_titular = Column(DECIMAL(15, 2), nullable=False)
    mes = Column(VARCHAR(2))
    ano = Column(VARCHAR(4))
    data = Column(Date, nullable=False)
    suspenso = Column(VARCHAR(1), nullable=False, default="N")
    motivo_suspensao = Column(VARCHAR(100))
    pago_suspenso = Column(VARCHAR(1), nullable=False, default="N")
    usuario = Column(VARCHAR(50), nullable=False)
    subsidio = Column(VARCHAR(2), nullable=False)

class CAUtilizador(Base):
    __tablename__ = "ca_utilizador"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    USERNAME = Column(VARCHAR(50), nullable=False)
    NOME = Column(VARCHAR(100), nullable=False)
    EMAIL = Column(VARCHAR(100))
    TELEFONE = Column(VARCHAR(25))
    CIDADE = Column(VARCHAR(100))
    ID_PROVINCIA = Column(Integer)
    ID_MUNICIPIO = Column(Integer)
    ID_PERFIL = Column(Integer)
    UNIDADE_ORGANICA = Column(VARCHAR(100), nullable=False)
    ACTIVO = Column(CHAR(1), nullable=False)
    DATA_INICIO = Column(Date)
    DATA_FIM = Column(Date)
    ID_AGENCIA_CPS = Column(Integer)
    APROVADOR = Column(Integer, nullable=False)
    JURIDICO = Column(CHAR(1), nullable=False)
    TIPO_PENSAO = Column(CHAR(1), nullable=False, default="N")
    ORGAO = Column(Integer, nullable=False)
    TECNICO = Column(CHAR(1), nullable=False)
    TECNICO_DPS = Column(CHAR(1), nullable=False)
    SIGLA_CARGO = Column(VARCHAR(4), nullable=False)
    CARGO = Column(VARCHAR(100), nullable=False)
    ADMIN = Column(CHAR(1), nullable=False, default="N")
    FICHA_INSC = Column(CHAR(1), nullable=False, default="N")
    RFC = Column(CHAR(1), nullable=False, default="N")
    PDV = Column(CHAR(1), nullable=False, default="N")
    ATENDIMENTO = Column(CHAR(1), nullable=False, default="N")
    PROCESSOS = Column(CHAR(1), nullable=False, default="N")
    RH = Column(CHAR(1), nullable=False, default="N")
    CARTOES = Column(CHAR(1), nullable=False, default="N")
    PORTA_SOCKET = Column(Integer)
    ARQUIVO = Column(CHAR(1), nullable=False)
    PLANO_REF = Column(CHAR(1), nullable=False)
    PLANO_RETRO = Column(CHAR(1), nullable=False)
    FOLHA_REF = Column(CHAR(1), nullable=False)
    REF_RETRO = Column(CHAR(1), nullable=False)
    RELATORIOS = Column(CHAR(1), nullable=False)
    SUB_MORTE = Column(CHAR(1), nullable=False)
    PLANO_SOB = Column(CHAR(1), nullable=False)
    FOLHA_SOB = Column(CHAR(1), nullable=False)
    FICHA_INSC_AUT = Column(CHAR(1), nullable=False)
    LANCAR_RETRO = Column(CHAR(1), nullable=False)
    id_acesso = Column(Integer)
    admin_pv = Column(CHAR(2))
    APROV_SOB = Column(VARCHAR(2), nullable=False)
    APROV_REF = Column(VARCHAR(2), nullable=False)
    ALTERAR_DOC = Column(VARCHAR(2), nullable=False)
    ELIMINAR_DEP = Column(VARCHAR(2), nullable=False)
    INSERCAO_FICHA = Column(VARCHAR(2), nullable=False)
    SIMULAR_FOLHA = Column(VARCHAR(2), nullable=False)
    REC_PENDENTES = Column(VARCHAR(2), nullable=False)
    INIC_RECALCULO = Column(VARCHAR(2), nullable=False)
    PV_REF_PENDENTE = Column(VARCHAR(2), nullable=False)
    PV_SOB_PENDENTE = Column(VARCHAR(2), nullable=False)
    ESTATISTICA = Column(VARCHAR(2), nullable=False)
    IMPOR_N_INSCRICAO = Column(CHAR(1), nullable=False)
    CARTAO_2_VIA = Column(CHAR(1), nullable=False)
    CARTAO_N_VIA = Column(VARCHAR(1), nullable=False)
    ID_REATIVAR_SOB = Column(VARCHAR(1), nullable=False)
    REATIVAR_SOB = Column(CHAR(1), nullable=False)
    SUSPENDER_SOB = Column(CHAR(1), nullable=False)
    VER_HISTORICO_DEP = Column(CHAR(1), nullable=False)
    IMPLANTAR_SOB_MORTE = Column(CHAR(1), nullable=False, default="N")
    SUSPENDER_SOB_MORTE = Column(CHAR(1), nullable=False, default="N")
    VER_HISTORICO_DE_IMPLANTACAO = Column(CHAR(1), nullable=False, default="N")
    ELIMINAR_FICHA = Column(CHAR(1), nullable=False, default="N")
    SOLICITAR_RECALCULO = Column(CHAR(1), nullable=False, default="N")
    REMOVER_ANOMALIA = Column(CHAR(1), nullable=False, default="N")


class PVSeguradoSIG(Base):
    __tablename__ = "pv_segurado_sig"

    id_segurado_Sig =Column(Integer, primary_key=True, autoincrement=True)
    data_falecido=Column(DateTime(), nullable=True)
    data_nascimento=Column(DateTime(), nullable=True)
    data_inicio_servico=Column(DateTime(), nullable=True)
    data_fim_servico=Column(DateTime(), nullable=True)
    data_inicio_pensao=Column(DateTime(), nullable=True)

class PVBeneficario(Base):
    __tablename__ = "pv_beneficiario"

    id_beneficiario  =Column(Integer, primary_key=True, autoincrement=True)
    id_segurado_fk = Column(Integer, nullable=False)
    Nome= Column(String(40), nullable=False)
    data_nascimento= Column(Date)
    id_grau_parentesco_fk = Column(Integer)
    Iban=Column(String(45), nullable=False)
    id_grau_academico_fk=Column(Integer, nullable=False)
    id_ensino_fk=Column(Integer, nullable=False)
    id_sexo_fk=Column(Integer, nullable=False)

class PVPagamentoSob(Base):
    __tablename__ = "pv_pagamento_sob"
    id_pagamento_sob = Column(Integer, primary_key=True, autoincrement=True)
    id_beneficiario = Column(BigInteger, nullable=False)
    id_segurado_fk = Column(Integer, nullable=False)
    mes = Column(VARCHAR(2), nullable=False)
    ano = Column(VARCHAR(4), nullable=False)
    data = Column(Date, default=func.now())
    total_subsidio_titular = Column(DECIMAL(15, 2), nullable=False)
    total_pensao_titular = Column(DECIMAL(15, 2), nullable=False)
    indice_fk = Column(Integer, nullable=False)
    subsidio = Column(VARCHAR(2), nullable=False)

class PVPagamentoSob(Base):
    __tablename__ = "pv_totais_pagamento_sob"
    pv_totais_pagamento_id  = Column(Integer, primary_key=True, autoincrement=True)
    mes = Column(VARCHAR(2), nullable=False)
    ano = Column(VARCHAR(4), nullable=False)
    data_plano_pag = Column(Date, default=func.now())
    usuario = Column(DECIMAL(15, 2), nullable=False)
    indice_fk = Column(Integer, nullable=False)
    fechada = Column(VARCHAR(2), nullable=False)

