# Leitura das transcrições e do protótipo — a entrada padrão

✅ **Reunião "Validação Entregas Tec" (22/10/2026):** o dimensionamento sai direto das **transcrições das reuniões de diagnóstico** (normalmente duas) e do **protótipo navegável** (Lovable, Claude, v0, Figma…). A PRD **não** é pré-requisito: ela é gerada depois da assinatura, como anexo de contrato, e serve para revalidar o número (`leitura-prd.md`).

Por que mudou: contar módulos da PRD media o estilo de quem escreveu o documento, não o trabalho. E ambiguidade na PRD virava gordura na conta (Projeto CTE: 17 sprints, com 13 a 14 esperadas). Agora a skill conta **jornadas** que o cliente pediu, e **toda dúvida vira pergunta para o CN, fora da venda**, nunca semana a mais escondida no número.

Este arquivo diz onde, nas transcrições e no protótipo, está cada campo do JSON do `scripts/calcular_faixa.py`, e **qual é o valor de cada campo quando ninguém falou dele** (Passo 4). Essa tabela do silêncio é a única: os arquivos de `fatores/` apontam para ela. **Todo campo é obrigatório:** o script não tem valor padrão.

---

## Regra zero — sem alucinação de contexto

Tudo que entra no JSON e na proposta precisa de **uma** destas origens, escrita ao lado:

| Origem | Como citar |
|---|---|
| Fala numa transcrição | `(T1 · 00:12:30 — "a Ana valida toda sexta")`. Sem marcação de tempo: `(T1 — "trecho")` |
| Tela do protótipo | `(Protótipo · tela "Agenda da clínica")` ou `(Protótipo · rota /admin/agenda)` |
| Resposta do CN no chat | `(CN, no chat)` |
| Resumo de reunião, quando não há transcrição | `(resumo T1 — "trecho do resumo")`. Deixa o status ⚠️ preliminar (Passo 1) |
| Silêncio | `(silêncio — valor do Passo 4)` + a pergunta em `a_confirmar` |
| Regra da skill | `(regra de peso fixo)`, `(fronteira — linha mais pesada)` |

Proibido:
- **Completar o produto com o que "normalmente tem"** (tela de relatórios, painel admin, notificações, histórico). Se ninguém falou e o protótipo não mostra, não existe.
- **Ler intenção no tom da conversa.** "Seria legal ter…", "quem sabe depois", "vamos ver" não é escopo. **Silêncio também não é aceite:** o cliente não ter reclamado de uma tela não quer dizer que pediu.
- **Tratar dado fictício do protótipo como integração real.** Um card "Pago via Pix" com dado inventado não prova que existe integração de pagamento: precisa de fala na transcrição.
- **Misturar projetos.** Se a transcrição cita outro cliente ou outro projeto da Poli como exemplo, aquilo não entra no escopo.
- **Pôr dúvida na venda.** O que não tem citação fica no valor do silêncio e vai para `a_confirmar` (Passo 5).

Se uma citação não puder ser encontrada de novo no texto, ela não existe: tire o item.

---

## Passo 1 — O que o CN manda

| Peça | Como usar |
|---|---|
| **Transcrições das reuniões de diagnóstico** (Fathom, Granola, Meet, Teams; texto colado, `.txt`, `.md`, `.docx` ou PDF) | Fonte do **escopo pedido** e de tudo que é do **projeto** (quem valida, stack, infra, lojas, prazo, contrato, referências). Numerar na ordem das datas: T1, T2… |
| **Protótipo navegável** (link, código exportado, prints ou vídeo) | Fonte das **telas e perfis** que o cliente viu. Ver o Passo 2. Sozinho, não põe nada na conta (Passo 3) |
| Resumo da reunião (anotações do Gemini, do Fathom) | Com a transcrição junto: só para achar o trecho; cita-se a transcrição. **Sem a transcrição:** usar o resumo e marcar ⚠️ preliminar |
| Formulário Dimensionamento Tec, ficha, briefing | Complemento. Vocabulário e perguntas em `insumos-e-perguntas.md` |
| PRD (se já existir) | Conferência, nunca contagem de módulo. Divergência com transcrição/protótipo vai para *Pontos de atenção* |

**O que precisa ter para dimensionar:**

