"""Calcula a faixa de semanas de um projeto do NTec a partir dos fatores F0 a F6.

Uso:
    python calcular_faixa.py entrada.json

A entrada é um JSON com os fatores levantados (ver `fatores/*.md` e os exemplos
em `exemplos/*.json`). A saída é o F0 (viabilidade), o detalhamento por fase em
(mínimo / central / máximo) e a faixa final: otimista, provável e conservador.

Nenhum fator tem valor padrão: campo ausente ou com valor desconhecido faz a
conta parar com erro, para que nunca entre a linha mais leve por esquecimento.

Os pesos daqui são a fonte da verdade da Régua. Se mudar um número aqui,
mude também no arquivo do fator em `fatores/` (e vice-versa).

Revisão de 21/10/2026 (reunião de validação de 20/10/2026): F0 criado, fator
Claude Code e "cliente com pouca disponibilidade" removidos, F2 em duas tabelas
(2 a 5 e 6+), formato extra e `bi_sem_doc` revistos, tetos não cortam mais.
As decisões em aberto (D1 a D5, `fatores/README.md`) usam o valor provisório.

Revisão de 22/10/2026 (dimensionamento do Projeto G, primeiro projeto com PRD de dois
níveis): fator de formato por fluxo (`fluxos_por_formato`): cada fluxo recebe o
fator do código em que existe, e o formato extra só pesa nos fluxos que existem
em mais de um código. Publicação nas lojas pode ser lacuna do Fathom ("+").

Revisão de 22/10/2026 (reunião "Validação Entregas Tec"): a entrada padrão passa a
ser as transcrições das reuniões de diagnóstico + o protótipo navegável (a PRD vem
depois do contrato). F0: multa por atraso sai (não existe nos contratos do NTec);
SLA/suporte 24/7 e infra do cliente sem acesso deixam de rejeitar e viram avisos de
contrato; multitenancy com regra por tenant é parada obrigatória.
"""

import json
import math
import sys

# (mínimo, central, máximo) em semanas

# F1 — fatores/F1-imersao-setup.md
F1_BASE = (1.5, 2, 2.5)
F1_DEMANDA_POUCO_DETALHADA = (0.5, 1, 1)
F1_ATIPICO = (0.5, 0.5, 1)
F1_STACK_FORA_TEMPLATE = (1, 1.5, 2)  # troca de stack aceita no F0 (ex.: Mongo → Supabase)
F1_TETO = 4

# F2 — fatores/F2-acesso-multitenancy.md. Sem fator Claude Code desde 20/10/2026.
F2_NIVEIS = {
    "nenhum": (0, 0, 0),
    "1": (0.5, 0.5, 1),
    "2-5-poucas": (0.5, 1, 1.5),
    "2-5-grandes": (1.5, 2, 2.5),  # D2: provisório, a reunião mandou aumentar
    "6+": (2.5, 3, 4),
}
F2_MULTITENANCY = {
    "nao": (0, 0, 0),
    "separado": (0.5, 0.5, 1),
    "isolado": (1, 1.5, 2),  # D2: provisório, a reunião mandou aumentar
    "instancias": (0, 0, 0),  # F0: não dimensiona, para
}
F2_TETO = 4

