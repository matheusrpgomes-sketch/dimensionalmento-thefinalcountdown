# Proposta Técnica — como preencher o template do NTec

O entregável da skill é a **Proposta Técnica** no template oficial do NTec ("Comercial → Validação de Projeto"). É o documento que o comercial manda para a validação técnica. A skill monta um JSON e roda `scripts/gerar_proposta.py`, que gera **"[Proposta Técnica] {projeto}.md"** (Markdown, desde 22/10/2026; antes era PDF): caixa de status no topo, selo `OBRIGATÓRIO` nas seções que o template exige, as 14 seções, o checklist final e um **Anexo — Memória do dimensionamento**.

Modelo completo do JSON: `exemplos/ficticio-petagenda-proposta.json`.

## Regras do preenchimento

- **Fonte de tudo são as transcrições das reuniões de diagnóstico e o protótipo navegável**, mais o CN no chat (`leitura-transcricoes-prototipo.md`). A proposta não acrescenta jornada, perfil, integração, log ou permissão que ninguém citou e que o protótipo não mostra. Se o template pede algo que não apareceu, escrever "não citado nas reuniões". Se isso muda o prazo, vira ponto em aberto (seção 11).
- **A PRD não é pré-requisito.** Ela vem depois da assinatura do contrato. Se já existir, entra só como conferência.
- **As semanas não são digitadas.** O script recalcula a faixa a partir de `dimensionamento.entrada`, que é o mesmo JSON da régua (`calcular_faixa.py`). Caixa de status, cronograma e anexo saem do mesmo cálculo.
- **Perguntas em aberto fora do prazo.** Com `a_confirmar` na entrada, a caixa de status mostra a venda com "+ até" ("14 semanas + até 4 que dependem de 3 perguntas em aberto"), e a seção 11 ganha a tabela "Perguntas que mudam o prazo", com o custo de cada uma calculado pelo script. O cronograma segue só a venda (sem as perguntas). Com pergunta em aberto, `status` é `atencao`.
- **Nada interno no corpo** (seções 1 a 14): sem `(origem: ...)`, marcação de tempo da transcrição nem nome de arquivo da régua. As origens ficam no anexo (critérios, suposições, inventário de telas) e no chat.
- **Texto curto e sem adjetivo de venda.** Todo termo técnico é explicado na primeira vez que aparece.

## Cabeçalho (`cabecalho`)

| Campo | De onde vem |
|---|---|
| `cliente_projeto` | Nome do produto + subtítulo ("PetAgenda · Agenda e carteirinha de vacina para rede de clínicas veterinárias") |
| `responsavel_comercial`, `data_envio` | Do CN. Sem resposta: deixar `""`, e a proposta sai com `______` para preencher à mão |
| `transcricoes` | Lista com uma linha por reunião: nome e data (`"Diagnóstico 1 — 03/03 (Fathom)"`) |
| `prototipo_link` | Link do protótipo navegável (ou "prints enviados pelo CN", "código exportado"). Sem protótipo, fica `""` e o checklist sai PENDENTE |
| `prd_link` | Opcional. Vazio = "gerado depois da assinatura, como anexo de contrato" |

`status`: `pronto`, `atencao`, `preliminar` (faltam transcrições ou protótipo) ou `parado`.

## Seção por seção

| Seção | Campo no JSON | Como preencher |
|---|---|---|
| 1. Problema | `problema.dor`, `problema.problemas` (2 a 4) | A dor que o cliente descreveu nas reuniões. Cada problema é uma dor concreta que uma jornada resolve |
| 2. Visão geral | `visao_geral.tipo`, `publico`, `proposta_valor`, `principios` | Formato (da transcrição) e quem usa; proposta de valor em 1 frase; princípios = regras de arquitetura ditas pelo cliente (offline-first, mobile-first) |
| 3. Entidades | `entidades.centrais`, `entidades.apoio` | Os substantivos das telas do protótipo e das falas. Centrais = o que a jornada principal produz; apoio = cadastros e registros auxiliares |
| 4. Perfis **(obrig.)** | `perfis.tabela` (`[perfil, o que faz, observações]`), `perfis.matriz_permissoes` | Perfis do protótipo (menus, troca de perfil) e das falas. Observação = em que código vive, o que só ele vê. Matriz: dizer se existe ou se está em aberto |
| 5. Fluxo | `fluxo` (lista de etapas `etapa, quem, dados, validacoes, pendente`) | A jornada principal, na ordem das telas do protótipo. `pendente` marca a etapa que depende de decisão futura do cliente e precisa ter o mesmo assunto na seção 11 |
| 6. Regras **(obrig.)** | `regras` (`[regra, o que garante]`) | Toda regra que o cliente disse (cálculo, limite, aprovação, quem vê o quê). Regra crítica (duplicidade, conflito, limite) não pode faltar |
| 7. Arquitetura | `arquitetura` (`[rótulo, texto]`) | Frontend por formato, backend, banco, autenticação, integrações externas citadas. Sem stack aqui: stack é a seção 12 |
| 8. Segurança **(obrig.)** | `seguranca` (`[rótulo, texto]`) | Sempre cobrir: tipos de dado (pessoal? sensível? LGPD?), login e controle por perfil, histórico e logs, dados públicos (links sem login). O que ninguém citou: "não citado nas reuniões" |
| 9. Módulos críticos | `modulos_criticos` (`nome, detalhe, mvp, futuro`) | Pagamentos, cada integração externa e as automações (offline com sincronização, rotina agendada, geração de documentos, importação). Sem nenhum: lista vazia |
| 10. Roadmap **(obrig.)** | `roadmap` (`[fase, entrega, natureza]`) | Cada jornada na conta = uma entrega *Prioritário*. *A confirmar* = jornadas só do protótipo, sem menção nas reuniões, e o que foi discutido sem fechar (não está na conta). *Futuro* = o que o cliente deixou para depois. **Nada A confirmar ou Futuro pode aparecer no cronograma** (o script confere pelo texto da entrega) |
| 11. Pontos em aberto **(obrig.)** | `pontos_abertos` (lista de textos) | As perguntas que mudam o prazo **não** vão aqui: o script gera a tabela delas a partir de `dimensionamento.entrada.a_confirmar`, com o custo de cada uma. Aqui, nesta ordem: divergências entre reuniões ou entre reunião e protótipo, dependências externas (API, fornecedor, conta de loja) e dúvidas que não mudam a faixa (data de início). **Nunca vazio** |
| 12. Stack | `stack.itens`, `stack.nao_validado` | O template NTec (Expo, Next.js, MongoDB + Prisma, Better Auth, S3, Vercel, Vitest e Playwright), só as peças que o projeto usa. O primeiro item de `nao_validado` é sempre "Toda a stack é premissa a validar na Sprint de Refino e Prototipação" |
| 13. Cronograma | `cronograma.sprints` (`[sprint, entregas, depende_de]`), `cronograma.duracao_obs` | Ver abaixo |
| 14. Protótipo **(obrig.)** | `prototipo.recebido`, `prototipo.tabela` (`[tela, regra, adaptação, justificativa, vale p/ MVP]`), `prototipo.declaracao` | Onde o protótipo difere do que foi combinado nas reuniões. Sem diferença: `declaracao` = "O protótipo segue integralmente as regras combinadas nas reuniões". Sem protótipo: `recebido: false`, tabela vazia; a proposta avisa o comercial |

