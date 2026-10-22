"""
Teste de regressão dos exemplos da régua NTec.

Roda calcular_faixa.py sobre cada exemplos/*.json e confere com exemplos/esperado.json:
otimista, provável e conservador (em semanas inteiras), a venda e a venda com todas as
perguntas em aberto. Confere também a tabela de exemplos/README.md, para que a faixa
mostrada aos CNs seja a mesma que o script calcula.

Uso:
    python scripts/testar_exemplos.py             # falha (saída 1) se algo mudou
    python scripts/testar_exemplos.py --atualizar # regrava esperado.json com a régua atual

Mudou um peso de propósito? Rode com --atualizar, confira a diferença no git e atualize a
tabela de exemplos/README.md e a ficha .md do exemplo.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from calcular_faixa import calcular, semanas, venda  # noqa: E402

EXEMPLOS = Path(__file__).resolve().parent.parent / "exemplos"
ESPERADO = EXEMPLOS / "esperado.json"


def entrada_de(arquivo):
    """A entrada da régua: o próprio JSON, ou o bloco dimensionamento.entrada de uma proposta."""
    dados = json.loads(arquivo.read_text(encoding="utf-8"))
    return dados["dimensionamento"]["entrada"] if "dimensionamento" in dados else dados


def resultado_de(entrada):
    r = calcular(entrada)
    if r["rejeicoes"]:
        return {"rejeitado": True}
    return {
        "otimista": semanas(r["otimista"]),
        "provavel": semanas(r["provavel"]),
        "conservador": semanas(r["conservador"]),
        "venda": venda(r["provavel"]),
        "venda_com_todas": r["venda_com_todas"],
    }


def faixas_do_readme():
    """{arquivo.json: "9 / 12 / 16"} a partir da tabela de exemplos/README.md."""
    faixas = {}
    for linha in (EXEMPLOS / "README.md").read_text(encoding="utf-8").splitlines():
        link = re.match(r"\| \[[^\]]+\]\(([^)]+)\) \|", linha)
        if not link:
            continue
        celulas = [c.strip() for c in linha.strip("|").split("|")]
        faixa = next((c for c in celulas if re.fullmatch(r"\d+ / \d+ / \d+", c)), None)
        if faixa:
            faixas[Path(link.group(1)).with_suffix(".json").name] = faixa
    return faixas


def main():
    atual = {a.name: resultado_de(entrada_de(a))
             for a in sorted(EXEMPLOS.glob("*.json")) if a.name != ESPERADO.name}

    if "--atualizar" in sys.argv:
        ESPERADO.write_text(json.dumps(atual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{ESPERADO.name} regravado com {len(atual)} exemplos.")
        return 0

    esperado = json.loads(ESPERADO.read_text(encoding="utf-8"))
    erros = []
    for nome in sorted(set(atual) | set(esperado)):
        if nome not in esperado:
            erros.append(f"{nome}: exemplo novo sem valor em {ESPERADO.name} (rode com --atualizar)")
        elif nome not in atual:
            erros.append(f"{nome}: está em {ESPERADO.name}, mas o arquivo não existe mais")
        elif atual[nome] != esperado[nome]:
            erros.append(f"{nome}: esperado {esperado[nome]}, calculado {atual[nome]}")

    for nome, faixa in faixas_do_readme().items():
        r = atual.get(nome)
        if r and not r.get("rejeitado"):
            calculada = f"{r['otimista']} / {r['provavel']} / {r['conservador']}"
            if faixa != calculada:
                erros.append(f"README.md, linha de {nome}: mostra {faixa}, o script calcula {calculada}")

    if erros:
        print("Exemplos divergentes:")
        for erro in erros:
            print(f"  - {erro}")
        return 1
    print(f"{len(atual)} exemplos conferidos, README.md incluído.")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
