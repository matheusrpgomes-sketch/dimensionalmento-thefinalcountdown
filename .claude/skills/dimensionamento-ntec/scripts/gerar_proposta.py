"""Gera a Proposta Técnica do NTec em Markdown, no template oficial do núcleo.

Uso:
    python gerar_proposta.py proposta.json [--saida PASTA]

A entrada é um JSON com as 14 seções do template e o bloco `dimensionamento`
(ver `proposta-tecnica.md` e `exemplos/ficticio-petagenda-proposta.json`).
A faixa de semanas NÃO é digitada: o script roda `calcular_faixa.calcular`
sobre `dimensionamento.entrada`, para que a proposta e a régua nunca divirjam.

Saída: "[Proposta Técnica] {projeto}.md" e, no terminal, a faixa e o
resultado do checklist final do template.

Desde 22/10/2026 a saída é só Markdown (antes era PDF com reportlab), e a
entrada padrão são as transcrições das reuniões de diagnóstico + o protótipo
navegável. A PRD vem depois da assinatura do contrato e não é pré-requisito.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from calcular_faixa import EntradaInvalida, calcular, fmt, parte_a_confirmar, semanas, sinal, sprints  # noqa: E402

OBRIGATORIAS = {4, 6, 8, 10, 11, 14}
STATUS = {
    "pronto": "✅ Pronto para proposta",
    "atencao": "⚠️ Precisa de revisão da área de projetos",
    "preliminar": "⚠️ Estimativa preliminar: faltam transcrições ou protótipo",
    "parado": "🚩 Parado: restrição técnica ou possível inviabilidade",
}


def cel(t):
    """Texto seguro para célula de tabela Markdown."""
    return str(t if t is not None else "").replace("|", "\\|").replace("\n", " ")


def tabela(cab, linhas):
    out = ["| " + " | ".join(cel(c) for c in cab) + " |", "|" + "---|" * len(cab)]
    out += ["| " + " | ".join(cel(c) for c in l) + " |" for l in linhas]
    return "\n".join(out)


def bullets(itens):
    return "\n".join(f"- {i}" for i in itens)


def titulo(n, texto):
    selo = " `OBRIGATÓRIO`" if n in OBRIGATORIAS else ""
    return f"## {n}. {texto}{selo}" if n else f"## {texto}"


def rotulados(pares):
    return "\n\n".join(f"**{r}:** {t}" for r, t in pares)


def vazio(v):
    return v in (None, "", [], {})


# ---------------------------------------------------------------- checklist
def checklist(d, r):
    cab = d.get("cabecalho", {})
    proto = d.get("prototipo", {})
    itens = []
    itens.append((
        "Transcrições das reuniões de diagnóstico e protótipo navegável anexados",
        not vazio(cab.get("transcricoes")) and bool(cab.get("prototipo_link")),
    ))
    obrig = {
        4: d.get("perfis", {}).get("tabela"), 6: d.get("regras"), 8: d.get("seguranca"),
        10: d.get("roadmap"), 11: d.get("pontos_abertos"), 14: proto.get("tabela") or proto.get("declaracao"),
    }
    itens.append(("Todos os campos OBRIGATÓRIO preenchidos", all(not vazio(v) for v in obrig.values())))
    itens.append((
        "Protótipo segue as regras de negócio das reuniões — ou as adaptações estão justificadas e claras "
        "para o MVP (seção 14)",
        bool(proto.get("recebido")) and not vazio(obrig[14]),
    ))
    cron = " ".join(str(s[1]) for s in d.get("cronograma", {}).get("sprints", [])).lower()
    fora = [l[1] for l in d.get("roadmap", []) if str(l[2]).lower() != "prioritário"]
    itens.append(("Roadmap e cronograma não se contradizem", not any(str(e).lower() in cron for e in fora)))
    itens.append((
        "Pontos em aberto (seção 11) listados explicitamente, não escondidos no meio do texto",
        not vazio(d.get("pontos_abertos")),
    ))
    itens.append((
        "Nenhuma dependência externa (API, fornecedor) tratada como certa sem confirmação",
        not d.get("dependencia_externa_sem_confirmacao", False),
    ))
    return itens


# ---------------------------------------------------------------- documento
def montar(d, r):
    s = []
    cab = d.get("cabecalho", {})
    dim = d.get("dimensionamento", {})
    projeto = d.get("projeto", dim.get("entrada", {}).get("projeto", "Projeto"))
    venda = sprints(r["provavel"]) * 2
    parte = parte_a_confirmar(r)
    parte = f" **{parte}** (seção 11)" if parte else ""

    s.append(f"# Proposta Técnica — {projeto}")
    s.append("*Padrão de documentação · NTec · Comercial → Validação de Projeto*")
    s.append(
        f"> **Status do dimensionamento:** {STATUS.get(d.get('status', 'atencao'), STATUS['atencao'])}  \n"
        f"> **Prazo recomendado:** {venda} semanas ({venda // 2} sprints de 2 semanas){parte}, mais as semanas off. "
        f"Faixa: otimista {semanas(r['otimista'])} · provável {semanas(r['provavel'])} · "
        f"conservador {semanas(r['conservador'])} semanas. Detalhe no Anexo."
    )
    transcricoes = cab.get("transcricoes") or []
    s.append(
        "> **Insumos do dimensionamento: transcrições das reuniões de diagnóstico + protótipo navegável.**  \n"
        f"> Transcrições: {'; '.join(transcricoes) if transcricoes else 'não informadas'}  \n"
        f"> Protótipo: {cab.get('prototipo_link') or 'não informado'}  \n"
        f"> Documento de requisitos (PRD): {cab.get('prd_link') or 'gerado depois da assinatura, como anexo de contrato'}"
    )
    s.append(" · ".join([
        f"**Cliente/Projeto:** {cab.get('cliente_projeto', projeto)}",
        f"**Responsável comercial:** {cab.get('responsavel_comercial') or '______'}",
        f"**Data de envio:** {cab.get('data_envio') or '______'}",
    ]))

    # 1
    s.append(titulo(1, "Problema que a solução resolve"))
    pb = d.get("problema", {})
    if pb.get("dor"):
        s.append(pb["dor"])
    s.append(bullets(pb.get("problemas", [])))
    # 2
    s.append(titulo(2, "Visão geral e princípios da solução"))
    vg = d.get("visao_geral", {})
    s.append(rotulados([(k, vg[c]) for k, c in (("Tipo de aplicação", "tipo"), ("Público-alvo", "publico"),
                                                 ("Proposta de valor", "proposta_valor")) if vg.get(c)]))
    if vg.get("principios"):
        s.append(bullets(vg["principios"]))
    # 3
    s.append(titulo(3, "Entidades principais do sistema"))
    en = d.get("entidades", {})
    s.append(rotulados([("Centrais", en.get("centrais", "")), ("De apoio", en.get("apoio", ""))]))
    # 4
    s.append(titulo(4, "Perfis de acesso"))
    pf = d.get("perfis", {})
    s.append(tabela(["Perfil", "O que faz", "Observações de permissão"], pf.get("tabela", [])))
    if pf.get("matriz_permissoes"):
        s.append(f"**Matriz de permissões por ação:** {pf['matriz_permissoes']}")
    # 5
    s.append(titulo(5, "Fluxo completo, etapa por etapa"))
    linhas = []
    for i, e in enumerate(d.get("fluxo", []), 1):
        etapa = e.get("etapa", "")
        if e.get("pendente"):
            etapa += f" **[Decisão futura do cliente: {e['pendente']}]**"
        linhas.append([i, etapa, e.get("quem", ""), e.get("dados", ""), e.get("validacoes", "")])
    s.append(tabela(["#", "O que acontece", "Quem faz", "Dados que entram/saem", "Validações"], linhas))
    # 6
    s.append(titulo(6, "Regras de negócio"))
    s.append(tabela(["Regra", "O que garante"], d.get("regras", [])))
    # 7
    s.append(titulo(7, "Arquitetura / como o sistema é construído"))
    s.append(rotulados(d.get("arquitetura", [])))
    # 8
    s.append(titulo(8, "Segurança, dados e rastreabilidade"))
    s.append(rotulados(d.get("seguranca", [])))
    # 9
    s.append(titulo(9, "Módulos críticos (pagamentos, integrações externas, automações)"))
    mods = d.get("modulos_criticos", [])
    if not mods:
        s.append("Não há módulo crítico de pagamento, integração externa ou automação no escopo.")
    for m in mods:
        bloco = [f"### {m.get('nome', '')}", bullets(m.get("detalhe", []))]
        extra = rotulados([(k, m[c]) for k, c in (("Entra no MVP", "mvp"),
                                                   ("Futuro / dependente de terceiro", "futuro")) if m.get(c)])
        if extra:
            bloco.append(extra)
        s.append("\n\n".join(bloco))
    # 10
    s.append(titulo(10, "Roadmap — MVP vs. futuro"))
    s.append(tabela(["Fase", "Entrega", "Natureza"], d.get("roadmap", [])))
    # 11
    s.append(titulo(11, "Pontos em aberto para validação conjunta"))
    s.append(bullets(d["pontos_abertos"]) if d.get("pontos_abertos") else "**Alerta:** nenhum ponto em aberto listado.")
    if r["a_confirmar"]:
        s.append("**Perguntas que mudam o prazo** (fora do prazo recomendado; calculadas pela régua):")
        s.append(tabela(["#", "O que ficou ambíguo", "Pergunta para o cliente", "Se sim"], [
            [n, p["o_que"], p["pergunta"],
             f"{sinal(p['venda'])} semanas na venda" + (" · 🚩 vira parada" if p["paradas"] else "")]
            for n, p in enumerate(r["a_confirmar"], 1)]))
    # 12
    s.append(titulo(12, "Stack de execução proposta"))
    st = d.get("stack", {})
    s.append(rotulados(st.get("itens", [])))
    if st.get("nao_validado"):
        s.append("**Ainda não validado:**\n\n" + bullets(st["nao_validado"]))
    # 13
    s.append(titulo(13, "Cronograma sprint a sprint"))
    cr = d.get("cronograma", {})
    linhas = [[x[0], x[1] + (f" **[depende de: {x[2]}]**" if len(x) > 2 and x[2] else "")]
              for x in cr.get("sprints", [])]
    s.append(tabela(["Sprint", "Entregas previstas"], linhas))
    s.append(f"**Duração total:** {venda} semanas, {venda // 2} sprints de 2 semanas"
             f"{', ' + cr['duracao_obs'] if cr.get('duracao_obs') else ''}.")
    # 14
    s.append(titulo(14, "Protótipo × regras de negócio"))
    pr = d.get("prototipo", {})
    if pr.get("tabela"):
        s.append(tabela(["Tela/fluxo", "Regra (reuniões)", "Adaptação no protótipo", "Justificativa",
                         "Vale para o MVP?"], pr["tabela"]))
    if pr.get("declaracao"):
        s.append(pr["declaracao"])
    if not pr.get("recebido"):
        s.append("> ⚠️ **Protótipo não recebido pela skill.** O comercial precisa anexar o protótipo navegável e "
                 "preencher esta seção antes de enviar para a validação.")

    # checklist
    s.append(titulo(0, "Checklist final antes de enviar (comercial)"))
    s.append("\n".join(f"- [{'x' if ok else ' '}] {'' if ok else '**PENDENTE** · '}{texto}"
                       for texto, ok in checklist(d, r)))

    # anexo
    s.append(titulo(0, "Anexo — Memória do dimensionamento (para a validação técnica)"))
    s.append("*Calculado com a skill dimensionamento-ntec sobre as transcrições das reuniões e o protótipo. "
             "Sem buffer percentual: o risco está no intervalo mínimo / central / máximo de cada fase. "
             "Semanas off e garantia de 30 dias ficam fora da faixa.*")
    s.append("### Faixa de semanas")
    s.append(tabela(["Cenário", "Semanas", "Sprints", "Quando acontece"], [
        ["Otimista (piso)", semanas(r["otimista"]), sprints(r["otimista"]),
         "Escopo congelado, cliente responde rápido. Não vender abaixo disto."],
        ["**Provável (recomendado)**", f"**{semanas(r['provavel'])}**", f"**{sprints(r['provavel'])}**",
         "O que costuma acontecer no NTec."],
        ["Conservador (teto de risco)", semanas(r["conservador"]), sprints(r["conservador"]),
         "Se os pontos em aberto e os riscos se confirmarem."],
    ]))
    s.append("### Detalhamento por fase")
    crit = dim.get("criterios", {})
    linhas = [[nome, fmt(a), fmt(b), fmt(c), crit.get(nome.split()[0], "")]
              for nome, (a, b, c) in r["fases"].items()]
    linhas.append(["**Total**", f"**{fmt(r['otimista'])}**", f"**{fmt(r['provavel'])}**",
                   f"**{fmt(r['conservador'])}**", f"Fator de formato no desenvolvimento: {r['fator_formato_detalhe']}"])
    s.append(tabela(["Fase", "Mín", "Central", "Máx", "Critério"], linhas))
    if r["paradas"] or r["alertas"]:
        s.append("### Alertas da régua")
        s.append(bullets([f"🚩 **PARADO:** {p}" for p in r["paradas"]] + r["alertas"]))
    if dim.get("atencao"):
        s.append("### Pontos de atenção")
        s.append(bullets(dim["atencao"]))
    if dim.get("lacunas"):
        s.append("### Lacunas para o CN")
        s.append(tabela(["Fator", "Procurado e não achado", "Pergunta para o cliente", "Valor provisório"],
                        dim["lacunas"]))
    if dim.get("inventario_prototipo"):
        s.append("### Inventário de telas do protótipo")
        s.append(tabela(["Tela / rota", "Perfil", "O que faz", "Dados", "Ações", "Citada em"],
                        dim["inventario_prototipo"]))
    if dim.get("precedente"):
        s.append("### Precedente")
        s.append(dim["precedente"])
    if dim.get("cortes"):
        s.append("### O que cortar")
        s.append(tabela(["Corte", "Economia estimada"], dim["cortes"]))
    for rot, chave in (("Suposições", "suposicoes"), ("Ajustes de fronteira", "fronteira"),
                       ("Pontos para a imersão", "imersao")):
        if dim.get(chave):
            s.append(f"### {rot}")
            s.append(bullets(dim[chave]))
    return "\n\n".join(x for x in s if x) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("proposta")
    ap.add_argument("--saida", default=None, help="pasta do .md (padrão: a pasta do JSON)")
    a = ap.parse_args()
    with open(a.proposta, encoding="utf-8") as f:
        d = json.load(f)
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    entrada = d.get("dimensionamento", {}).get("entrada")
    if not entrada:
        sys.exit("Erro: falta dimensionamento.entrada (o JSON da régua).")
    try:
        r = calcular(entrada)
    except EntradaInvalida as erro:
        sys.exit(f"Erro em dimensionamento.entrada: {erro}")
    if r["rejeicoes"]:
        motivos = "\n  - ".join(r["rejeicoes"])
        sys.exit(f"REJEITADO NO F0, nenhuma proposta gerada:\n  - {motivos}\n"
                 "Responder ao CN com o critério, a citação e o que precisaria mudar (fatores/F0-viabilidade.md).")
    projeto = d.get("projeto", entrada.get("projeto", "Projeto"))
    pasta = a.saida or os.path.dirname(os.path.abspath(a.proposta))
    os.makedirs(pasta, exist_ok=True)
    destino = os.path.join(pasta, f"[Proposta Técnica] {projeto}.md")
    with open(destino, "w", encoding="utf-8") as f:
        f.write(montar(d, r))

    venda = sprints(r["provavel"]) * 2
    parte = parte_a_confirmar(r)
    print(f"Proposta: {destino}")
    print(f"Faixa: otimista {semanas(r['otimista'])} · provável {semanas(r['provavel'])} · "
          f"conservador {semanas(r['conservador'])} · vender {venda} semanas ({venda // 2} sprints)")
    if parte:
        print(f"  {parte}")
    print("Checklist:")
    for texto, ok in checklist(d, r):
        print(f"  [{'x' if ok else ' '}] {texto}")
    if r["paradas"]:
        print("PARADO:", *r["paradas"], sep="\n  - ")
    if r["avisos_internos"]:
        print("Avisos da revisão da régua (fora da proposta):", *r["avisos_internos"], sep="\n  - ")


if __name__ == "__main__":
    main()
