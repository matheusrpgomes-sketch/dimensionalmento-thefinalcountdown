---
name: dimensionamento-ntec
description: Dimensiona propostas de software do NTec (Poli Júnior) — sites, webapps, PWAs, apps e painéis — a partir das transcrições das reuniões de diagnóstico e do protótipo navegável (Lovable, Claude, v0, Figma), e devolve uma faixa de semanas (otimista, provável, conservador) com os riscos para a área de projetos, na "Proposta Técnica" do NTec em Markdown (14 seções, cronograma por sprint e memória do dimensionamento). Feita para CNs sem formação técnica; a PRD não é pré-requisito, vem depois do contrato. Use quando pedirem para dimensionar, estimar prazo, validar ou "ver quantas sprints dá" um projeto do NTec; quando mandarem transcrições do Fathom ou de outra ferramenta, o link ou o código de um protótipo, a PRD, o formulário Dimensionamento Tec ou um briefing; quando pedirem a proposta técnica para validação; ou quando perguntarem "cabe em X semanas?" ou "isso é viável?", mesmo que pareça só uma estimativa rápida.
---

# Skill de Dimensionamento — NTec

Transforma as **transcrições das reuniões de diagnóstico** (normalmente duas) e o **protótipo navegável** numa **faixa de semanas** defensável, calibrada nos projetos reais do NTec. O público principal são **CNs sem formação técnica**: a skill pergunta em linguagem de negócio, traduz para fatores técnicos e devolve números que a área de projetos reconhece.

**Onde fica no processo (desde 22/10/2026):** reuniões de diagnóstico gravadas → CN monta o protótipo navegável → **esta skill dimensiona a partir das transcrições + protótipo** → área de projetos revisa → proposta → contrato → **PRD por último** (skill `documento-requisitos-ntec`), como anexo de contrato. Com a PRD pronta, a skill pode rodar de novo para revalidar o número.

A área de projetos sempre revisa o resultado antes de virar proposta. A skill evita que chegue à equipe um prazo "nada a ver". Ela não substitui a validação.

## Arquivos desta pasta (ler sob demanda)

| Arquivo | Quando ler |
|---|---|
| `fatores/README.md` e `fatores/glossario.md` | **Sempre.** Índice dos fatores, decisões em aberto (D1 a D5) e a definição única de cada termo (o glossário vence qualquer outro arquivo) |
| `fatores/F0-viabilidade.md` | **Sempre, antes de tudo.** Critérios que rejeitam o projeto (🚫), param para a área de projetos (🚩) ou só ajustam o contrato |
| `fatores/F1-*.md` a `fatores/F6-*.md` | Sempre: pergunta, onde ler e o que fazer sem resposta para cada fator, com os pesos de cada fase |
| `leitura-transcricoes-prototipo.md` | **Sempre (entrada padrão).** Regra zero contra alucinação, como abrir o protótipo, como cruzar protótipo × transcrição e onde está cada campo do JSON |
| `insumos-e-perguntas.md` | Perguntas prontas para o CN, vocabulário de negócio → técnico, e o caminho com formulário, ficha ou briefing |
| `leitura-prd.md` | Só quando já existe PRD (revalidação depois do contrato). A PRD nunca é usada para contar módulos |
| `regua-dimensionamento.md` | Sempre: regras de uso, faixa final, quando parar, calibração e histórico das mudanças (os pesos estão em `fatores/`) |
| `regra-fronteira-e-faixa.md` | Quando um fator encaixar em duas linhas da régua, e para a tabela de cortes de "O que cortar" |
| `exemplos/*.md` | Para achar um **precedente** parecido (mesmo formato, mesmo porte) e comparar o resultado |
| `scripts/calcular_faixa.py` | Sempre, para fazer a conta (não somar de cabeça) |
| `proposta-tecnica.md` | Sempre, no fim: como preencher cada uma das 14 seções da **Proposta Técnica** a partir das transcrições, do protótipo e da conta |
| `scripts/gerar_proposta.py` | Sempre, no fim: gera "[Proposta Técnica] {projeto}.md" no template do NTec |
| `exemplos/ficticio-petagenda-proposta.json` | Modelo do JSON da proposta, para copiar a estrutura |

## Procedimento

