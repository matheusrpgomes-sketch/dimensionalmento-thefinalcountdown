# Projeto D — app de ciência cidadã

**Situação:** em execução, sem atraso (47,6% do prazo em 16/10/2026). **Vendido:** 18 semanas (+3 off), 9 sprints planejadas.

> ⚠️ **Ficha incompleta.** O levantamento recebido foi cortado no meio da ficha deste projeto. Os fatores abaixo marcados como *palpite* precisam ser conferidos no hand-off.

## O que era
O cidadão registra avistagens de espécies com foto e geolocalização. App nativo nas lojas + painel admin web + landing com mapa. Cliente do terceiro setor (ONG ou instituto).

## Como a régua classificou

| Fator | Classificação | Origem |
|---|---|---|
| Formato | App nativo + web (painel e landing, código separado) → x1,3 | hand-off |
| Níveis de acesso | cidadão, admin (talvez pesquisador) → 2 a 6 com poucas diferenças | **palpite** |
| Fluxos comuns | 5: registrar avistagem (foto + localização), mapa público, moderação pelo admin, catálogo de espécies, histórico do usuário | **palpite** |
| Integrações | mapa (uni, doc); upload de foto (S3) = template | **palpite** |
| Offline | não (**a conferir**: uso em campo pode precisar) | **palpite** |
| Lojas | app comum | hand-off |

## Resultado da régua

_Recalculado em 22/10/2026 com a régua atual; conferido por `scripts/testar_exemplos.py`._

| Fase | Mín | Central | Máx |
|---|---|---|---|
| F1 Imersão e setup | 1,5 | 2 | 2,5 |
| F2 Acesso e login | 0,5 | 1 | 1,5 |
| F3 Desenvolvimento — compartilhado x1,4 (5 fluxos) | 7,5 | 9,25 | 11,5 |
| F4 Testes com cliente | 1 | 1,5 | 2 |
| F5 Deploy | 0,5 | 1 | 1,5 |
| F6 Lojas | 2 | 2,5 | 4 |
| **Faixa** | **13** | **18** | **23** |

## Vendido × realizado
- **Recomendação de venda da régua = vendido (18).** Sem atraso até agora: 6 de 9 sprints abertas.
- Resultado final: a confirmar.

## Lição para a régua
Se o hand-off mostrar que o app precisa funcionar **offline com sincronização** (comum em uso de campo), a régua soma +2 no central (faixa 15 / 20 / 26, recomendação de venda 20). Vale como alerta para futuros apps de campo: perguntar sempre.
