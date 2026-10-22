# Fatores de dimensionamento — NTec

Um arquivo por fator, na ordem em que a skill aplica. Substituem as seções F1 a F6 de `regua-dimensionamento.md` e criam o F0. Os termos em **negrito** estão definidos em `glossario.md`, que vale para todos os arquivos. Se um arquivo e o glossário divergirem, vale o glossário.

Origem: reunião "Validação Skill NTec" (20/10/2026) e análise do LLM Council (21/10/2026).

| Arquivo | Fase | O que decide |
|---|---|---|
| `glossario.md` | — | Definição única de cada termo |
| `F0-viabilidade.md` | Antes de tudo | Se o projeto pode ser dimensionado ou é rejeitado |
| `F1-imersao-setup.md` | F1 | Imersão, refinamento, setup e o alerta de discovery |
| `F2-acesso-multitenancy.md` | F2 | Níveis de acesso (F2a) e multitenancy (F2b), em tabelas separadas |
| `F3-desenvolvimento.md` | F3 | Fluxos, formato e extras (dados, offline, volume) |
| `F3-integracoes.md` | F3 | Integrações, separadas dos fluxos |
| `F4-testes.md` | F4 | Testes com o cliente |
| `F5-deploy.md` | F5 | Deploy |
| `F6-lojas.md` | F6 | Publicação nas lojas |

---

## Como cada critério está escrito

Todo critério segue o mesmo formato, para que o Claude não precise interpretar adjetivo:

| Campo | O que é |
|---|---|
| **Pergunta** | Sim ou não. Nunca "muito", "pouco", "grande" |
| **Onde ler** | A fala da transcrição (ou a tela do protótipo) que responde. A seção da PRD aparece só como "na revalidação" |
| **Sem resposta** | O valor que vai na venda e a pergunta que vai para `a_confirmar`. A tabela única do silêncio está em `leitura-transcricoes-prototipo.md`, Passo 4 |

**Entrada padrão desde 22/10/2026: transcrições + protótipo.** A PRD só entra na revalidação, depois do contrato.

**Regra de citação (revista em 22/10/2026):** o valor que vai para a venda precisa de citação. O que não tem citação **não** sobe para a linha mais pesada: fica no valor do silêncio (Passo 4 de `leitura-transcricoes-prototipo.md`) e vira pergunta em `a_confirmar`, que o script calcula **fora** da venda ("vender 14 + até 4"). A linha mais pesada só vale para **classificar** um fator que foi citado e encaixa em duas linhas (`regra-fronteira-e-faixa.md`).

**Regra de campo vazio:** nenhum fator tem valor padrão. Se um campo do JSON não foi preenchido, a conta não roda.

---

## Marcações usadas nos arquivos

| Marca | Significa |
|---|---|
| ✅ **Reunião 20/10** | Decidido na reunião de validação |
| 🔎 **Proposta** | Sugerido pelo Council, ainda não validado pela área técnica. Revisar com Augusto e Frank |
| ⏳ **D1 … D5** | Decisão em aberto: o número ou a regra depende do time. Até decidir, a skill usa o valor indicado como *provisório* |

**Como a skill trata uma 🔎 Proposta enquanto não é validada:**
- Se a proposta **define um critério** (uma pergunta, um limite, o que entra em cada linha), a skill já usa.
- Se a proposta **muda um peso** (um número da tabela), a skill usa o valor de **"Até validar"**, que é sempre o valor atual.

## Decisões em aberto

| # | Decisão | Onde aparece | Provisório até decidir |
|---|---|---|---|
| **D1** | "Formato extra pelo menos 1,2" é **+0,2 por formato extra** (app + web = 1,4) ou **×1,2 sobre o fator** (app + web = 1,44)? Desde 22/10/2026 vale só para fluxos `compartilhado` (com tela em mais de um código) | `F3-desenvolvimento.md` | +0,2 por formato extra |
| **D2** | Novos valores para as linhas que a reunião mandou aumentar sem dizer quanto: "2 a 5 com grandes diferenças" (F2a), "isolado" (F2b), "RN crítica" (F4) e central/máximo do `bi_sem_doc` (mínimo já é 4) | `F2-acesso-multitenancy.md`, `F4-testes.md`, `F3-integracoes.md` | Valores atuais, com sugestão ao lado |
| **D3** | Margem de segurança ("gordura") explícita: percentual sobre o F3, sobre o total, ou embutida nos centrais? Quanto? | `F3-desenvolvimento.md` | Sem margem extra (como hoje) e aviso na resposta |
| **D4** | Quando a soma de uma fase passa do teto: **manter a soma e marcar ⚠️** ou **parar** para a área de projetos? | `F1`, `F2`, `F4` | Manter a soma e marcar ⚠️ (não cortar) |
| **D5** | Offline com sincronização exige Postgres (não MongoDB). Isso **soma como stack fora do template** no F1, ou é só premissa da Sprint de Refino? | `F0-viabilidade.md`, `F1-imersao-setup.md`, `F3-desenvolvimento.md` | Só premissa, sem peso no F1 |

## O que ainda não foi feito

- `calcular_faixa.py` já segue estes arquivos (21/10/2026). O F0 está no bloco `"f0"` do JSON. Nenhum campo tem padrão. As decisões D1–D5 estão nas constantes marcadas com `D1`…`D5`.
- O texto de `exemplos/*.md` e o exemplo `ficticio-petagenda-proposta.json` (cronograma com 9 sprints, feito com o fator Claude Code) ainda mostram os números antigos.
- `SKILL.md`, `regua-dimensionamento.md`, `leitura-prd.md` e `insumos-e-perguntas.md` já apontam para cá (21/10/2026). `regra-fronteira-e-faixa.md` ainda cita as regras antigas.
- **Teste de concordância** (🔎 Proposta): antes de adotar, aplicar estes critérios aos Projetos A, B, C e D com 2 CNs e o Claude, sem um ver a classificação do outro, e conferir onde divergem.