1. **Ler a entrada** (`leitura-transcricoes-prototipo.md`).
   - **Transcrições + protótipo:** caminho padrão. Numerar as transcrições (T1, T2…) por data e montar o inventário de telas do protótipo (Passo 2).
   - **Só transcrições:** dimensionar e marcar ⚠️ *Estimativa preliminar: falta o protótipo*. Pedir o protótipo.
   - **Só o resumo das reuniões** (Gemini, Fathom), sem transcrição: dimensionar como ⚠️ *Estimativa preliminar*, citando `(resumo T1)`, e pedir a transcrição completa.
   - **Só protótipo:** não dimensionar. Pedir as transcrições (o protótipo não responde nada do projeto).
   - **Formulário, ficha ou briefing sem transcrição:** `insumos-e-perguntas.md`, status ⚠️ preliminar.
   - **PRD junto:** só conferência (`leitura-prd.md`). Divergência com transcrição/protótipo vai para *Pontos de atenção*.
2. **F0 — Viabilidade** (`fatores/F0-viabilidade.md`). Responder cada critério com citação da transcrição. Critério de 🚫 rejeição → **parar aqui**: não preencher F1 a F6, não gerar proposta e responder ao CN no formato do fim do F0. Critério de 🚩 parada → seguir dimensionando, mas o status fica 🚩 e a proposta não vai para o cliente antes da área de projetos responder. Critério de contrato (SLA/suporte 24/7, infra sem acesso) → só alerta.
3. **Cruzar protótipo × transcrição** (`leitura-transcricoes-prototipo.md`, Passo 3) e **preencher F1 a F6**, cada um pelo seu arquivo em `fatores/`. Contar **jornadas** pela regra fechada do glossário (perfil + objetivo + entidade principal; cadastro auxiliar não conta; 3+ entidades ou 6+ telas próprias contam 2), nunca telas nem módulos. **Regra de citação (22/10/2026):** só entra na venda o que tem citação. **Toda dúvida fica fora da venda:**
   - **Escopo ambíguo** (jornada ou perfil só no protótipo, tela que passou na demo sem o cliente falar dela, integração ou regra citada de forma vaga): **não conta**.
   - **Fator de projeto sem resposta** (stack, infra, lojas, referência, multitenancy sem detalhe): entra com o **valor do silêncio** (tabela do Passo 4 de `leitura-transcricoes-prototipo.md`), não com o mais pesado.
   - Os dois viram item de **`a_confirmar`** no JSON, com o efeito se a resposta for sim. O script calcula o custo de cada um e a venda sai "**+ até X**". Enquanto houver item em aberto, o status é ⚠️.
   - **Exceção:** ninguém nomeado para validar → `f0.sem_validador_nomeado: true` (🚩, não soma semanas).
   - A **linha mais pesada** só serve para classificar um fator **citado** que encaixa em duas linhas (fronteira), nunca para decidir se algo entra.
   **Integrações não geram pergunta sobre documentação:** peso fixo de `fatores/F3-integracoes.md`.
4. **Montar o JSON** de entrada no formato dos `exemplos/*.json`: o bloco `"f0"`, **todos** os campos de F1 a F6 e o `a_confirmar` (formato no Passo 5 de `leitura-transcricoes-prototipo.md`). Nenhum campo tem padrão: se faltar um, o script para e diz qual. Rodar:
   ```bash
   python scripts/calcular_faixa.py entrada.json
   ```
   Sem Python disponível, fazer a conta pelas tabelas de `fatores/` e dizer isso em *Observações*.
5. **Comparar com o precedente** mais parecido em `exemplos/`. Se o resultado ficar muito longe do precedente (mais de 30%), explicar o porquê ou rever os fatores.
6. **Aplicar fronteira** se necessário (`regra-fronteira-e-faixa.md`).
7. **Montar a Proposta Técnica** (`proposta-tecnica.md`): um JSON com as 14 seções do template e o bloco `dimensionamento` (a mesma entrada do passo 4, mais critérios, inventário de telas, lacunas, precedente, cortes e observações). Gerar o Markdown:
   ```bash
   python scripts/gerar_proposta.py proposta.json --saida <pasta-que-o-CN-vê>
   ```
   O script recalcula a faixa a partir de `dimensionamento.entrada` (nunca digitar as semanas no JSON) e confere o checklist final do template. Projeto rejeitado no F0 não gera proposta. Os avisos internos (decisões D1 a D5 em aberto) saem só no terminal. Não precisa de biblioteca extra.
