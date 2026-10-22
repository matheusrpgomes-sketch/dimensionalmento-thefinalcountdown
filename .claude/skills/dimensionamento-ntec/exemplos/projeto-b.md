# Projeto B — app clínico offline

**Situação:** em execução (45% do prazo em 16/10/2026). **Vendido:** 12 semanas (+1 off), 6 sprints.

## O que era
Calculadora clínica pediátrica que substitui a planilha usada hoje pela cliente. App nativo iOS e Android, publicado nas 2 lojas. Sem login, sem backend, sem banco: 100% offline com cálculo local. Cliente: profissional de saúde com plantões e pouca disponibilidade para validar.

## Como a régua classificou

| Fator | Classificação | Origem |
|---|---|---|
| Formato | App nativo | hand-off |
| Níveis de acesso | nenhum | hand-off |
| Fluxos | 1 jornada com RN específica (médico · calcula a prescrição · soro: faixas de peso, soluções, eletrólitos e alertas). Recontado em 22/10/2026: o antigo fluxo comum "interface e preferências" não é jornada, ninguém o pediu nas reuniões | T1 + protótipo |
| Offline | local, sem sincronizar → 0 | hand-off |
| RN crítica | sim: erro de cálculo é risco clínico | hand-off |
| Quem valida | a própria médica (cliente pessoa física) | T1 |
| Lojas | app sensível (saúde): revisão mais rigorosa | hand-off |

## Resultado da régua

_Recalculado em 22/10/2026 com a régua atual; conferido por `scripts/testar_exemplos.py`._

| Fase | Mín | Central | Máx |
|---|---|---|---|
| F1 Imersão e setup | 1,5 | 2 | 2,5 |
| F2 Acesso e login | 0 | 0 | 0 |
| F3 Desenvolvimento — app x1,2 (1 fluxo) | 2,4 | 3,6 | 4,8 |
| F4 Testes com cliente | 1,5 | 2 | 3 |
| F5 Deploy | 0,5 | 0,5 | 1 |
| F6 Lojas | 2,5 | 3 | 6 |
| **Faixa** | **9** | **12** | **18** |

## Vendido × planejado
Plano do hand-off: imersão (sem. 1–2), motor de cálculo em três etapas (3–6), interface e preferências (7–8), testes, deploy e lojas (9–12).

- Com a régua atual e a contagem por jornada, o vendido (12) é **igual à recomendação de venda (12)**. Pela régua antiga (1 + 1 fluxos), ficava entre o piso (11) e o provável (14).
- O próprio hand-off registrou os riscos: escopo real maior que o da ficha, prazo encolhido de 4 para 2–3 meses e "não se sustenta com só 1 dev".
- **Resultado final: a confirmar** quando o projeto terminar.

## Lição para a régua
1. **A ficha de qualificação subestimou o escopo** (variáveis clínicas e unidades que só apareceram depois). Por isso o "fluxo com RN específica" exige o documento da regra antes da proposta.
2. **A stack (Expo) foi sugestão comercial, sem validação do time** → regra "o CN não promete stack".
3. Testes, deploy e lojas de um app de saúde em 4 semanas está no limite inferior da régua (F4 + F5 + F6 no mínimo = 4,5).

## Ritmo com Claude Code (17/10/2026, histórico)

O projeto está sendo codado com Claude Code por uma dupla com cerca de 20 horas por semana somadas. Pelo git, o código começou em 30/09/2026 e, até 06/10, já tinha o motor das 3 faixas, a composição do soro, a tela completa com o modal de alerta e o hook ligando a tela ao motor. É quase todo o F3, que a régua antiga estimava em 5,1 semanas no central.

Esse dado criou o fator Claude Code, que **saiu da régua em 20/10/2026**. A recontagem por jornada (22/10/2026) chega ao mesmo vendido sem fator nenhum: 9 / 12 / 18, venda de 12 semanas.

## Rodada às cegas (22/10/2026)

Primeiro teste do caminho transcrições + protótipo num projeto real: a skill rodou só com a T1 (diagnóstico de 14/07, Fathom), o protótipo publicado no Lovable e a planilha da médica, sem o código nem o hand-off. Resultado: 1 jornada com RN específica, sem login, offline local, RN crítica e app sensível nas lojas → **9 / 12 / 18, vender 12 + até 2** (perguntas em aberto: login e forma de cobrança). A reunião de apresentação do protótipo (T2) não foi gravada.

Lições: as decisões sobre validador pessoa física, offline sem dado salvo, app clínico como sensível e versão do protótipo que vale saíram desta rodada e estão nos fatores.