# F3 — fatores/F3-desenvolvimento.md e fatores/F3-integracoes.md. Sem fator Claude Code.
F3_FLUXO_COMUM = (1, 1.25, 1.5)
F3_FLUXO_RN = (2, 3, 4)
F3_FEATURE_ATIPICA = (1, 1.5, 2)
F3_FORMATO = {"web": 1.0, "pwa": 1.1, "app": 1.2}
F3_FORMATO_EXTRA = 0.2  # D1: provisório (+0,2 por formato extra; antes +0,1). Só nos fluxos "compartilhado"
F3_COMPARTILHADO = "compartilhado"  # chave de `fluxos_por_formato` para fluxo que existe em mais de um código
F3_TIPOS_FLUXO = {"comuns": "fluxos_comuns", "rn_especifica": "fluxos_rn_especifica", "atipicas": "features_atipicas"}
F3_INTEGRACAO = {
    "template": (0, 0, 0),
    "uni_doc": (0.5, 0.5, 1),
    "bi_doc": (0.5, 1, 1.5),
    "uni_sem_doc": (1, 1.5, 2),
    "bi_sem_doc": (4, 4, 5),  # mínimo 4 decidido em 20/10; central e máximo: D2 provisório
    "sem_api": (0, 0, 0),  # F0: não dimensiona, para
}
F3_DEPENDENCIA_DADOS = (1, 1.5, 2)
F3_OFFLINE = {"nao": (0, 0, 0), "local": (0, 0, 0), "sync": (1.5, 2, 3)}
F3_VOLUME_ALTO = (1, 1.5, 2)
F3_MARGEM = 0.0  # D3: margem de segurança sobre o F3, provisório 0 (a reunião pediu margem explícita)

# F4 — fatores/F4-testes.md. "Cliente com pouca disponibilidade" removido em 20/10/2026.
F4_BASE = (1, 1.5, 2)
F4_RN_CRITICA = (0.5, 0.5, 1)  # D2: provisório, a reunião mandou aumentar
F4_TETO = 4

# F5 — fatores/F5-deploy.md
F5_WEB = (0.5, 0.5, 1)
F5_APP_SOZINHO = (0.5, 0.5, 1)
F5_APP_JUNTO_WEB = (0, 0.5, 0.5)
F5_INFRA_CLIENTE = (1, 1, 2)

# F6 — fatores/F6-lojas.md
F6_LOJAS = {"nao": (0, 0, 0), "normal": (2, 2.5, 4), "sensivel": (2.5, 3, 6)}

PROVAVEL_CALIBRADO_ATE = 26  # acima disso a régua ainda não foi calibrada

# F0 — fatores/F0-viabilidade.md. Rejeita: a skill não dimensiona.
F0_REJEICOES = {
    "stack_exigida_fora_da_lista": "O cliente exige uma tecnologia fora da lista aceita pelo NTec.",
    "offline_sync_com_mongodb_exigido": "Offline com sincronização exigido em MongoDB: só se vende com Postgres.",
}
# F0 — Ajustam o contrato, não rejeitam nem param (reunião de 22/10/2026). Viram alerta.
F0_CONTRATO = {
    "sla_ou_sustentacao": "Suporte 24/7, SLA ou sustentação além da garantia de 30 dias: fica fora deste prazo e "
                          "vai para um contrato de manutenção à parte.",
    "infra_cliente_sem_acesso": "Roda na infra do cliente sem acesso do time do NTec: o projeto perde a garantia "
                                "de 30 dias e o contrato precisa dizer isso.",
}
# F0 — Parar e consultar a área de projetos: a skill dimensiona, mas o status é 🚩.
F0_PARADAS = {
    "sem_validador_nomeado": "Ninguém do cliente foi nomeado para testar e aprovar as entregas.",
    "feature_sem_referencia_nem_doc": "Feature sem referência e sem documentação técnica pública: pode exigir prova de conceito paga.",
    "hardware": "O produto depende de hardware (Bluetooth com dispositivo próprio, IoT, leitor, impressora fiscal).",
}

F0_REMOVIDOS = {"multa_por_atraso": "critério removido em 22/10/2026 (o NTec não tem multa por atraso)"}