8. **Responder no chat** no formato curto abaixo: o detalhe está na proposta.

## Regras gerais

- **Sem alucinação de contexto.** Todo fator, jornada, perfil e regra tem a origem ao lado: `(T1 · 00:12:30 — "trecho")`, `(Protótipo · tela "Agenda")`, `(CN, no chat)`, `(silêncio — valor do Passo 4)`, `(fronteira — linha mais pesada)`. Não completar o produto com o que "normalmente tem". Dado fictício do protótipo não prova integração. Silêncio do cliente não é aceite. Citação que não se acha de novo no texto não existe.
- **Nunca inventar número nem fator.** O que as reuniões não decidem vai para `a_confirmar`, e o custo sai do script, nunca de cabeça.
- **Ambiguidade não é gordura.** Dúvida fica fora da venda, como pergunta com custo (Projeto CTE, 22/10/2026: ambiguidades viraram margem e deram 17 sprints, com 13 a 14 esperadas). **E também não é desconto:** enquanto houver pergunta em aberto, o status é ⚠️ e a proposta não vai ao cliente, porque o erro histórico do NTec é vender para menos (Projeto C: vendido 11, levou ~14).
- **Só os fatores contam.** O prazo sai do F0 ao F6 e dos multiplicadores de `fatores/`, nada além disso: nem faixa de portfólio, nem prazo pedido pelo cliente, nem palpite do CN.
- **Restrição técnica → F0, não aumentar prazo.** Multitenancy com regra diferente por tenant (parada obrigatória), integração com sistema sem API, feature sem referência nem documentação e dependência de hardware viram 🚩 no F0, não "+3 semanas".
- **Sempre trazer a seção "O que cortar".** Cada corte é uma jornada ou uma integração que está na conta, nunca algo que o cliente já tirou.
- **Não acrescentar escopo.** Se a skill achar que falta algo para o produto funcionar, isso vai para *Pontos de atenção* ("as reuniões não cobrem X"), e não para a conta.
- **Não prometer stack nem tecnologia.** A seção 12 sugere a stack do template NTec sempre como *premissa a validar na Sprint de Refino*.
- **Semanas off e garantia ficam fora da faixa**: somar as semanas off do calendário depois; a garantia de 30 dias é gratuita.
- **Precificação não é desta skill.** A skill entrega semanas. O ajuste do ETIP nas fases finais (testes, deploy, lojas, gestão da mudança com dedicação de 25% a 50%) é feito na precificação; a skill só mostra quanto do prazo é F4 a F6 no anexo.

## Parar e sinalizar para a área de projetos

- 🚫 **Rejeitado no F0** (stack exigida fora da lista, offline com sincronização em MongoDB exigido): não dimensionar.
- 🚩 **Parado no F0** (ninguém nomeado para validar, feature sem referência nem documentação, hardware, multitenancy com regra diferente por tenant, integração sem API, prazo exigido abaixo do otimista): dimensionar, mas não vender sem a área de projetos.
- **Ajuste de contrato** (suporte 24/7 ou SLA → contrato de manutenção à parte; infra do cliente sem acesso → sem garantia): dimensionar normalmente e trazer o alerta.
- **Demanda pouco detalhada** (`fatores/F1-imersao-setup.md`, 1.2): abrir a resposta com o alerta de discovery. O status nunca é ✅.
- **Provável acima de 26 semanas**: a régua ainda não foi calibrada para projetos grandes. Dimensionar mesmo assim, marcar ⚠️ e sugerir quebrar em fases.
- Dependência de dados de bases soltas → chamar o núcleo de Dados.
- Cliente Enterprise ou Grande com restrição de stack ou regras de deploy próprias.
- Divergência entre o que o CN declarou, o protótipo e as transcrições.
- Teto de fase passado (F1, F2 ou F4 acima de 4 semanas): a soma é mantida, não cortada, e a área de projetos revisa (D4, provisório).

## Entregável: a Proposta Técnica (template do NTec, em Markdown)

O dimensionamento final sai **no template "Proposta Técnica" do NTec** (Comercial → Validação de Projeto), como arquivo **Markdown** (desde 22/10/2026; antes era PDF). São 14 seções, seis delas OBRIGATÓRIAS (4 Perfis, 6 Regras, 8 Segurança, 10 Roadmap, 11 Pontos em aberto, 14 Protótipo), o checklist final e, no fim, o **Anexo — Memória do dimensionamento**: faixa, F1 a F6 com critério, alertas, inventário de telas do protótipo, lacunas, precedente, O que cortar, suposições, ajustes de fronteira e pontos para a imersão.