| Chegou | O que a skill faz |
|---|---|
| Transcrições + protótipo | Caminho padrão. Status pode ser ✅ (se não sobrar pergunta em aberto) |
| Só transcrições | Dimensiona, status ⚠️ *Estimativa preliminar: falta o protótipo*. Pede o protótipo ao CN |
| Só o resumo das reuniões (sem transcrição), com ou sem protótipo | Dimensiona, status ⚠️ *Estimativa preliminar: só o resumo das reuniões*. Cita `(resumo T1)`. Pede a transcrição completa antes de fechar a proposta |
| Só protótipo | **Não dimensiona.** O protótipo não diz nada do projeto (quem valida, lojas, infra, prazo) nem o que o cliente pediu. Pedir as transcrições |
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

A coluna **Citada em** liga a tela à fala: `T2 · 00:18:10` ou `não citada`. "Citada" quer dizer que alguém **falou da tela ou do que ela faz** na gravação, não só que ela passou na tela durante a demo.

**Qual versão do protótipo vale** (✅ decisão de 22/10/2026): a que foi **mostrada ao cliente** na reunião gravada. Sem essa informação, o **link publicado** que o CN mandou. Se o código exportado, um print ou outra versão tiver telas ou campos que a versão válida não tem, eles **não** entram na conta e viram pergunta em `a_confirmar` ("o cliente viu e pediu X?"). Registrar no inventário qual versão foi usada.

**Protótipo é desenho, não especificação.** Ele diz *quais* telas o cliente viu e *quem* as usa. Não diz formato (todo protótipo do Lovable é web, mesmo que o produto seja app), offline, volume, nem se o botão "Enviar no WhatsApp" é um link ou uma integração. Essas respostas vêm da transcrição.

---

## Passo 3 — Cruzar protótipo × transcrição: o que é escopo

A unidade de contagem é a **jornada** (glossário, *Jornada*): **perfil + objetivo + entidade principal**, com a regra de agrupamento do glossário (cadastro auxiliar não conta; 3+ entidades ou 6+ telas próprias contam 2). Contar jornadas, nunca telas nem menus.

| Situação | Entra na conta? | O que fazer |
|---|---|---|
| Jornada no protótipo **e** pedida na transcrição | Sim | Citar as duas origens |
| Jornada no protótipo, mostrada numa reunião gravada **e comentada** pelo cliente (ele fala dela, pede ajuste, aprova em voz alta) | Sim | Citar o trecho com a marcação de tempo |
| Jornada no protótipo que **só passou na tela** durante a demo, sem nenhuma fala sobre ela | **Não** | `a_confirmar`. O cliente não reclamar não é pedido |
| Jornada só no protótipo, **sem nenhuma** menção nas reuniões | **Não** | `a_confirmar` com o efeito `jornada` e uma pergunta pronta. Prototipadores com IA criam telas que ninguém pediu: contar isso é a gordura que a reunião de 22/10 mandou tirar |
| Perfil só no protótipo (seletor de perfil, usuário de demonstração), sem fala | **Não** | `a_confirmar` com `"troca": {"niveis_acesso": ...}` |
| Jornada pedida na transcrição, **sem tela** no protótipo, com fala que diz quem faz e o que sai no fim | Sim | Ponto de atenção: "o protótipo não cobre X" |
| Jornada pedida na transcrição, sem tela, com **fala vaga** | **Não** | `a_confirmar` |
| Cliente disse que **não** quer, ou "fica para depois" | Não | Vai para *Futuro* no roadmap |
| Duas reuniões discordam | Vale a **mais recente** | Divergência em *Pontos de atenção*. Se não der para saber qual vale, a mais leve vai na conta e a outra vai para `a_confirmar` |

**Uma regra só para toda dúvida:** o que as reuniões não decidem (escopo ambíguo **ou** fator de projeto sem resposta) **não entra na venda**. Vai na conta com o valor do silêncio (Passo 4) e para `a_confirmar` com o efeito se a resposta for sim. O script mostra a venda "+ até X" e cada pergunta com o custo. **Exceção:** quem valida as entregas (F0): o silêncio vira 🚩, que não soma semanas mas segura a proposta.

**A linha mais pesada continua valendo só para classificar** um fator **citado** que encaixa em duas linhas (ex.: o cliente falou "no celular" sem dizer loja → app; falou do ERP sem dizer o sentido → bidirecional). Nunca para decidir **se** uma coisa entra.

---

## Passo 4 — Onde está cada campo do JSON, e o valor no silêncio

**Primeiro o F0** (`fatores/F0-viabilidade.md`):

