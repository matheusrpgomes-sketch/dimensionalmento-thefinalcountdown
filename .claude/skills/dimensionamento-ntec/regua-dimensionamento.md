# Régua de Dimensionamento — NTec

Regras gerais para transformar o que o coordenador de negócios (CN) levantou em uma faixa de semanas. Os pesos de cada fase ficam em `fatores/` (um arquivo por fase, do F0 ao F6). A estrutura de fases vem do **Baseline de Projeto** do formulário *Dimensionamento Tec* (seção 7). Os fatores vêm do **Perfil da demanda** (seção 6). Os pesos foram calibrados contra os projetos reais do NTec (ver `exemplos/`).

**Fonte da verdade dos números:** `scripts/calcular_faixa.py`. As tabelas de `fatores/` e o script precisam bater. Se mudar um, mude o outro e registre no fim deste arquivo.

**Índice:** Regras de uso · Regras transversais · F0 a F6 · Faixa final · Parar e sinalizar · Calibração · Lacunas · Registro das fontes

---

## Regras de uso (ler antes de dimensionar)

1. **Não inventar fator.** Cada fator tem uma pergunta de sim ou não e o lugar onde ler a resposta (`fatores/`). Só entra na venda o que tem citação da transcrição (ou da tela do protótipo, confirmada por fala). **Sem citação** (revisão de 22/10/2026): o campo fica no valor do silêncio (`leitura-transcricoes-prototipo.md`, Passo 4) e a dúvida vai para `a_confirmar`, que o script calcula **fora** da venda ("vender 14 + até 4"), com status ⚠️ até o CN responder. Assim a dúvida não vira gordura (erro do CTE) e também não vira desconto escondido (erro do Projeto C, vendido para menos). A linha mais pesada só decide o empate de um fator **citado** que encaixa em duas linhas (`regra-fronteira-e-faixa.md`).
2. **Toda linha tem três valores: mínimo / central / máximo.** O mínimo é o cenário "tudo dá certo", o central é o que costuma acontecer no NTec e o máximo é "os riscos aparecem".
3. **F0 primeiro, depois somar fase a fase, na ordem F1 a F6.** O F0 não soma semanas: rejeita o projeto ou para para a área de projetos. As fases são sequenciais na régua, mesmo quando na prática se sobrepõem um pouco. A sobreposição é a folga natural do time.
4. **Rodar o script para fechar a conta.** Não somar de cabeça.
5. **Casos de fronteira** (o projeto encaixa em duas linhas): `regra-fronteira-e-faixa.md`.

---

## Regras transversais

### Os pesos já assumem o time típico do NTec
Uma dupla de empresa júnior com **cerca de 20 horas por semana somadas**, sprints de 2 semanas e o template do monorepo NTec (Next.js + Expo + MongoDB/Prisma + Better Auth). **Sem multiplicador por ferramenta:** o fator Claude Code foi removido na reunião de 20/10/2026. **Sem buffer percentual:** o risco já está no intervalo mínimo / central / máximo de cada linha (a margem explícita está em aberto, D3).

### O que o template já entrega (não soma prazo)
Login por e-mail e senha, recuperação de senha, login com Google, envio de e-mail (Resend), upload de arquivo para AWS S3, estrutura de API e painel admin básico. Quando uma "integração" é uma dessas, ela entra como `template` (0 semanas).

### Formato conta por código separado, não por tela
Um painel admin dentro do mesmo app web **não** é um formato a mais. Um app nativo + um painel web **são** dois formatos (dois códigos, duas publicações). Desde 22/10/2026, cada fluxo recebe o fator do código em que existe; o formato extra só pesa nos fluxos com tela nos dois códigos (`fatores/F3-desenvolvimento.md`, 3.2).

### Semanas off e garantia ficam fora da régua
- **Semanas off** (férias, provas, recesso de fim de ano, julho) entram por calendário, somadas depois da faixa. No histórico, de 1 a 3 por projeto.
- **Garantia de 30 dias** é gratuita e não entra no prazo (vale para o que está no documento de requisitos).