# Campos obrigatórios e valores aceitos. Nenhum tem padrão.
OPCOES = {
    "niveis_acesso": set(F2_NIVEIS),
    "multitenancy": set(F2_MULTITENANCY),
    "offline": set(F3_OFFLINE),
    "lojas": set(F6_LOJAS),
}
BOOLEANOS = [
    "demanda_pouco_detalhada", "atipico", "stack_fora_template", "dependencia_dados",
    "volume_alto", "rn_critica", "deploy_infra_cliente",
]
CONTAGENS = ["fluxos_comuns", "fluxos_rn_especifica", "features_atipicas"]
RENOMEADOS = {
    "2-6-baixa": "2-5-poucas (ou 6+ se forem 6 perfis)",
    "2-6-alta": "2-5-grandes (ou 6+ se forem 6 perfis)",
    "webapp": "pwa (se instala pelo navegador) ou web",
}
REMOVIDOS = {
    "claude_code": "fator Claude Code removido em 20/10/2026",
    "cliente_pouca_disponibilidade": "fator removido em 20/10/2026 (quem valida vai para o F0)",
}

# Fatores que nem as transcrições nem o protótipo responderam (leitura-transcricoes-prototipo.md).
# O nome `lacunas_fathom` ficou por compatibilidade: Fathom = as transcrições das reuniões.
# Lacuna entra na conta com o valor mais pesado; a parte da venda que depende dela aparece
# com "+" ("vender 14 semanas = 12 + 2 que dependem de confirmar com o cliente").
LACUNAS_FATHOM = {
    "atipico": "referência de produto",
    "stack_fora_template": "tecnologia exigida",
    "deploy_infra_cliente": "servidores do cliente",
    "lojas": "publicação nas lojas",
}
# Valor leve de cada lacuna: com ele o script refaz a conta para mostrar o "+".
LACUNAS_LEVE = {"atipico": False, "stack_fora_template": False, "deploy_infra_cliente": False, "lojas": "nao"}


class EntradaInvalida(ValueError):
    pass


def validar_f0(e):
    """Confere só o bloco F0. Roda antes do resto para que uma rejeição não exija preencher F1 a F6."""
    erros = []
    f0 = e.get("f0")
    if not isinstance(f0, dict):
        erros.append("f0: ausente (bloco de viabilidade, ver fatores/F0-viabilidade.md)")
    else:
        for campo in [*F0_REJEICOES, *F0_CONTRATO, *F0_PARADAS]:
            if not isinstance(f0.get(campo), bool):
                erros.append(f"f0.{campo}: ausente ou não é true/false")
        for campo, motivo in F0_REMOVIDOS.items():
            if campo in f0:
                erros.append(f"f0.{campo}: tirar do JSON ({motivo})")
        prazo = f0.get("prazo_exigido_semanas", "ausente")
        if prazo is not None and (isinstance(prazo, bool) or not isinstance(prazo, (int, float))):
            erros.append("f0.prazo_exigido_semanas: ausente (usar null se o cliente não exigiu prazo)")
        elif prazo is not None and prazo <= 0:
            erros.append("f0.prazo_exigido_semanas: tem de ser maior que 0 (usar null se não houver prazo)")
    if erros:
        raise EntradaInvalida("Entrada incompleta ou inválida:\n  - " + "\n  - ".join(erros))


