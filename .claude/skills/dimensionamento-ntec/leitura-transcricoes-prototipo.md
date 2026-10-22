# Leitura das transcrições e do protótipo — a entrada padrão

✅ **Reunião "Validação Entregas Tec" (22/10/2026):** o dimensionamento sai direto das **transcrições das reuniões de diagnóstico** (normalmente duas) e do **protótipo navegável** (Lovable, Claude, v0, Figma…). A PRD **não** é pré-requisito: ela é gerada depois da assinatura, como anexo de contrato, e serve para revalidar o número (`leitura-prd.md`).

Por que mudou: contar módulos da PRD media o estilo de quem escreveu o documento, não o trabalho. E ambiguidade na PRD virava gordura na conta (Projeto CTE: 17 sprints, com 13 a 14 esperadas). Agora a skill conta **jornadas** que o cliente pediu e que aparecem no protótipo, e **ambiguidade vira pergunta para o CN**, não semana a mais.

Este arquivo diz onde, nas transcrições e no protótipo, está cada campo do JSON do `scripts/calcular_faixa.py`. O critério completo de cada fator está em `fatores/`; se divergirem, vale `fatores/`. **Todo campo é obrigatório:** o script não tem valor padrão.

---

## Regra zero — sem alucinação de contexto

Tudo que entra no JSON e na proposta precisa de **uma** destas origens, escrita ao lado:

| Origem | Como citar |
|---|---|
| Fala numa transcrição | `(T1 · 00:12:30 — "a Ana valida toda sexta")`. Sem marcação de tempo: `(T1 — "trecho")` |
| Tela do protótipo | `(Protótipo · tela "Agenda da clínica")` ou `(Protótipo · rota /admin/agenda)` |
| Resposta do CN no chat | `(CN, no chat)` |
| Regra da skill | `(regra de peso fixo)`, `(suposição da skill — valor mais pesado)` |

Proibido:
- **Completar o produto com o que "normalmente tem"** (tela de relatórios, painel admin, notificações, histórico). Se ninguém falou e o protótipo não mostra, não existe.
- **Ler intenção no tom da conversa.** "Seria legal ter…", "quem sabe depois", "vamos ver" não é escopo.
- **Tratar dado fictício do protótipo como integração real.** Um card "Pago via Pix" com dado inventado não prova que existe integração de pagamento: precisa de fala na transcrição ou de um fluxo completo de pagamento no protótipo.
- **Misturar projetos.** Se a transcrição cita outro cliente ou outro projeto da Poli como exemplo, aquilo não entra no escopo.

Se uma citação não puder ser encontrada de novo no texto, ela não existe: tire o item.

---

## Passo 1 — O que o CN manda

| Peça | Como usar |
|---|---|
| **Transcrições das reuniões de diagnóstico** (Fathom, Granola, Meet, Teams; texto colado, `.txt`, `.md`, `.docx` ou PDF) | Fonte do **escopo pedido** e de tudo que é do **projeto** (quem valida, stack, infra, lojas, prazo, contrato, referências). Numerar na ordem das datas: T1, T2… |
| **Protótipo navegável** (link, código exportado, prints ou vídeo) | Fonte das **jornadas, telas e perfis**: é o que o cliente viu. Ver o Passo 2 |
| Resumo da reunião (anotações do Gemini, do Fathom) | Só para achar o trecho na transcrição. Não cita resumo: cita a transcrição |
| Formulário Dimensionamento Tec, ficha, briefing | Complemento. Vocabulário e perguntas em `insumos-e-perguntas.md` |
| PRD (se já existir) | Conferência, nunca contagem de módulo. Divergência com transcrição/protótipo vai para *Pontos de atenção* |

**O que precisa ter para dimensionar:**

| Chegou | O que a skill faz |
|---|---|
| Transcrições + protótipo | Caminho padrão. Status pode ser ✅ |
| Só transcrições | Dimensiona, status ⚠️ *Estimativa preliminar: falta o protótipo*. Pede o protótipo ao CN |
| Só protótipo | **Não dimensiona.** O protótipo não diz nada do projeto (quem valida, lojas, infra, prazo). Pedir as transcrições |
| Uma transcrição só (esperava duas) | Dimensiona normalmente, e pergunta ao CN se houve outra reunião |

---

## Passo 2 — Abrir o protótipo e montar o inventário de telas

Tente nesta ordem, até uma funcionar:

