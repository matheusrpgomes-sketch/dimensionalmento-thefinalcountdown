# F5 — Deploy

**Baseline do formulário:** 1 a 4 semanas. **Sem teto definido** (🔎 Proposta: usar 4, como F1, F2 e F4).

| Item | Mín | Central | Máx |
|---|---|---|---|
| 5.1 Tem web ou PWA (infra do NTec, ex.: Vercel) | 0,5 | 0,5 | 1 |
| 5.2 Tem app nativo, sem web | 0,5 | 0,5 | 1 |
| 5.3 Tem app nativo junto com web | +0 | +0,5 | +0,5 |
| 5.4 Infra do cliente | +1 | +1 | +2 |

Os itens 5.1 a 5.3 saem direto do formato (`F3-desenvolvimento.md`, item 3.2). Não há pergunta.

**Deploys parciais** (✅ Reunião 20/10): o time publica versões parciais desde a primeira sprint. Por isso o F5 é curto: ele cobre só a publicação final, domínio e ajustes de produção.

**Publicação nas lojas não é F5:** é F6.

---

## 5.4 Infra do cliente

É `true` se **qualquer** pergunta for sim:

| Pergunta | Onde ler | Sem resposta |
|---|---|---|
| A conta de nuvem ou o servidor onde o sistema vai rodar é **do cliente**? | Transcrições ("nossos servidores", "a nossa TI hospeda", "tem que ficar na nossa AWS"). Na revalidação: PRD 3.1 | `false` (infra do NTec) + pergunta em `a_confirmar`: "O sistema vai ficar nos servidores ou na nuvem do cliente?", com `"troca": {"deploy_infra_cliente": true}` |
| A TI do cliente precisa **aprovar cada publicação**, ou exige um pipeline de deploy próprio? | Transcrições | `false` (vale a mesma pergunta acima) |

Infra do cliente **sem acesso do time do NTec** para publicar e corrigir → **F0**, 📝 ajuste de contrato (desde 22/10/2026 **não rejeita**): o projeto perde a garantia de 30 dias e o contrato diz isso. O F5 continua com 5.4 = `true`.

**Alerta:** pedir os acessos e as regras de deploy do cliente **já na imersão**.