def validar(e):
    """Confere que todo fator de F1 a F6 foi preenchido com um valor conhecido. Nunca assume o leve."""
    erros = []

    def opcao(campo, valor, aceitos):
        if valor in RENOMEADOS:
            erros.append(f"{campo}: '{valor}' não existe mais, usar {RENOMEADOS[valor]}")
        elif valor not in aceitos:
            erros.append(f"{campo}: '{valor}' não é um destes: {', '.join(sorted(aceitos))}")

    for campo, aceitos in OPCOES.items():
        if campo not in e:
            erros.append(f"{campo}: ausente")
        else:
            opcao(campo, e[campo], aceitos)
    for campo in BOOLEANOS:
        if not isinstance(e.get(campo), bool):
            erros.append(f"{campo}: ausente ou não é true/false")
    for campo in CONTAGENS:
        if not isinstance(e.get(campo), int) or isinstance(e.get(campo), bool) or e[campo] < 0:
            erros.append(f"{campo}: ausente ou não é um inteiro >= 0")
    if not isinstance(e.get("formatos"), list) or not e["formatos"]:
        erros.append("formatos: ausente ou vazio")
    else:
        for f in e["formatos"]:
            opcao("formatos", f, set(F3_FORMATO))
        if len(set(map(str, e["formatos"]))) < len(e["formatos"]):
            erros.append("formatos: formato repetido (cada formato entra uma vez)")
    if not isinstance(e.get("integracoes"), list):
        erros.append("integracoes: ausente (usar [] se não houver)")
    else:
        for i in e["integracoes"]:
            opcao("integracoes", i, set(F3_INTEGRACAO))
    for campo, motivo in REMOVIDOS.items():
        if campo in e:
            erros.append(f"{campo}: tirar do JSON ({motivo})")
    if not erros:
        erros += validar_fluxos_por_formato(e)
    if erros:
        raise EntradaInvalida("Entrada incompleta ou inválida:\n  - " + "\n  - ".join(erros))


def validar_fluxos_por_formato(e):
    """Com mais de um formato, cada fluxo diz em que código existe (fatores/F3-desenvolvimento.md, 3.2)."""
    erros = []
    formatos = e["formatos"]
    dist = e.get("fluxos_por_formato")
    if len(formatos) == 1:
        if dist is not None:
            erros.append("fluxos_por_formato: só se usa com mais de um formato (tirar do JSON)")
        return erros
    if not isinstance(dist, dict):
        return ["fluxos_por_formato: ausente. Com mais de um formato, dizer em que código cada fluxo existe: "
                f"chaves {', '.join(formatos)} e '{F3_COMPARTILHADO}' (fluxo que existe em mais de um código), "
                "cada uma com {\"comuns\", \"rn_especifica\", \"atipicas\"}"]
    aceitas = set(formatos) | {F3_COMPARTILHADO}
    for chave, cont in dist.items():
        if chave not in aceitas:
            erros.append(f"fluxos_por_formato.{chave}: não é um destes: {', '.join(sorted(aceitas))}")
            continue
        if not isinstance(cont, dict) or set(cont) != set(F3_TIPOS_FLUXO):
            erros.append(f"fluxos_por_formato.{chave}: precisa ter exatamente comuns, rn_especifica e atipicas")
            continue
        for tipo, v in cont.items():
            if not isinstance(v, int) or isinstance(v, bool) or v < 0:
                erros.append(f"fluxos_por_formato.{chave}.{tipo}: não é um inteiro >= 0")
    if erros:
        return erros
    for tipo, total in F3_TIPOS_FLUXO.items():
        s = sum(cont[tipo] for cont in dist.values())
        if s != e[total]:
            erros.append(f"fluxos_por_formato: soma de '{tipo}' é {s}, mas {total} é {e[total]}")
    return erros


def soma(*partes):
    return tuple(sum(p[i] for p in partes) for i in range(3))


def vezes(parte, n):
    return tuple(v * n for v in parte)


def teto(nome, parte, limite, alertas):
    """D4 (provisório): passar do teto não corta a soma, só marca para revisão."""
    if parte[2] > limite:
        alertas.append(f"{nome} passou do teto de {limite} semanas ({fmt(parte[2])} no máximo): "
                       "revisar com a área de projetos (a soma foi mantida, não cortada).")
    return parte