---

## F0 a F6 — os fatores

Desde a revisão de 20/10/2026, cada fase tem o seu arquivo em `fatores/`, com a pergunta de sim ou não, onde ler (nas transcrições e no protótipo; seções da PRD só na revalidação), o que fazer sem resposta e a tabela de pesos. **Os pesos estão lá, não aqui.**

| Fase | Arquivo | Campos do JSON |
|---|---|---|
| F0 Viabilidade (não soma semanas) | `fatores/F0-viabilidade.md` | bloco `"f0"`: `stack_exigida_fora_da_lista`, `offline_sync_com_mongodb_exigido` (🚫 rejeitam); `sla_ou_sustentacao`, `infra_cliente_sem_acesso` (📝 ajustam o contrato); `sem_validador_nomeado`, `feature_sem_referencia_nem_doc`, `hardware` (🚩 param); `prazo_exigido_semanas` (número ou `null`). `multa_por_atraso` saiu em 22/10/2026 |
| F1 Imersão, refinamento e setup | `fatores/F1-imersao-setup.md` | `demanda_pouco_detalhada`, `stack_fora_template`, `atipico` |
| F2 Acesso e multitenancy | `fatores/F2-acesso-multitenancy.md` | `niveis_acesso` (`nenhum`, `1`, `2-5-poucas`, `2-5-grandes`, `6+`), `multitenancy` (`nao`, `separado`, `isolado`, `instancias`) |
| F3 Desenvolvimento | `fatores/F3-desenvolvimento.md` | `fluxos_comuns`, `fluxos_rn_especifica`, `features_atipicas`, `formatos` (`web`, `pwa`, `app`), `fluxos_por_formato` (só com mais de um formato), `dependencia_dados`, `offline` (`nao`, `local`, `sync`), `volume_alto` |
| F3 Integrações | `fatores/F3-integracoes.md` | `integracoes` (lista de `template`, `uni_doc`, `bi_doc`, `uni_sem_doc`, `bi_sem_doc`, `sem_api`; `[]` se não houver) |
| F4 Testes com o cliente | `fatores/F4-testes.md` | `rn_critica` |
| F5 Deploy | `fatores/F5-deploy.md` | `deploy_infra_cliente` |
| F6 Publicação nas lojas | `fatores/F6-lojas.md` | `lojas` (`nao`, `normal`, `sensivel`) |

Opcionais: `projeto` e `a_confirmar` (ver *Faixa final*). **Nenhum outro campo tem padrão:** campo ausente, valor desconhecido ou campo removido (`claude_code`, `cliente_pouca_disponibilidade`, `lacunas_fathom`) faz o script parar com a lista do que corrigir.

**Decisões em aberto** (`fatores/README.md`): D1 formato extra, D2 pesos que a reunião mandou aumentar, D3 margem de segurança, D4 teto de fase, D5 Postgres por causa do offline. Até a área técnica decidir, o script usa o valor provisório, marcado com o código da decisão nas constantes.

---

## Faixa final

Sem buffer percentual (removido em 17/10/2026: o efeito era desprezível e o risco já está no intervalo de cada linha).

| Cenário | Conta | Para que serve |
|---|---|---|
| **Otimista (piso)** | soma dos mínimos | Nunca vender abaixo disto. Só se chega nele com escopo congelado e cliente rápido |
| **Provável (recomendado)** | soma dos centrais | O valor para a proposta |
| **Conservador (teto de risco)** | soma dos máximos | O que acontece se os riscos listados se confirmarem |

- **Arredondamento:** semanas sempre para cima. A **recomendação de venda** é o provável arredondado para cima até fechar sprints inteiras (número par de semanas).
- **Perguntas em aberto** (`"a_confirmar"` no JSON, desde 22/10/2026): **não entram na venda.** O script calcula, para cada uma, quanto soma no provável e na venda se a resposta for sim, e a venda sai "**14 semanas + até 4** que dependem de 3 perguntas em aberto" (o "até" é com todas sim, em sprints inteiras). Enquanto houver pergunta em aberto, o status é ⚠️. Substitui o antigo `lacunas_fathom`, que punha a lacuna na venda no valor mais pesado.
- **Depois somar as semanas off** do calendário.