1. **Link** (Lovable, Claude, v0, Vercel, Figma): abrir no navegador que a sessão tiver (ferramentas de browser) e **clicar por todo o menu**, em cada perfil se houver troca de perfil ou login de demonstração. Ler o texto da página (`get_page_text` / `read_page`) e tirar print só quando o texto não bastar. Buscar a página só por HTTP costuma trazer uma casca vazia (o protótipo é montado no navegador): se vier vazia, não concluir nada dela.
2. **Código exportado** (repositório do Lovable, zip): as telas são as **rotas** (`src/App.tsx`, `src/pages/`, `app/**/page.tsx`, `src/routes/`). Os perfis aparecem em guards de rota, menus condicionais e dados de mock de usuário. Pastas `mock`, `data`, `fixtures` mostram as **entidades**, não integrações.
3. **Prints, PDF ou vídeo**: ler as imagens na ordem em que o CN mandou.
4. Nada disso abriu: pedir ao CN **uma vez** os prints das telas ou o código exportado. Sem resposta, seguir como *Só transcrições*.

Monte o **inventário de telas**, que vai para o anexo da proposta em `dimensionamento.inventario_prototipo` (uma lista de linhas com as seis colunas abaixo):

| Tela / rota | Perfil que vê | O que a pessoa faz ali | Dados que aparecem | Ações (botões que gravam, enviam, cobram) | Citada em |
|---|---|---|---|---|---|

A coluna **Citada em** liga a tela à fala: `T2 · 00:18:10` ou `não citada`.

**Protótipo é desenho, não especificação.** Ele diz *quais* jornadas existem e *quem* as usa. Não diz formato (todo protótipo do Lovable é web, mesmo que o produto seja app), offline, volume, nem se o botão "Enviar no WhatsApp" é um link ou uma integração. Essas respostas vêm da transcrição.

---

## Passo 3 — Cruzar protótipo × transcrição: o que é escopo

A unidade de contagem é a **jornada** (glossário, *Fluxo*): um objetivo completo de uma pessoa, do começo ao fim (ex.: "o tutor agenda e paga a consulta"). Várias telas da mesma jornada = 1 fluxo. Contar jornadas, nunca telas nem menus.

| Situação | Entra na conta? | O que fazer |
|---|---|---|
| Jornada no protótipo **e** pedida na transcrição | Sim | Citar as duas origens |
| Jornada no protótipo, **não** citada nas transcrições, mas apresentada ao cliente numa reunião sem objeção (ex.: T2 é a apresentação do protótipo) | Sim | Citar a reunião em que o protótipo foi mostrado |
| Jornada só no protótipo, **sem nenhuma** menção nas reuniões | **Não** | Vai para a seção 11 como *A confirmar*, com o custo dela ("se entrar: +1,25 semana no provável") e uma pergunta pronta para o CN. Prototipadores com IA criam telas que ninguém pediu: contar isso é a gordura que a reunião de 22/10 mandou tirar |
| Jornada pedida explicitamente na transcrição, **sem tela** no protótipo | Sim | Ponto de atenção: "o protótipo não cobre X". Se a fala for vaga, é lacuna, não escopo |
| Cliente disse que **não** quer, ou "fica para depois" | Não | Vai para *Futuro* no roadmap |
| Duas reuniões discordam | Vale a **mais recente** | Divergência em *Pontos de atenção*. Se não der para saber qual vale, é lacuna |

**Duas regras diferentes para coisas diferentes:**
- **Escopo ambíguo** (não se sabe *se* a jornada entra): não conta; vira pergunta com custo. O CN decide com o cliente.
- **Fator de projeto sem resposta** (quem valida, stack, lojas, referência, infra): entra com o **valor mais pesado** + lacuna com "+" na venda, como sempre (`regua-dimensionamento.md`, *Faixa final*).

---

## Passo 4 — Onde está cada campo do JSON

**Primeiro o F0** (`fatores/F0-viabilidade.md`):

| Campo do bloco `"f0"` | Onde ler | Como traduzir |
|---|---|---|
| `stack_exigida_fora_da_lista` | Transcrição ("tem que ser em…", "nossa TI só aceita…") | `true` só se o cliente **exige**. "Vocês decidem" → `false`. 🚫 rejeita |
| `offline_sync_com_mongodb_exigido` | Transcrição | Grava sem internet para subir depois **e** o cliente exige MongoDB → `true`. 🚫 rejeita |
| `sla_ou_sustentacao` | Transcrição | Suporte 24/7, SLA ou sustentação além da garantia → `true`. **Não rejeita** (22/10): vira alerta de contrato de manutenção à parte |
| `infra_cliente_sem_acesso` | Transcrição ("fica no nosso servidor", "nossa TI publica") | Infra do cliente sem acesso do NTec → `true`. **Não rejeita** (22/10): o projeto perde a garantia e o contrato diz isso |
| `sem_validador_nomeado` | Transcrição | Ninguém nomeado para testar e aprovar → `true`. 🚩 |
| `feature_sem_referencia_nem_doc` | Transcrição + protótipo | Feature sem referência citada **e** sem documentação pública → `true`. 🚩 |
| `hardware` | Transcrição + protótipo | Bluetooth com dispositivo próprio, IoT, leitor, impressora fiscal → `true`. 🚩 |
| `prazo_exigido_semanas` | Transcrição ("precisa estar pronto até…") | Semanas até a data, ou `null` |