def calcular(e):
    # F0 — Viabilidade. Rejeição responde antes de exigir o resto da entrada.
    validar_f0(e)
    f0 = e["f0"]
    rejeicoes = [msg for campo, msg in F0_REJEICOES.items() if f0[campo]]
    paradas = [msg for campo, msg in F0_PARADAS.items() if f0[campo]]
    if rejeicoes:
        return {"rejeicoes": rejeicoes, "paradas": paradas, "alertas": [], "avisos_internos": []}

    validar(e)
    alertas = [msg for campo, msg in F0_CONTRATO.items() if f0[campo]]
    # Avisos para quem mantém a régua (decisões em aberto). Saem no terminal, não na proposta.
    avisos_internos = []
    if e["multitenancy"] == "instancias":
        paradas.append("Multitenancy com código ou regra de negócio diferente por cliente: parada obrigatória, "
                       "o NTec não suporta essa arquitetura. Não vender sem a área de projetos.")
    if "sem_api" in e["integracoes"]:
        paradas.append("Integração com sistema que, segundo as transcrições, não tem API: avaliar alternativa (planilha); "
                       "potencial motivo de inviabilidade.")

    # F1 — Imersão, refinamento, setup e acessos
    f1 = [F1_BASE]
    if e["demanda_pouco_detalhada"]:
        f1.append(F1_DEMANDA_POUCO_DETALHADA)
        alertas.append("Demanda pouco detalhada: recomendar ao comercial uma fase de discovery antes da proposta.")
    if e["atipico"]:
        f1.append(F1_ATIPICO)
        alertas.append("Produto atípico: pedir benchmark ou referência antes de fechar o prazo.")
    if e["stack_fora_template"]:
        f1.append(F1_STACK_FORA_TEMPLATE)
        alertas.append("Troca de stack aceita no F0: confirmar com a área de projetos se o time domina.")
        if "stack_fora_template" in e.get("lacunas_fathom", []):
            alertas.append("Tecnologia exigida ainda não confirmada: se estiver fora da lista aceita, o projeto "
                           "é rejeitado no F0 (fatores/F0-viabilidade.md), não só mais lento.")
    f1 = teto("F1 (imersão e setup)", soma(*f1), F1_TETO, alertas)

    # F2 — F2a níveis de acesso + F2b multitenancy
    niveis, multi = e["niveis_acesso"], e["multitenancy"]
    if niveis == "6+":
        alertas.append("6+ níveis de acesso: complexidade alta, confirmar se todos são mesmo necessários no MVP.")
    if multi == "isolado":
        alertas.append("Multitenancy com isolamento de dados: complexidade média/alta.")
    f2 = teto("F2 (acesso e multitenancy)", soma(F2_NIVEIS[niveis], F2_MULTITENANCY[multi]), F2_TETO, alertas)

    # F3 — Desenvolvimento
    formatos = e["formatos"]
    # Fator por fluxo: o fluxo recebe o fator do código em que existe. O formato extra (D1) só pesa
    # nos fluxos que existem em mais de um código ("compartilhado"). Um formato só: todos os fluxos nele.
    fator_compartilhado = max(F3_FORMATO[f] for f in formatos) + F3_FORMATO_EXTRA * (len(formatos) - 1)
    if len(formatos) == 1:
        dist = {formatos[0]: {t: e[c] for t, c in F3_TIPOS_FLUXO.items()}}
    else:
        dist = e["fluxos_por_formato"]
    nucleo_bruto, nucleo, detalhe = (0, 0, 0), (0, 0, 0), []
    for chave, cont in dist.items():
        f = fator_compartilhado if chave == F3_COMPARTILHADO else F3_FORMATO[chave]
        parte = soma(
            vezes(F3_FLUXO_COMUM, cont["comuns"]),
            vezes(F3_FLUXO_RN, cont["rn_especifica"]),
            vezes(F3_FEATURE_ATIPICA, cont["atipicas"]),
        )
        nucleo_bruto = soma(nucleo_bruto, parte)
        nucleo = soma(nucleo, vezes(parte, f))
        n = sum(cont.values())
        if n:
            detalhe.append(f"{chave} x{fmt(f)} ({n} {'fluxo' if n == 1 else 'fluxos'})")
    fator = nucleo[1] / nucleo_bruto[1] if nucleo_bruto[1] else fator_compartilhado
    if e["features_atipicas"]:
        alertas.append("Feature atípica: validar se é possível e se existe benchmark (pode exigir prova de conceito).")

    integracoes = e["integracoes"]
    extras = [F3_INTEGRACAO[i] for i in integracoes]
    if any(i in ("uni_sem_doc", "bi_sem_doc") for i in integracoes):
        alertas.append("Integração com sistema do cliente: incluir a cláusula de contrato (acesso à API até o início "
                       "da sprint; sem acesso, vira planilha) e o plano B em 'O que cortar'.")
    if e["dependencia_dados"]:
        extras.append(F3_DEPENDENCIA_DADOS)
        alertas.append("Dependência de dados de bases soltas: chamar o núcleo de Dados para avaliar.")
    extras.append(F3_OFFLINE[e["offline"]])
    if e["offline"] == "sync":
        alertas.append("Offline com sincronização: banco em Postgres, não MongoDB (premissa da Sprint de Refino).")
        avisos_internos.append("D5 em aberto: a troca para Postgres por causa do sync não soma no F1.")
    if e["volume_alto"]:
        extras.append(F3_VOLUME_ALTO)
        alertas.append("Volume de uso alto: requisitos de performance precisam estar escritos.")
    f3 = vezes(soma(nucleo, *extras), 1 + F3_MARGEM)
    if not F3_MARGEM:
        avisos_internos.append("D3 em aberto: margem de segurança 0, a faixa não tem margem extra.")

    # F4 — Testes com o cliente
    f4 = [F4_BASE]
    if e["rn_critica"]:
        f4.append(F4_RN_CRITICA)
    f4 = teto("F4 (testes)", soma(*f4), F4_TETO, alertas)

    # F5 — Deploy
    tem_web = any(f in ("web", "pwa") for f in formatos)
    tem_app = "app" in formatos
    f5 = []
    if tem_web:
        f5.append(F5_WEB)
    if tem_app:
        f5.append(F5_APP_JUNTO_WEB if tem_web else F5_APP_SOZINHO)
    if e["deploy_infra_cliente"]:
        f5.append(F5_INFRA_CLIENTE)
        alertas.append("Deploy na infra do cliente: pedir as regras de deploy e os acessos já na imersão.")
    f5 = soma(*f5)

    # F6 — Publicação nas lojas
    lojas = e["lojas"]
    if tem_app and lojas == "nao":
        alertas.append("Tem app nativo mas as lojas não foram marcadas: confirmar se o cliente quer publicar.")
    if lojas != "nao" and not tem_app:
        alertas.append("Lojas marcadas sem app nativo: só app nativo vai para a loja (fatores/F6-lojas.md).")
    f6 = F6_LOJAS[lojas]

    fases = {
        "F1 Imersão, refinamento e setup": f1,
        "F2 Infra, níveis de acesso e login": f2,
        "F3 Desenvolvimento": f3,
        "F4 Testes com o cliente": f4,
        "F5 Deploy": f5,
        "F6 Publicação nas lojas": f6,
    }
    total = soma(*fases.values())

    otimista, provavel, conservador = total
    if provavel > PROVAVEL_CALIBRADO_ATE:
        alertas.append(
            f"Provável acima de {PROVAVEL_CALIBRADO_ATE} semanas: fora da faixa calibrada da régua; "
            "validar com a área de projetos e considerar quebrar em fases."
        )
    prazo = f0["prazo_exigido_semanas"]
    if prazo is not None and prazo < otimista:
        paradas.append(f"O cliente exige {fmt(prazo)} semanas, abaixo do otimista ({fmt(otimista)}): "
                       "não vender sem a área de projetos.")

    # Parte da venda que depende das lacunas (o que as transcrições e o protótipo não responderam) (em sprints inteiras)
    lacunas = [k for k in e.get("lacunas_fathom", []) if k in LACUNAS_FATHOM and e[k] != LACUNAS_LEVE[k]]
    venda_confirmada = None
    if lacunas:
        confirmada = dict(e, lacunas_fathom=[], **{k: LACUNAS_LEVE[k] for k in lacunas})
        venda_confirmada = venda(calcular(confirmada)["provavel"])

    return {
        "fases": fases,
        "fator_formato": fator,
        "fator_formato_detalhe": " · ".join(detalhe) or f"x{fmt(fator)}",
        "otimista": otimista,
        "provavel": provavel,
        "conservador": conservador,
        "alertas": alertas,
        "avisos_internos": avisos_internos,
        "paradas": paradas,
        "rejeicoes": [],
        "lacunas_na_conta": lacunas,
        "venda_confirmada": venda_confirmada,
    }