Onde o dimensionamento aparece no corpo do template:
- **Caixa de status** (topo): status, prazo recomendado, a faixa e os insumos (transcrições, protótipo; a PRD aparece como "gerada depois da assinatura").
- **10. Roadmap:** tudo que está na conta é *Prioritário*. *A confirmar* (inclui as jornadas só do protótipo) e *Futuro* nunca entram no cronograma (o script confere).
- **11. Pontos em aberto:** a tabela "Perguntas que mudam o prazo" (gerada pelo script a partir de `a_confirmar`) e toda dependência externa. Nunca vazio.
- **13. Cronograma sprint a sprint:** as fases F1 a F6 (valores centrais) distribuídas em sprints de 2 semanas, somando a recomendação de venda.

**O que a skill não inventa no template:** conteúdo do protótipo que ela não conseguiu abrir (a seção 14 sai com o aviso e o checklist fica PENDENTE), responsável comercial e data de envio (em branco, para o CN), e histórico, logs ou permissões que ninguém citou (escrever "não citado nas reuniões").

## Resposta no chat (sempre esta, curta)

Público: um CN que talvez nunca tenha programado.

1. `# Projeto [nome do cliente ou produto]`
2. **Status**, uma linha: ✅ Pronto para proposta · ⚠️ Precisa de revisão da área de projetos (inclui "⚠️ Estimativa preliminar" e "⚠️ Demanda pouco detalhada") · 🚩 Parado · 🚫 Rejeitado no F0 (nesse caso, a resposta é só o bloco do fim de `fatores/F0-viabilidade.md`, sem os itens 3 a 8).
3. **Prazo em uma frase.** Ex.: *"Recomendado vender 18 semanas (9 sprints), mais as semanas off. Não vender abaixo de 13."* Com perguntas em aberto, usar a frase do script, com "+ até": *"Recomendado vender 16 semanas (8 sprints) + até 4 que dependem de 3 perguntas em aberto, mais as semanas off."*
4. **Faixa:** otimista · provável · conservador, em semanas e sprints.
5. **Caminho do arquivo** "[Proposta Técnica] {projeto}.md".
6. **Perguntas para o CN**, numa tabela só, copiada da saída do script (as 5 que mais mexem no prazo primeiro): `# | O que ficou ambíguo | Pergunta para o cliente | Se sim: venda`. Ou `Sem perguntas: tudo veio das transcrições e do protótipo.`
7. **Itens PENDENTES do checklist**, com o que o CN precisa fazer.
8. **Os 2 ou 3 pontos de atenção mais graves**, uma linha cada.

## Status da skill

Versão inicial (16/10/2026). Revisão de 20/10/2026: F0 de viabilidade antes de tudo, um arquivo por fator em `fatores/`, nenhum campo do JSON com padrão, tetos que não cortam a soma. Revisão de 22/10/2026 (Projeto G): fluxo = jornada, fator de formato por fluxo (`fluxos_por_formato`). **Revisão de 22/10/2026 (reunião "Validação Entregas Tec", Projeto CTE):** a entrada padrão passa a ser transcrições + protótipo navegável, e a PRD vem por último; ambiguidade de escopo vira pergunta, não gordura; regra zero contra alucinação; F0 sem multa por atraso, SLA/24-7 e infra sem acesso viram ajuste de contrato, multitenancy por tenant é parada obrigatória; proposta em Markdown no lugar do PDF. **Revisão de 22/10/2026 (decisões do Matheus):** jornada com regra fechada; tela que só passou na demo não conta; nenhuma dúvida entra na venda (`a_confirmar`, "+ até X"; `lacunas_fathom` saiu); só o resumo da reunião → preliminar; glossário e F1 a F6 escritos para transcrição + protótipo. Pesos inalterados. Pendente: (1) testar o novo fluxo com as transcrições e o protótipo de um projeto real e comparar com o número da área de projetos; (2) fichas técnicas dos Projetos E e F para calibrar projetos grandes; (3) a proposta do Projeto CTE para comparar com o dimensionamento.
