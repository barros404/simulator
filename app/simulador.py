from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import date, datetime
from .models import (
    CAUtilizador,
    PVPlanoPagamentoSob,
    PVSeguradoSIG,
    PVBeneficario,
    PVPagamentoSob
)

# ========================================
# Funções utilitárias
# ========================================

def parse_date_safe(date_value):
    if isinstance(date_value, date):
        return date_value
    if isinstance(date_value, datetime):
        return date_value.date()
    if isinstance(date_value, str):
        try:
            return datetime.strptime(date_value, "%Y-%m-%d").date()
        except ValueError:
            return None
    return None

def calcular_idade(data_nascimento: date, data_ref: date) -> int:
    if not data_nascimento or not data_ref:
        return None
    return data_ref.year - data_nascimento.year - (
        (data_ref.month, data_ref.day) < (data_nascimento.month, data_nascimento.day)
    )

# ========================================
# Verifica permissões
# ========================================

async def validar_permissao(session: AsyncSession, username: str, tipo_folha: str):
    query = select(CAUtilizador).where(CAUtilizador.USERNAME == username)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        return False, "Usuário não encontrado."
    if user.TECNICO_DPS != 'S':
        return False, "Usuário não tem permissão técnica."
    if user.APROVADOR not in [2, 3]:
        return False, "Usuário não tem permissão de aprovador."
    if tipo_folha == 'SOB' and user.FOLHA_SOB != 'S':
        return False, "Usuário não tem permissão para folha SOB."
    if tipo_folha == 'REF' and user.FOLHA_REF != 'S':
        return False, "Usuário não tem permissão para folha REF."

    return True, "Permissão validada."

# ========================================
# Obter beneficiários do plano ativos
# ========================================

async def listar_beneficiarios_plano(session: AsyncSession):
    query = select(
        PVPlanoPagamentoSob.id_beneficiario,
        PVPlanoPagamentoSob.id_segurado_fk,
        PVPlanoPagamentoSob.total_subsidio_titular,
        PVPlanoPagamentoSob.total_pensao_titular
    ).where(
        PVPlanoPagamentoSob.suspenso != 'S'
    )
    result = await session.execute(query)
    return result.all()

# ========================================
# Aplicar regras de filtro
# ========================================


async def processar_viuvas_menor_50(
    session: AsyncSession,
    viuvas: list[dict]
) -> list[dict]:
    """
    Retorna a lista de viúvas menores de 50 que devem permanecer na folha,
    considerando o número de pagamentos e filhos vinculados menores de idade.
    """
    ids_viuvas = [b["id_beneficiario"] for b in viuvas]
    ibans_viuvas = [b["Iban"] for b in viuvas]

    # Obter número de pagamentos
    query_pag = select(
        PVPagamentoSob.id_beneficiario,
        func.count().label("qtd_pagamentos")
    ).where(
        PVPagamentoSob.id_beneficiario.in_(ids_viuvas)
    ).group_by(
        PVPagamentoSob.id_beneficiario
    )
    result_pag = await session.execute(query_pag)
    pagamentos_data = {row.id_beneficiario: row.qtd_pagamentos for row in result_pag.fetchall()}

    # Obter filhos vinculados
    filhos_vinculados = await obter_filhos_vinculados(session, ibans_viuvas)

    # Filtrar viúvas que ainda devem entrar
    viuvas_filtradas = []
    for ben in viuvas:
        qtd_pag = pagamentos_data.get(ben["id_beneficiario"], 0)
        filhos_menores = any(
            idade is not None and idade <= 18
            for idade in filhos_vinculados.get(ben["Iban"], [])
        )

        if qtd_pag < 24 or filhos_menores:
            ben["qtd_pagamentos"] = qtd_pag
            viuvas_filtradas.append(ben)

    return viuvas_filtradas
