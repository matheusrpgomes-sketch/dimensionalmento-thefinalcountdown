# Projeto C — plataforma de saúde (web + app)

**Situação:** entregue, com atraso registrado na base. **Vendido:** 11 semanas (+2 off). **Realizado:** 6 sprints (~14 semanas), com "terminar os testes" ainda não iniciada.

## O que era
Calcula um índice científico a partir de diários preenchidos pelo usuário e cruza o resultado com um questionário validado. Dashboard web + app do usuário final (testado no Expo; a publicação nas lojas não foi encontrada). Clientes do meio acadêmico, com orçamento curto. O escopo foi reescopado 2 vezes antes do contrato para caber no orçamento.

## Como a régua classificou

| Fator | Classificação | Origem |
|---|---|---|
| Formato | Web + app (2 códigos) → x1,3 | kick-off, planning S5 |
| Níveis de acesso | 5 perfis (dois níveis de admin, profissionais de duas áreas e paciente); um perfil profissional tem cadastro pendente/rejeitado que bloqueia rotas → 2 a 6 com grandes diferenças | plannings S1 e S5 |
| Fluxos | 3 comuns (diário, questionário, gestão e dashboards por perfil) + 1 com RN específica (cálculo do índice, "100% fidedigno", mínimo de 7 registros) | hand-off; contagem de fluxos = palpite |
| Dependência de dados | base pública de referência + importação e exportação de CSV, com conversão de unidades | plannings S2–S4 |
| RN crítica | sim (fórmula científica das clientes) | hand-off |
| Atípico | **não**: o que é incomum é a fórmula, já contada como RN específica | regra "atípico ≠ RN" |
| Lojas | não (só mapeamento na S5) | planning S5 |

## Resultado da régua

_Recalculado em 22/10/2026 com a régua atual; conferido por `scripts/testar_exemplos.py`._

| Fase | Mín | Central | Máx |
|---|---|---|---|
| F1 Imersão e setup | 1,5 | 2 | 2,5 |
| F2 Acesso e login | 1,5 | 2 | 2,5 |
| F3 Desenvolvimento — compartilhado x1,4 (4 fluxos) | 8 | 10,95 | 13,9 |
| F4 Testes com cliente | 1,5 | 2 | 3 |
| F5 Deploy | 0,5 | 1 | 1,5 |
| **Faixa** | **13** | **18** | **24** |

## Vendido × realizado
- **Vendido (11) abaixo do piso da régua (13).** O projeto atrasou (~14 semanas) e ainda ficou com os testes por terminar.
- No real, setup e login andaram juntos na S1 (~2 semanas, aproveitando o monorepo template), o desenvolvimento ocupou S2–S5 (~9 semanas, com deploy web na S3) e a entrega ficou na S6 (1 semana).
- Conclusão das sprints: S1 Over, S2 Under (base externa e CSV não iniciados), S3 Delivery, S4 e S5 Over, S6 Delivery.

## Lição para a régua
1. **Vender abaixo do piso atrasa.** O caso mais claro da base.
2. **Viés conhecido da régua:** o provável (18) ficou ~3 semanas acima do realizado (~14 + testes pendentes), porque o time juntou setup e login. Não corrigido com um único projeto. Se outros projetos repetirem o padrão, reduzir F1 + F2 quando o template for usado sem mudanças.
3. Os dados externos foram justamente a sprint em *Underdelivery* → o fator "dependência de dados" se justifica.
4. Retro S1: codar na main, cuidado com IA, dailies faltando. As outras retros estão vazias, então a causa do atraso não foi registrada.