def semanas(v):
    return math.ceil(v - 1e-9)


def sprints(v):
    return math.ceil(semanas(v) / 2)


def venda(provavel):
    """Recomendação de venda: o provável fechado em sprints inteiras de 2 semanas."""
    return sprints(provavel) * 2


def parte_lacunas(e, r):
    """Complemento da venda com as lacunas ("= 12 + 2 que dependem de confirmar com o cliente (...)"), ou ""."""
    v, vc = venda(r["provavel"]), r.get("venda_confirmada")
    if vc is None or vc >= v:
        return ""
    nomes = ", ".join(LACUNAS_FATHOM[k] for k in r["lacunas_na_conta"])
    return f"= {vc} + {v - vc} que dependem de confirmar com o cliente ({nomes})"


def fmt(v):
    return f"{v:.2f}".rstrip("0").rstrip(".").replace(".", ",")


def imprimir(e, r):
    print(f"# Projeto {e.get('projeto', '?')}\n")
    if r["rejeicoes"]:
        print("🚫 REJEITADO NO F0 — não dimensionar:")
        for p in r["rejeicoes"]:
            print(f"  - {p}")
        print("\nResponder ao CN com o critério, a citação e o que precisaria mudar (fatores/F0-viabilidade.md).")
        return
    if r["paradas"]:
        print("🚩 PARADO — não vender até a área de projetos avaliar:")
        for p in r["paradas"]:
            print(f"  - {p}")
        print()
    print("| Fase | Mín | Central | Máx |")
    print("|---|---|---|---|")
    for nome, (a, b, c) in r["fases"].items():
        print(f"| {nome} | {fmt(a)} | {fmt(b)} | {fmt(c)} |")
    print(f"\nFator de formato no desenvolvimento: {r['fator_formato_detalhe']} "
          f"(médio x{fmt(round(r['fator_formato'], 2))})\n")
    print("| Cenário | Semanas | Sprints (2 sem) |")
    print("|---|---|---|")
    rotulos = {
        "otimista": "Otimista (piso)",
        "provavel": "Provável (recomendado)",
        "conservador": "Conservador (teto de risco)",
    }
    for nome, rotulo in rotulos.items():
        v = r[nome]
        print(f"| {rotulo} | {semanas(v)} ({fmt(round(v, 2))}) | {sprints(v)} |")
    v = venda(r["provavel"])
    parte = parte_lacunas(e, r)
    print(f"\nRecomendação de venda: {v} semanas ({v // 2} sprints){' ' + parte if parte else ''}, "
          "mais as semanas off do calendário.")
    if r["alertas"]:
        print("\nAlertas:")
        for a in r["alertas"]:
            print(f"  - {a}")
    if r["avisos_internos"]:
        print("\nAvisos da revisão da régua (não vão para a proposta):")
        for a in r["avisos_internos"]:
            print(f"  - {a}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as f:
        entrada = json.load(f)
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        resultado = calcular(entrada)
    except EntradaInvalida as erro:
        print(erro)
        sys.exit(2)
    imprimir(entrada, resultado)
    if resultado["rejeicoes"]:
        sys.exit(1)