---

## Parar e sinalizar (a skill não decide sozinha)

- 🚫 Critério de rejeição do F0 (stack exigida fora da lista, offline com sincronização em MongoDB exigido) → não dimensionar (`fatores/F0-viabilidade.md`).
- 🚩 Critério de parada do F0: ninguém do cliente nomeado para validar, feature sem referência **e** sem documentação, hardware, multitenancy com regra diferente por tenant (`instancias`, parada obrigatória), integração com sistema sem API (`sem_api`), prazo exigido abaixo do otimista.
- 📝 Ajuste de contrato no F0: suporte 24/7 ou SLA (contrato de manutenção à parte), infra do cliente sem acesso (sem garantia).
- ⚠️ Demanda pouco detalhada → recomendar discovery antes da proposta (`fatores/F1-imersao-setup.md`, 1.2).
- ⚠️ Dependência de dados → chamar o núcleo de Dados para avaliar se precisa de engenharia de dados.
- ⚠️ Provável acima de **26 semanas** → fora da faixa calibrada (ver Calibração). Validar com a área de projetos e considerar quebrar em fases ou contratos.
- ⚠️ Cliente Enterprise ou Grande com regras de deploy e restrição de stack → envolver a área de projetos antes da proposta.
- ⚠️ Teto de fase passado (F1, F2 ou F4 acima de 4 semanas): a soma é mantida, não cortada (D4, provisório).

---

## Calibração (estado em 22/10/2026; os números são conferidos por `scripts/testar_exemplos.py`)

Rodando a régua sobre os projetos reais (detalhes em `exemplos/`):

| Projeto | Otimista | Provável | Conservador | Vendido | Realizado / situação | Leitura |
|---|---|---|---|---|---|---|
| Projeto A | 9 | 12 | 16 | 12 (+1 off) | No prazo, finalizando | ✅ Provável = vendido |
| Projeto D | 13 | 18 | 23 | 18 (+3 off) | Em execução, sem atraso (47,6% do prazo) | ✅ Recomendação = vendido |
| Projeto C | 13 | 18 | 24 | 11 (+2 off) | ~14 semanas, atrasou, testes não terminados | ⚠️ Vendido abaixo do piso → atrasou. Régua ~3 semanas acima do real |
| Projeto B | 9 | 12 | 18 | 12 (+1 off) | Em execução (45% do prazo), com Claude Code | ✅ Recomendação = vendido, recontado por jornada pela T1 + protótipo (rodada às cegas de 22/10/2026). Conferir no fim (23/11/2026) |
| Projeto E | — | — | — | 34 | Em execução | Sem ficha técnica; não calibrado |
| Projeto F | — | — | — | 38 (+3 off) | Em execução | Sem ficha técnica; não calibrado |

Leituras:
- **Projetos pequenos e médios (até ~20 semanas):** a régua acerta ou fica um pouco acima. É intencional que erre para cima.
- **Viés conhecido:** quando o time aproveita bem o template, setup e login andam juntos e mais rápido (Projeto C fez os dois em 2 semanas). A régua não desconta isso automaticamente.
- **Claude Code:** não há fator na régua desde 20/10/2026. Se o ganho da ferramenta for real, ele aparece nos realizados dos próximos projetos e entra pelos pesos, com dado medido.
- **Projetos grandes (Projetos E, F, 30+ semanas):** sem dados de ficha, a régua **não está calibrada** para eles. Por isso o alerta acima de 26 semanas.

---

## Lacunas