`dependencia_externa_sem_confirmacao`: `true` se alguma integração ou fornecedor está sendo tratado como certo sem confirmação. Com a regra de peso fixo e a cláusula de contrato, o normal é `false`.

## Cronograma sprint a sprint (seção 13)

Usar os valores **centrais** de cada fase do `calcular_faixa.py` e encaixar em sprints de 2 semanas até fechar a recomendação de venda.

1. **F1** (imersão e setup): Sprint 1, ou 1 e 2 se F1 passar de 2 semanas. Inclui validar o protótipo e, se houver app nas lojas, pedir as contas Apple e Google.
2. **F2** (acesso e login): a sprint seguinte. Se sobrar meia sprint, começar os cadastros.
3. **F3** (desenvolvimento): as jornadas na ordem de uso, de 1 a 2 por sprint conforme o peso. Jornada com RN específica ou offline com sincronização ocupa a sprint inteira ou mais. Integração com sistema do cliente vai depois da sprint em que vence o prazo da cláusula de acesso à API.
4. **F4** (testes com o cliente), **F5** (deploy) e **F6** (lojas) no fim, nessa ordem. Em F6, contar o tempo de aprovação das lojas.
5. Toda sprint cuja entrega depende de um ponto da seção 11 leva `depende_de` = "ponto N".
6. O número de sprints precisa bater com a recomendação. Se a soma dos centrais for quebrada, a folga fica na última sprint ("correções finais e entrega").

## Anexo — Memória do dimensionamento (`dimensionamento`)

É o que a área de projetos revisa. A proposta mostra a faixa e o detalhamento F1 a F6 calculados pelo script, os alertas da régua e os campos abaixo.

| Campo | Conteúdo |
|---|---|
| `entrada` | O JSON da régua, igual ao de `calcular_faixa.py` |
| `criterios` | `{"F1": "...", ..., "F6": "..."}`: o critério de cada fase, citando transcrição e protótipo (ex.: "F3: 4 jornadas (Protótipo · Agenda, Pagamento, Carteirinha, Painel); pagamento citado em T1 · 00:14:20") |
| `inventario_prototipo` | `[tela/rota, perfil, o que faz, dados, ações, citada em]` (`leitura-transcricoes-prototipo.md`, Passo 2) |
| `atencao` | Pontos de atenção, do mais grave para o menos grave, cada um com o que fazer. Toda integração com sistema do cliente traz aqui a cláusula de contrato pronta de `regua-dimensionamento.md` |
| `lacunas` | `[fator, procurado e não achado, pergunta para o cliente, valor provisório]` |
| `precedente` | O projeto mais parecido em `exemplos/`, o prazo dele e por que é comparável (ou "sem precedente comparável"). Mais de 30% de distância: explicar |
| `cortes` | 2 a 4 cortes `[corte, economia]`, recalculados com o script. Com integração de sistema do cliente, um corte é sempre o plano B (planilha) |
| `suposicoes`, `fronteira`, `imersao` | Suposições (inclui o agrupamento de telas em jornadas e o valor provisório de cada lacuna), os comentários de duas linhas de `regra-fronteira-e-faixa.md` e os detalhes que não mudam o tamanho, para a imersão |

## Checklist final (o script confere)

| Item do template | Como o script decide |
|---|---|
| Transcrições e protótipo anexados | `transcricoes` não vazio e `prototipo_link` preenchido. A PRD não é cobrada: vem depois do contrato |
| Campos OBRIGATÓRIO preenchidos | Seções 4, 6, 8, 10, 11 e 14 não vazias |
| Protótipo segue as regras ou adaptações justificadas | `prototipo.recebido` e tabela ou declaração preenchidas |
| Roadmap e cronograma não se contradizem | Nenhuma entrega *A confirmar* ou *Futuro* aparece no texto do cronograma |
| Pontos em aberto listados | Seção 11 não vazia |
| Nenhuma dependência externa tratada como certa | `dependencia_externa_sem_confirmacao` é `false` |

Item PENDENTE não impede a proposta. Ele sai marcado e vai para o chat com o que o CN precisa fazer.
