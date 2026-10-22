# F4 — Testes com o cliente

**Baseline do formulário:** 1 a 4 semanas. **Teto de referência:** 4 (ver ⏳ **D4**).

| Item | Mín | Central | Máx |
|---|---|---|---|
| 4.1 Base | 1 | 1,5 | 2 |
| 4.2 RN crítica ⏳ **D2** | +0,5 | +0,5 | +1 |

✅ **Reunião 20/10:** o fator "cliente com pouca disponibilidade para validar" foi **removido**. Também saiu do script, de `leitura-prd.md` e de `insumos-e-perguntas.md`. Quem do cliente testa e aprova passa a ser conferido no **F0** (item 0.3: ninguém nomeado → parar e consultar).

✅ **Reunião 20/10:** a prática de **deploys parciais desde o início** (o cliente usa versões embrionárias nas revisões, na Vercel) está validada. Ela não muda o peso; é a premissa que torna a base do F4 possível.

---

## 4.1 Base

Sempre entra.

> 🔎 **Proposta:** hoje 2 fluxos e 12 fluxos testam no mesmo tempo. Sugestão: +0,25 no central a cada 4 fluxos acima de 4. **Até validar:** base fixa.

## 4.2 RN crítica

| Pergunta | Onde ler | Sem resposta |
|---|---|---|
| **O código do NTec calcula** valor em dinheiro, dose, dado clínico, prazo legal ou dado fiscal, e um erro causa dano ao usuário final? | Transcrições ("o sistema calcula a mensalidade", "a dose sai da tabela"). Na revalidação: RNs da PRD, 3.4 | `false`. Cálculo citado sem dizer quem calcula (o sistema ou o gateway/outro sistema) → `false` + pergunta em `a_confirmar` com `"troca": {"rn_critica": true}` |

**Não é RN crítica:** só repassar um valor para o gateway de pagamento, que é quem calcula e cobra. **É RN crítica:** o sistema calcula o valor da mensalidade com desconto proporcional, a dose de um medicamento, o prazo de uma multa.

**Relação com o F3:** quase sempre uma RN crítica também é RN específica no F3. **As duas somam**, porque medem coisas diferentes: o F3 mede o tempo de construir, o F4 mede o tempo de o cliente validar. É a única contagem dupla permitida.

> ⏳ **D2 — em aberto:** ✅ a reunião mandou **aumentar** o tempo de testes para regra de negócio crítica, sem dizer quanto. **Provisório:** valores atuais (0,5 / 0,5 / 1). 🔎 Sugestão: 1 / 1 / 1,5.

---

## Teto

> ⏳ **D4 — em aberto:** com o fator de disponibilidade removido, a soma só passa de 4 se a D2 subir muito a RN crítica. **Provisório:** manter a soma e marcar ⚠️. Não cortar.