- **Amostra pequena:** 4 projetos com dados, 2 ainda em execução. Os pesos são um ponto de partida, não uma regressão.
- **Contagem de fluxos dos projetos antigos é estimada** a partir das tasks do Notion (marcada como palpite nos exemplos).
- **Regras de tradução da PRD ainda não calibradas:** "1 módulo = 1 fluxo" e "concorrência, imutabilidade ou rotina agendada → módulo com RN específica" (`leitura-prd.md`) não foram conferidas contra um projeto real, porque todos os projetos da calibração são anteriores à PRD.
- **A "Régua de Dimensionamento" citada no formulário é uma subpágina do Notion** que não veio no PDF. Se ela tiver números diferentes, ela vence e este arquivo precisa ser atualizado.
- **Retrospectivas quase sempre vazias:** as causas de atraso não estão registradas.

---

## Registro das fontes

| Data | Fonte | O que trouxe |
|---|---|---|
| 16/10/2026 | Formulário *Dimensionamento Tec* (PDF, 5 páginas) | Estrutura de fases (baseline 1–4 semanas por fase, lojas 2–6), fatores do perfil da demanda, níveis de multitenancy e integração, buffer adaptável, checklist da área de projetos |
| 16/10/2026 | Levantamento no Notion do NTec (base de projetos: Projeto C, Projeto A, Projeto B, Projeto D, Projetos E, F) | Semanas vendidas, sprints realizadas, fases por task, riscos dos hand-offs |
| 16/10/2026 | Calibração inicial (Matheus Padilha + Claude) | Pesos mín/central/máx; regra "atípico ≠ RN específica"; corte de calibração em 26 semanas |
| 16/10/2026 | Skill `documento-requisitos-ntec` ([repositório](https://github.com/rivasaugustus/documento-requisitos-ntec)) | PRD vira a entrada padrão. Mapeamento da PRD para os fatores, sem peso novo: 1 módulo = 1 fluxo; fatores de complexidade da PRD encaixados nas linhas existentes (`leitura-prd.md`) |
| 17/10/2026 | Decisão do NTec: CNs não avaliam API e não há técnico para validar antes da proposta | Integração com peso fixo, sem perguntar ao CN: serviço de mercado = linha "com documentação", sistema do cliente = linha "sem documentação", com cláusula de contrato e plano B (planilha). Pesos inalterados |
| 17/10/2026 | Decisão do NTec: buffer desprezível | Buffer de risco adaptável (seção 8 do formulário) removido: provável = soma dos centrais, conservador = soma dos máximos. Projeto B passa de 11 / 15 / 23 para 11 / 14 / 21. Também saiu a negociação "quando o cliente pede menos prazo" (a seção "O que cortar" continua) |
| 17/10/2026 | Template "Proposta Técnica" do NTec (PDF, 2 páginas, 14 seções) | Entregável da skill: a faixa entra na caixa de status, no roadmap (10), nos pontos em aberto (11) e no cronograma sprint a sprint (13); a memória do dimensionamento vai num anexo. Pesos inalterados |
| 17/10/2026 | Ritmo real do Projeto B no git (dupla, ~20 h/semana, Claude Code) | Fator Claude Code: núcleo do F3 x0,4 / 0,5 / 0,65 e F2 x0,5 / 0,65 / 0,8; demais fases iguais. Time típico passa a ser a dupla com ~20 h/semana somadas. Projetos antigos ficam com `claude_code: false` |
| 17/10/2026 | Revisão da área de projetos: app + painel de 8 fluxos com offline deve levar ~12 sprints | Fator Claude Code revisto para o meio-termo: núcleo do F3 x0,6 / 0,75 / 0,9 e F2 x0,7 / 0,85 / 1 (o x0,5 inicial dava 20 semanas para esse projeto). Projeto B continua em vender 12 |
| 20/10/2026 | Reunião "Validação Skill NTec" e análise do LLM Council (21/10/2026) | F0 de viabilidade antes de tudo; um arquivo por fator em `fatores/` (pesos saem deste arquivo); nenhum campo do JSON com padrão; tetos não cortam a soma; fator Claude Code e "cliente com pouca disponibilidade" removidos; F2 em 2 a 5 / 6+; formato extra +0,2; `bi_sem_doc` com mínimo 4. Decisões D1 a D5 com valores provisórios. Calibração: B 10 / 13 / 20 (vender 14), C 13 / 18 / 24 |
| 22/10/2026 | Dimensionamento do Projeto G (app de campo offline + painel web; primeira PRD em três níveis): a skill deu 17 sprints e a área esperava ~14 | Diagnóstico: o erro estava na tradução da PRD, não nos pesos (baixar o peso do fluxo para 0,9 levaria A de 12 para 10 e D de 18 para 16). Mudanças: (1) fluxo = jornada, independente da numeração da PRD (glossário); (2) fator de formato por fluxo (`fluxos_por_formato`), com o formato extra só nos fluxos `compartilhado`; (3) relatório em template fixo não é RN específica; (4) upload simples do usuário não é dependência de dados; (5) Superfície vale pelo título da seção-mãe; (6) `lojas` pode ser lacuna do Fathom ("+"). Projeto G: vender 34 → 28 semanas (14 sprints = 24 + 4 que dependem de referência de produto e lojas). Pesos inalterados; A a D com os mesmos números (C e D com todos os fluxos `compartilhado`, a conferir) |
| 22/10/2026 | Reunião "Validação Entregas Tec" (Projeto CTE: a skill deu 17 sprints, esperado 13 a 14; diferença vinda de ambiguidades da PRD tratadas como margem e da precificação de testes e gestão da mudança) | (1) Entrada padrão = transcrições das reuniões de diagnóstico + protótipo navegável; a PRD vem depois do contrato (`leitura-transcricoes-prototipo.md`); (2) ambiguidade de escopo vira pergunta com custo, não semana; (3) regra zero contra alucinação (toda informação com citação); (4) F0: multa por atraso sai; SLA/24-7 e infra sem acesso viram ajuste de contrato; multitenancy por tenant é parada obrigatória; (5) proposta em Markdown no lugar do PDF; (6) redução do ETIP nas fases finais fica na precificação, fora da skill. Pesos inalterados; A a D com os mesmos números |
| 22/10/2026 | Decisões do Matheus sobre a reunião "Validação Entregas Tec" (revisão do fluxo transcrições + protótipo) | (1) Jornada com regra fechada: perfil + objetivo + entidade principal; cadastro auxiliar não conta; 3+ entidades principais ou 6+ telas próprias contam 2 (limites a calibrar no CTE); (2) tela que só passou na demo, sem fala do cliente, não conta; (3) nenhuma dúvida entra na venda: valor do silêncio (tabela única no Passo 4 de `leitura-transcricoes-prototipo.md`) + `a_confirmar`, calculado pelo script fora da venda ("+ até X"), status ⚠️ até a resposta; `lacunas_fathom` removido; (4) só o resumo da reunião → ⚠️ preliminar; (5) glossário e F1 a F6 escritos para transcrição + protótipo; F5 corrigido (infra sem acesso não rejeita); F0: feature sem referência só com confirmação do CN, prazo exigido contado da data de início. Pesos inalterados; A a D com os mesmos números |
| 22/10/2026 | Rodada às cegas do Projeto B (T1 + protótipo + planilha) e revisão da skill | (1) Projeto B recontado por jornada: 0 comum + 1 RN (o fluxo "interface e preferências" não foi pedido) → 9 / 12 / 18, venda = vendido; (2) regras fechadas: cliente pessoa física que revisa o protótipo é validadora nomeada (F0); "sem internet" + nada salvo = offline local (F3); calculadora clínica ou de dose é Medical = app sensível (F6); vale o protótipo mostrado ao cliente (leitura); (3) `scripts/testar_exemplos.py` + CI conferem os 7 exemplos e a tabela de `exemplos/README.md`; fichas e tabela recalculadas; (4) texto antigo limpo (fronteira, F0, fator Claude Code). Pesos inalterados |
