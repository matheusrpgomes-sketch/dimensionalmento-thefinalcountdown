# F3 — Integrações

✅ **Reunião 20/10:** integrações são um tópico **separado** dos fluxos. Somam no F3 **depois** do fator de formato (não são multiplicadas por ele).

**Peso fixo, sem perguntar ao CN sobre documentação.** O CN não tem como avaliar a API de outro sistema. A linha sai de quatro perguntas sobre o que o cliente disse.

---

## O teste

Para **cada** sistema que o cliente nomeou nas reuniões ("integrar com o ERP", "puxar do Bling", "pagar com Pix"). **Onde ler:** transcrições. Botão do protótipo ("Pagar", "Enviar no WhatsApp") sem fala nas reuniões **não** é integração: vai para `a_confirmar`. Na revalidação, os itens SID da PRD.

**Integração citada de forma vaga** ("seria bom conversar com o sistema de lá", "quem sabe integrar"): não conta. Vai para `a_confirmar` com `"integracao"` na linha que ela teria pelas perguntas abaixo (sistema do cliente sem sentido claro → `bi_sem_doc`).

| # | Pergunta | Onde ler | Resultado |
|---|---|---|---|
| 0 | A troca de dados é **automática**, sem uma pessoa disparar? | Transcrições ("cai sozinho", "atualiza automático" × "a gente exporta e sobe") | Se **não** (uma pessoa importa ou exporta um arquivo): não é integração, é **dependência de dados** (`F3-desenvolvimento.md`) |
| 1 | É login com Google, envio de e-mail ou upload de arquivo? | Transcrições | `template` (0) |
| 2 | Alguma transcrição diz que o outro sistema **não tem API**? | Transcrições | **F0** — parar e consultar |
| 3 | O sistema **envia e recebe**? | Transcrições ("manda o pedido e recebe o status") | Sim → bidirecional. Só envia ou só recebe → unidirecional. Não dá para saber o sentido → bidirecional (classificação de um fator citado) |
| 4 | O outro lado é **serviço de mercado** (documentação pública **e** sandbox que o NTec acessa sozinho, sem a TI do cliente)? | Nome do serviço citado | Sim → `_doc`. Não, ou dúvida → `_sem_doc` |

**Exemplos de serviço de mercado:** Mercado Pago, Stripe, Pix via gateway, Google Maps, Mapbox, Expo Push / FCM, OpenAI / Anthropic, WhatsApp Business API, emissores de NF-e, Google Calendar, SMS.

**Caem em "sistema do cliente" (`_sem_doc`):** ERP, sistema legado, sistema sob medida e **SaaS em que o acesso depende da TI do cliente** (ex.: Totvs, Bling ou RD Station sem sandbox liberado ao NTec).

---

## Tabela

| Código | Linha | Mín | Central | Máx | Obrigatório na resposta |
|---|---|---|---|---|---|
| `template` | Google, e-mail, upload (S3) | 0 | 0 | 0 | |
| `uni_doc` | Unidirecional com serviço de mercado | +0,5 | +0,5 | +1 | |
| `bi_doc` | Bidirecional com serviço de mercado | +0,5 | +1 | +1,5 | |
| `uni_sem_doc` | Unidirecional com sistema do cliente | +1 | +1,5 | +2 | Cláusula + plano B |
| `bi_sem_doc` | Bidirecional com sistema do cliente ⏳ **D2** | **+4** | +4 | +5 | Cláusula + plano B |
| `sem_api` | Sistema sem API (uni ou bi) | — vai para o **F0** — | | | |

✅ **Reunião 20/10:** integração bidirecional com sistema do cliente (antes 1,5 / 2,5 / 3,5) **não pode custar menos de 4 semanas**, pelos riscos de depender da TI de outra empresa.

> ⏳ **D2 — em aberto:** o mínimo de `bi_sem_doc` é 4 (decidido). O central e o máximo não foram definidos. **Provisório:** 4 / 4 / 5. 🔎 Sugestão: 4 / 4,5 / 5,5.

> 🔎 **Proposta:** se o `bi_sem_doc` subiu de 2,5 para 4+ no central, o `uni_sem_doc` (1,5 no central) ficou desproporcional. Sugestão: 2 / 2,5 / 3. **Até validar:** 1 / 1,5 / 2.

---

## Casos comuns

| O cliente pediu | Linha |
|---|---|
| Pagamento (gateway, Pix, cartão) | `bi_doc`. `bi_sem_doc` só se o pagamento passar pelo sistema próprio do cliente |
| IA (classificar, extrair, gerar, responder) | `uni_doc`. Se a IA decide sem um humano no fim: ⚠️ em *Pontos de atenção* |
| Push no app | `uni_doc` |
| WhatsApp automático | `uni_doc`; `bi_doc` se o sistema lê a resposta. Link para abrir o WhatsApp = 0 |
| E-mail | `template` |
| Aviso dentro do sistema | 0 (faz parte do módulo) |

**Não contar duas vezes:** uma integração não vira também feature atípica.

---

## Toda integração com sistema do cliente leva, na resposta

**Cláusula de contrato** (em *Pontos de atenção*):
> "A integração com {sistema} depende de o cliente fornecer acesso à API e à documentação dela até o início da sprint {n}. Sem esse acesso, a integração será substituída por importação e exportação de planilha, sem alteração de prazo."

**Plano B** (em *O que cortar*): trocar a integração por importação ou exportação manual de planilha. A economia em semanas é recalculada pelo script.

## Origem na resposta

```
Integração ERP Totvs: bidirecional com sistema do cliente (origem: T1 · 00:22:10 — "manda o pedido pro Totvs e volta a nota" + acesso depende da TI do cliente)
Integração Mercado Pago: bidirecional com serviço de mercado (origem: T2 · 00:08:45 — "o cliente paga no Pix pelo app")
```