| Campo do bloco `"f0"` | Onde ler | Como traduzir | Silêncio |
|---|---|---|---|
| `stack_exigida_fora_da_lista` | Transcrição ("tem que ser em…", "nossa TI só aceita…") | `true` só se o cliente **exige**. "Vocês decidem" → `false`. 🚫 rejeita | `false` |
| `offline_sync_com_mongodb_exigido` | Transcrição | Grava sem internet para subir depois **e** o cliente exige MongoDB → `true`. 🚫 rejeita | `false` |
| `sla_ou_sustentacao` | Transcrição | Suporte 24/7, SLA ou sustentação além da garantia → `true`. 📝 contrato de manutenção à parte | `false` |
| `infra_cliente_sem_acesso` | Transcrição ("fica no nosso servidor", "nossa TI publica") | Infra do cliente sem acesso do NTec → `true`. 📝 sem garantia | `false` |
| `sem_validador_nomeado` | Transcrição | Ninguém nomeado para testar e aprovar → `true`. 🚩. Cliente pessoa física que revisa o protótipo → `false` (F0, 0.3) | **`true`** (🚩, não soma semanas) |
| `feature_sem_referencia_nem_doc` | Transcrição **e** confirmação do CN | Só `true` com fala ("ninguém faz isso") **e** o CN confirmando. 🚩 | `false` |
| `hardware` | Transcrição + protótipo | Bluetooth com dispositivo próprio, IoT, leitor, impressora fiscal → `true`. 🚩 | `false` |
| `prazo_exigido_semanas` | Transcrição ("precisa estar pronto até…") | Semanas entre a data de início prevista e a data limite (sem início citado: a partir de hoje, em *Suposições*) | `null` |

Multa por atraso **saiu** do F0 em 22/10/2026 (não existe nos contratos do NTec): não pôr o campo no JSON.

**Depois F1 a F6.** Coluna **Silêncio**: o valor que vai na venda quando ninguém falou; **Pergunta em `a_confirmar`**: o efeito se a resposta for sim.

| Campo do JSON | Onde ler | Como traduzir | Silêncio | Pergunta em `a_confirmar` |
|---|---|---|---|---|
| `formatos` | **Transcrição** ("baixar na loja", "pelo navegador", "no celular") | O protótipo não decide: Lovable é sempre web. Dúvida entre PWA e app → app (fronteira) | **Não dimensionar**: perguntar ao CN antes | — |
| `fluxos_por_formato` | Perfil × formato, pela transcrição | Só com mais de um formato. A jornada de um perfil que só usa um código vive nele | Dúvida → `"compartilhado"` (classificação) | — |
| `fluxos_comuns` | Inventário agrupado em jornadas (Passo 3 + glossário) | Só as jornadas que passaram no Passo 3. Agrupamento em *Suposições* | Não conta | `"jornada": {"tipo": "comuns", "formato": ..., "quantas": n}` |
| `fluxos_rn_especifica` | Transcrição: fórmula, tabela, norma, protocolo **do cliente**; concorrência; imutabilidade; rotina agendada | A jornada sai de `fluxos_comuns` e entra aqui. Uma vez por jornada | Fluxo comum | Regra citada sem detalhe: `"vira_rn_especifica": {"formato": ..., "quantas": 1}` |
| `features_atipicas` | Transcrição + protótipo | Pedidas nas reuniões e na lista do glossário (tempo real, construtor de relatório) | 0 | `"jornada": {"tipo": "atipicas", ...}` |
| `niveis_acesso` | Transcrição (quem usa) + protótipo (telas de cada perfil) | Contar os perfis **citados** (admin conta). Teste de `fatores/F2-acesso-multitenancy.md` | Só os citados; testes a, b, c = não | Perfil ou diferença só no protótipo: `"troca": {"niveis_acesso": ...}` |
| `multitenancy` | Transcrição ("cada unidade", "várias empresas") | Teste de `fatores/F2-acesso-multitenancy.md`. Regra própria por tenant → `"instancias"` (🚩) | Ninguém falou: `"nao"`. Citado sem detalhe: `"separado"` | `"troca": {"multitenancy": "isolado"}` e `{"multitenancy": "instancias"}` |
| `integracoes` | Transcrição (o cliente nomeia o sistema) | Peso fixo de `fatores/F3-integracoes.md`. Sentido não dito → bidirecional (classificação) | Não conta. Botão do protótipo sem fala também não | Citada de forma vaga: `"integracao": "<linha>"` |
| `dependencia_dados` | Transcrição ("a gente tem uma planilha com…", "o sistema antigo") | Migrar, limpar ou cruzar dado que já existe fora → `true` + núcleo de Dados | `false` | Citada sem dizer se migra: `"troca": {"dependencia_dados": true}` |
| `offline` | Transcrição | Só consulta → `"local"`; grava e sincroniza → `"sync"`; "sem internet" + nada salvo → `"local"` (F3, Offline) | `"nao"` | Sinal ruim citado sem detalhe: `"troca": {"offline": "sync"}` |
| `volume_alto` | Transcrição | 1.000+ simultâneos ou pico com data → `true` | `false` | "Muita gente" sem número: `"troca": {"volume_alto": true}` |
| `rn_critica` | Transcrição | O código do NTec calcula dinheiro, dose, dado clínico, prazo legal ou fiscal → `true` | `false` | Cálculo citado sem dizer quem calcula: `"troca": {"rn_critica": true}` |
| `demanda_pouco_detalhada` | Tudo | `fatores/F1-imersao-setup.md`, 1.2 | Pelas perguntas do 1.2 | — |
| `stack_fora_template` | Transcrição | Exige tecnologia da lista aceita que não é a do template | `false` (template como premissa) | `"troca": {"stack_fora_template": true}` |
| `deploy_infra_cliente` | Transcrição ("nossos servidores", "a TI aprova") | Infra do cliente | `false` (infra do NTec) | `"troca": {"deploy_infra_cliente": true}` |
| `atipico` | Transcrição | `true` só se disseram que **não existe** nada parecido com o produto | `false` | "Existe app parecido?": `"troca": {"atipico": true}` |
| `lojas` | Transcrição | Loja aberta → `"normal"`, ou `"sensivel"` (`fatores/F6-lojas.md`; app clínico ou de dose é sensível pela natureza). Uso interno → `"nao"` | `"nao"` | `"troca": {"lojas": "normal"}` (ou `"sensivel"`) |