Multa por atraso **saiu** do F0 em 22/10/2026 (não existe nos contratos do NTec): não pôr o campo no JSON.

**Depois F1 a F6:**

| Campo do JSON | Onde ler | Como traduzir |
|---|---|---|
| `formatos` | **Transcrição** ("baixar na loja", "pelo navegador", "no celular") | Ver `insumos-e-perguntas.md` (Formato). O protótipo não decide: Lovable é sempre web. Sem fala → lacuna; na dúvida entre PWA e app → app |
| `fluxos_por_formato` | Perfil × formato | Só com mais de um formato. O fluxo que só um perfil usa vive no formato daquele perfil; dúvida → `"compartilhado"` |
| `lojas` | Transcrição | App público na loja → `"normal"`, ou `"sensivel"` com dado de saúde, financeiro ou de menores. Uso interno → `"nao"`. Silêncio → `"normal"` + `"lojas"` em `lacunas_fathom` |
| `niveis_acesso` | Protótipo (menus por perfil, troca de perfil, telas de aprovação) + transcrição | Contar os perfis (admin conta). Teste de `fatores/F2-acesso-multitenancy.md` |
| `multitenancy` | Transcrição ("cada unidade", "várias empresas") | Teste de `fatores/F2-acesso-multitenancy.md`. Regra própria por tenant → `"instancias"`: **parada obrigatória** (🚩) |
| `fluxos_comuns` | Inventário de telas, agrupado em jornadas (Passo 3) | Tirar login e cadastro de conta (F2) e publicação (F5/F6). Registrar o agrupamento em *Suposições*: "Jornada 'agendar consulta' = telas Agenda, Horários, Confirmação" |
| `fluxos_rn_especifica` | Transcrição: cálculo, fórmula, regra clínica, legal ou de dinheiro **do cliente** | A jornada sai de `fluxos_comuns` e entra aqui. Uma vez por jornada. Concorrência, imutabilidade e rotina agendada também (tabela do Passo 3 de `leitura-prd.md`) |
| `features_atipicas` | Transcrição + protótipo | Tempo real por push, construtor de relatório, feature sem benchmark (`leitura-prd.md`, Passo 3) |
| `integracoes` | Transcrição (o cliente nomeia o sistema) + botões do protótipo | Peso fixo de `fatores/F3-integracoes.md`, sem perguntar sobre documentação. Botão no protótipo **sem** fala → lacuna de escopo (Passo 3), não integração |
| `dependencia_dados` | Transcrição ("a gente tem uma planilha com…", "o sistema antigo") | Migrar, limpar ou cruzar dado que já existe fora → `true` + núcleo de Dados |
| `offline` | Transcrição | Só consulta → `"local"`; grava e sincroniza → `"sync"`. Silêncio → `"nao"` |
| `volume_alto` | Transcrição | Milhares simultâneos ou picos → `true` |
| `rn_critica` | Transcrição | O código do NTec calcula dinheiro, dose, dado clínico, prazo legal ou fiscal → `true` |
| `demanda_pouco_detalhada` | Tudo | Ver `fatores/F1-imersao-setup.md`, 1.2 (critérios para transcrição + protótipo) |
| `stack_fora_template`, `deploy_infra_cliente` | Transcrição | Como no F0. Silêncio → `false` (stack do template como premissa) |
| `atipico` | Transcrição ("tipo o…", "igual ao…") | Referência citada → `false`. Nenhuma → `true` + lacuna |

---

## Passo 5 — Perguntas ao CN em vez de gordura

Ao fim da leitura, a skill **critica a clareza** antes de fechar o número. Para cada ambiguidade, uma pergunta pronta, a resposta que muda a conta e quanto muda:

```
| # | O que ficou ambíguo | Pergunta para o cliente | Se sim | Se não |
| 1 | Tela "Relatórios" está no protótipo, ninguém falou dela | "O relatório de vendas entra no MVP?" | +1,25 sem. | 0 |
```

No máximo 5 por rodada, as que mais mexem no prazo primeiro. Com o CN respondendo no chat, trocar o valor, mudar a origem para `(CN, no chat)` e rodar o script de novo. Sem resposta, a proposta sai com elas na seção 11 e o status ⚠️.

---

## Passo 6 — Depois do contrato: a PRD

A PRD vem **por último**: o CN gera o documento de requisitos (skill `documento-requisitos-ntec`) depois da assinatura, a partir das mesmas transcrições e do protótipo. Se rodarem esta skill de novo com a PRD (`leitura-prd.md`), comparar com o dimensionamento da proposta: diferença de mais de 1 sprint vai para a área de projetos, com o motivo (jornada nova, regra nova, integração nova). A PRD não pode **acrescentar** escopo ao que foi vendido sem aditivo.