async def obter_filhos_vinculados(session: AsyncSession, ibans: list[str]) -> dict:
    """
    Retorna um dicionário onde a chave é o IBAN e o valor é uma lista com idades atuais
    dos filhos vinculados (por IBAN) com até 18 anos.
    """
    query = select(
        PVBeneficario.Iban,
        PVBeneficario.data_nascimento
    ).where(
        PVBeneficario.Iban.in_(ibans)
    )
    result = await session.execute(query)

    vinculados = {}
    for row in result.fetchall():
        idade = calcular_idade(parse_date_safe(row.data_nascimento), date.today())
        if row.Iban not in vinculados:
            vinculados[row.Iban] = []
        vinculados[row.Iban].append(idade)

    return vinculados


async def filtrar_beneficiarios(session: AsyncSession, registros):
    ids_beneficiarios = {r.id_beneficiario for r in registros}
    ids_segurados = {r.id_segurado_fk for r in registros}

    # Obter dados
    ben_result = await session.execute(
        select(
            PVBeneficario.id_beneficiario,
            PVBeneficario.data_nascimento,
            PVBeneficario.id_grau_parentesco_fk,
            PVBeneficario.Iban
        ).where(PVBeneficario.id_beneficiario.in_(ids_beneficiarios))
    )
    seg_result = await session.execute(
        select(
            PVSeguradoSIG.id_segurado_Sig,
            PVSeguradoSIG.data_falecido
        ).where(PVSeguradoSIG.id_segurado_Sig.in_(ids_segurados))
    )

    ben_data = {
        row.id_beneficiario: {
            "nascimento": row.data_nascimento,
            "grau": row.id_grau_parentesco_fk,
            "iban": row.Iban
        } for row in ben_result.fetchall()
    }
    seg_data = {row.id_segurado_Sig: row.data_falecido for row in seg_result.fetchall()}

    beneficiarios_final = []
    viuvas_menor_50 = []

    for r in registros:
        ben = ben_data.get(r.id_beneficiario, {})
        grau = ben.get("grau")
        data_nasc = parse_date_safe(ben.get("nascimento"))
        data_morte = parse_date_safe(seg_data.get(r.id_segurado_fk))
        iban = ben.get("iban")

        item = {
            "id_beneficiario": r.id_beneficiario,
            "id_segurado_fk": r.id_segurado_fk,
            "total_subsidio_titular": float(r.total_subsidio_titular or 0),
            "total_pensao_titular": float(r.total_pensao_titular or 0),
            "id_grau_parentesco_fk": grau,
            "Iban": iban
        }

        if grau in [109, 108, 102, 101]:  # Viúvas
            idade_na_morte = calcular_idade(data_nasc, data_morte)
            item["idade_na_morte"] = idade_na_morte
            if idade_na_morte is not None and idade_na_morte < 50:
                viuvas_menor_50.append(item)
            else:
                beneficiarios_final.append(item)
        else:
            if grau in [103, 104, 105] and data_nasc:
                item["idade_actual"] = calcular_idade(data_nasc, date.today())
            beneficiarios_final.append(item)

    # 🟢 Chamada para função dedicada
    viuvas_validas = await processar_viuvas_menor_50(session, viuvas_menor_50)
    beneficiarios_final.extend(viuvas_validas)

    return beneficiarios_final

# ========================================
# Função principal
# ========================================

async def gerar_folha(session: AsyncSession, username: str, tipo_folha: str):
    # 1️⃣ Validar permissão
    permissao_ok, msg = await validar_permissao(session, username, tipo_folha)
    if not permissao_ok:
        return {"erro": msg}

    # 2️⃣ Listar beneficiários ativos no plano
    registros = await listar_beneficiarios_plano(session)
    if not registros:
        return {"dados": [], "msg": "Nenhum beneficiário ativo no plano."}

    # 3️⃣ Aplicar filtro (lógica completa)
    beneficiarios = await filtrar_beneficiarios(session, registros)

    # 4️⃣ Retornar resultado
    return {
        "dados": beneficiarios,
        "msg": f"{len(beneficiarios)} beneficiários válidos encontrados."
    }