---

## Passo 5 — Perguntas ao CN em vez de gordura (`a_confirmar`)

Ao fim da leitura, a skill **critica a clareza** antes de fechar o número. Cada dúvida vira um item de `a_confirmar` no JSON, com o efeito se a resposta for sim. **O custo é do script, nunca de cabeça:**

```json
"a_confirmar": [
  {
    "o_que": "Tela \"Relatórios\" está no protótipo, ninguém falou dela (Protótipo · tela \"Relatórios\")",
    "pergunta": "O relatório de vendas entra no MVP?",
    "efeito": {"jornada": {"tipo": "comuns", "formato": "web", "quantas": 1}}
  },
  {
    "o_que": "ERP citado de passagem, sem dizer se troca dados (T1 · 00:40:12 — \"lá a gente usa o Bling\")",
    "pergunta": "O sistema precisa mandar ou receber dados do Bling automaticamente?",
    "efeito": {"integracao": "bi_sem_doc"}
  },
  {
    "o_que": "Ninguém falou de loja",
    "pergunta": "O app precisa estar na App Store ou na Play Store?",
    "efeito": {"troca": {"lojas": "normal"}}
  }
]
```

Efeitos possíveis (podem se combinar no mesmo item):

| Efeito | Para quê |
|---|---|
| `"jornada": {"tipo": "comuns" \| "rn_especifica" \| "atipicas", "formato": ..., "quantas": n}` | Jornada ou feature que ainda não está na conta |
| `"vira_rn_especifica": {"formato": ..., "quantas": n}` | Jornada já contada como comum que vira RN específica |
| `"integracao": "<linha>"` | Integração citada de forma vaga |
| `"troca": {"campo": valor}` | Qualquer outro fator (lojas, atipico, multitenancy, offline…) |

O script imprime a venda "**+ até X** que dependem de N perguntas em aberto" e, para cada pergunta, quanto ela soma no provável e na venda (e se vira 🚩). Na resposta ao CN, mostrar **as 5 que mais mexem no prazo** primeiro; todas vão para a seção 11 da proposta.

Com o CN respondendo no chat: resposta **sim** → aplicar o efeito no JSON e tirar o item; **não** → só tirar o item. Mudar a origem para `(CN, no chat)` e rodar o script de novo. **Enquanto houver item em `a_confirmar`, o status é ⚠️** e a proposta não vai para o cliente.

---

## Passo 6 — Depois do contrato: a PRD

A PRD vem **por último**: o CN gera o documento de requisitos (skill `documento-requisitos-ntec`) depois da assinatura, a partir das mesmas transcrições e do protótipo. Se rodarem esta skill de novo com a PRD (`leitura-prd.md`), comparar com o dimensionamento da proposta: diferença de mais de 1 sprint vai para a área de projetos, com o motivo (jornada nova, regra nova, integração nova). A PRD não pode **acrescentar** escopo ao que foi vendido sem aditivo.
