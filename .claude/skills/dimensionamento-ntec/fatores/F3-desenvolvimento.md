# F3 — Desenvolvimento: fluxos, formato e extras

**Baseline do formulário:** 1 a X semanas. É a fase que mais varia. Sem teto.

✅ **Reunião 20/10:** integrações e fluxos são **tópicos separados**. As integrações estão em `F3-integracoes.md`.

✅ **Reunião 20/10:** o fator Claude Code (×0,6 / ×0,75 / ×0,9 no núcleo) foi **removido**.

**Onde ler:** transcrições + protótipo (caminho padrão). Na revalidação, a PRD. O silêncio de cada campo está em `leitura-transcricoes-prototipo.md`, Passo 4.

**Conta do F3:**

```
F3 = Σ (fluxos de cada código × fator daquele código) + integrações + extras [+ margem, ver D3]
fluxos = fluxos comuns + fluxos com RN específica + features atípicas
```

---

## 3.1 Núcleo — contar as jornadas

### Passo 1: quantas jornadas

✅ **Reunião 22/10/2026:** contar módulos media o estilo de quem escreveu, não o trabalho. A unidade é a **jornada** (glossário, *Jornada*), contada pela mesma regra fechada para qualquer CN:

| # | Passo | Onde ler |
|---|---|---|
| 1 | Montar o inventário de telas do protótipo | `leitura-transcricoes-prototipo.md`, Passo 2 |
| 2 | Agrupar as telas em jornadas: **perfil + objetivo + entidade principal**. Listar, ver, criar, editar e excluir a mesma entidade pelo mesmo perfil = 1 | Inventário + transcrições |
| 3 | Juntar o **cadastro auxiliar** (categorias, tipos, status, configurações simples) na jornada que o usa. Tirar login e cadastro de conta (F2), publicação (F5/F6) e telas de offline (extra de offline) | Inventário |
| 4 | Jornada que cruza **3 ou mais entidades principais** ou tem **mais de 6 telas próprias** conta **2** | Inventário |
| 5 | Separar o que **entra** (pedida ou comentada na gravação) do que vai para `a_confirmar` (só no protótipo) | `leitura-transcricoes-prototipo.md`, Passo 3 |
| 6 | Registrar cada agrupamento em *Suposições*, com as telas ("Jornada 'recepção gerencia a agenda' = Agenda, Detalhe, Remarcar") | — |

**Jornada pedida na transcrição e sem tela no protótipo:** entra, se a fala diz quem faz e o que sai no fim. Se a fala for vaga, vai para `a_confirmar`.

**Sem jornada nenhuma citada, não dimensionar.** Pedir ao CN as jornadas completas (`insumos-e-perguntas.md`).

> 🔎 **Proposta:** os limites 3 entidades e 6 telas precisam ser calibrados no primeiro projeto rodado por este caminho (CTE). **Na revalidação (PRD):** a regra das folhas e dos 8 itens A(cli)D (glossário) continua valendo para conferir o número.

### Passo 2: cada jornada é comum ou tem RN específica?

| Pergunta | Onde ler | Se sim |
|---|---|---|
| O cliente precisa entregar uma **fórmula, tabela, norma ou protocolo escrito** para essa jornada funcionar? | Transcrições ("a conta é feita assim…", "segue a norma X", "tem uma planilha com a fórmula") | RN específica |
| A jornada tem **concorrência** ("o primeiro que aceitar leva") ou **imutabilidade** (registro que não se edita, versionamento)? | Transcrições | RN específica |
| Nenhuma das duas | — | Fluxo comum |

**Regra citada sem detalhe** ("tem um cálculo lá", "depende de umas regras"): fluxo **comum** na venda + pergunta em `a_confirmar` com `"vira_rn_especifica": {"formato": "<código da jornada>", "quantas": 1}` (a jornada já contada passa de comum para RN específica; não soma outra). Se a regra mexe com dinheiro, dose, dado clínico, prazo legal ou fiscal, o mesmo item leva também `"troca": {"rn_critica": true}`.

**Não é RN específica:** validação padrão de mercado (CPF, CNPJ, CEP, e-mail), "cálculo que não pode errar" sem documento, só envolver dinheiro, ou **gerar um documento num template fixo** (relatório, contrato, certificado), inclusive em mais de um formato (PDF, Word, Excel). Template fixo e exportação fazem parte da jornada: o fluxo é comum. Template que o usuário monta ou edita é *relatório configurável* (feature atípica).

**Não usar a fronteira aqui.** "Na dúvida, linha mais pesada" (`regra-fronteira-e-faixa.md`) só vale quando as perguntas acima não decidem. Se a resposta das perguntas é "não", o fluxo é comum, mesmo que a jornada pareça trabalhosa.

**Conta uma vez por jornada**, mesmo com várias RNs.

**Rotina agendada** (roda sozinha por horário): hoje transforma o fluxo em RN específica (+1,75 no central).
> 🔎 **Proposta:** é desproporcional para um agendamento simples. Sugestão: +0,5 no fluxo em vez de trocar de linha. **Até validar:** continua virando RN específica.

### Passo 3: features atípicas

| Pergunta | Onde ler | Sem resposta |
|---|---|---|
| Quantas features **pedidas nas reuniões** estão nesta lista: tempo real por aviso do servidor (chat, rastreio ao vivo, push em tempo real), relatório configurável pelo usuário (construtor)? | Transcrições + protótipo | 0 |
| Alguma feature pedida **não tem referência** ("nunca vi isso em lugar nenhum")? | Transcrições | Ninguém disse que não existe → não é atípica. Se o CN ou o cliente disseram → pergunta em `a_confirmar`: "Existe algum app que já faça {feature}?", com `"jornada": {"tipo": "atipicas", ...}` |

É uma **contagem** de features, não semanas. Feature sem referência **e** sem documentação técnica pública vai para o **F0** só quando o CN confirmar as duas coisas (`F0-viabilidade.md`, 0.4).

### Tabela do núcleo

| Item (por unidade) | Mín | Central | Máx |
|---|---|---|---|
| Fluxo comum | 1 | 1,25 | 1,5 |
| Fluxo com RN específica | 2 | 3 | 4 |
| Feature atípica | 1 | 1,5 | 2 |

---

## 3.2 Fator de formato

**O protótipo não decide o formato** (Lovable e v0 são sempre web). O formato vem da fala do cliente.

| Pergunta | Onde ler | Resultado |
|---|---|---|
| Precisa estar na App Store ou Play Store, **ou** usa Bluetooth, GPS em segundo plano, NFC, notificação com o app fechado em iOS ou sensores? | Transcrições ("baixar na loja", "app na Play Store", "funcionar com o celular no bolso") | App nativo |
| Instala pelo navegador (ícone na tela), sem loja? | Transcrições ("atalho no celular", "não precisa de loja") | PWA |
| Só abre no navegador | Transcrições ("pelo computador", "acessa pelo link") | Web |
| Quantos **códigos separados** vão para o ar? | Transcrições: quem usa o quê, e onde ("o motorista no celular, o escritório no computador") | Cada código além do primeiro é um formato extra |

**Sem fala sobre o formato:** não dimensionar; perguntar ao CN (`insumos-e-perguntas.md`, *Quando parar*). O formato é escopo central e não vai para `a_confirmar`.

**Fala ambígua entre PWA e app** ("no celular", sem dizer loja): **app**. O cliente citou o celular, então é a classificação de um fator citado, e aí vale a linha mais pesada (`regra-fronteira-e-faixa.md`, tipo 3). A publicação nas lojas fica de fora até alguém falar de loja (`F6-lojas.md`).

| Formato | Fator |
|---|---|
| Web | ×1,0 |
| PWA | ×1,1 |
| App nativo | ×1,2 |
| Fluxo que existe em mais de um código (`compartilhado`) | fator do formato mais pesado + ⏳ **D1** por formato extra |

O `webapp` do script deixa de existir: vira PWA se instala, web se não instala.

### Fator por fluxo (revisão de 22/10/2026)

**Cada jornada recebe o fator do código em que existe.** Com mais de um formato, o JSON leva `fluxos_por_formato`, dizendo quantas jornadas estão em cada código:

| Pergunta (para cada jornada) | Onde ler | Chave |
|---|---|---|
| A jornada é de um perfil que só usa um código (ex.: o consultor só no app, o admin só no painel)? | Transcrições (quem usa onde) | O formato daquele código (`app`, `pwa`, `web`) |
| A jornada tem tela nos dois códigos (ex.: o tutor agenda no app e a recepção gerencia a mesma agenda no painel)? | Transcrições + protótipo | `compartilhado` |
| Não dá para saber | — | `compartilhado` (linha mais pesada: é classificação de um fator citado, não escopo) |

```json
"formatos": ["app", "pwa"],
"fluxos_por_formato": {
  "app":           {"comuns": 3, "rn_especifica": 0, "atipicas": 0},
  "pwa":           {"comuns": 5, "rn_especifica": 1, "atipicas": 0},
  "compartilhado": {"comuns": 0, "rn_especifica": 0, "atipicas": 0}
}
```

A soma de cada coluna tem de bater com `fluxos_comuns`, `fluxos_rn_especifica` e `features_atipicas` (o script confere). Com um formato só, o campo não entra.

**Por quê:** antes, o fator de app + painel (×1,4) multiplicava **todos** os fluxos. Quando cada jornada vive num código só (consultor só no app, admin só no painel), o segundo código já está pago pelos fluxos dele, e o ×1,4 cobrava de novo. No Projeto G isso somava ~4 semanas. O custo de ter dois códigos que não está nos fluxos (setup e deploy do segundo código) já está no F1 e no F5.

✅ **Reunião 20/10:** o antigo "+0,1 por formato extra" é pouco. Deve ser **pelo menos 1,2**. Agora ele vale só para os fluxos `compartilhado`.

> ⏳ **D1 — em aberto:** "pelo menos 1,2" quer dizer:
> - (a) **+0,2 por formato extra**: app + painel web = 1,2 + 0,2 = **×1,4**; ou
> - (b) **×1,2 sobre o fator**: app + painel web = 1,2 × 1,2 = **×1,44**.
>
> **Provisório:** (a), +0,2 por formato extra.

Os prazos de desenvolvimento **não** incluem a publicação nas lojas (que é F6).

---

## 3.3 Extras (somam depois do fator de formato)

| Item | Mín | Central | Máx | Alerta |
|---|---|---|---|---|
| Dependência de dados | +1 | +1,5 | +2 | ⚠️ Chamar o núcleo de Dados |
| Offline local | 0 | 0 | 0 | |
| Offline com sincronização | +1,5 | +2 | +3 | ⚠️ Postgres, não MongoDB (ver F0, item 0.2) |
| Volume alto | +1 | +1,5 | +2 | ⚠️ Requisitos de performance por escrito |

### Dependência de dados

| Pergunta | Onde ler | Sem resposta |
|---|---|---|
| O projeto depende de dados que **já existem fora do sistema** (planilha legada, base pública, sistema antigo) e precisam ser **migrados, limpos ou convertidos** para o produto funcionar? | Transcrições ("hoje está tudo numa planilha", "tem o histórico no sistema antigo", "puxar a tabela do governo") | Ninguém falou → `false`. Citado sem dizer se precisa migrar ("a gente tem uma planilha") → `false` + pergunta em `a_confirmar` com `"troca": {"dependencia_dados": true}` |

**Não é dependência de dados** (é parte da jornada, 0 a mais): um **upload simples feito pelo usuário dentro do produto**, com formato fixo, que vira registros na hora (ex.: planilha de uma coluna em que cada linha vira uma pergunta). Sinais: o formato do arquivo é fixo, não há conversão de unidades nem cruzamento com outra base, e a importação é uma tela do produto, não uma tarefa do projeto.

É dependência de dados quando há pelo menos um destes: migração do histórico do cliente; base pública ou externa a tratar; conversão de unidades ou de formatos; cruzamento entre bases; dado sujo que precisa de limpeza. Nesses casos chamar o núcleo de Dados.

Se a importação roda **sozinha**, sem ninguém disparar, é integração (`F3-integracoes.md`), não dependência de dados.

### Offline

| Pergunta | Onde ler | Resultado |
|---|---|---|
| O app **grava** algo sem internet para subir depois? | Transcrições ("no campo não tem sinal", "registra e manda depois") | Offline com sincronização |
| O app só **lê** sem internet o que já está no aparelho? | Transcrições | Offline local |
| Ninguém falou de internet ou sinal | — | Nenhum (0) |
| Falaram de sinal ruim sem dizer o que o app faz sem internet | Transcrições | Nenhum (0) + pergunta em `a_confirmar` com `"troca": {"offline": "sync"}` |

> 🔎 **Proposta:** baixar dados do servidor para consultar offline já é uma sincronização de mão única e tem custo. Sugestão: offline local com leitura de dados do servidor = +0,5 / +0,5 / +1. **Até validar:** 0.

✅ **Reunião 20/10:** offline com sincronização **não** se vende com MongoDB. A proposta registra Postgres como premissa (ver ⏳ **D5** no F0).

### Volume alto

| Pergunta | Onde ler | Sem resposta |
|---|---|---|
| Alguma transcrição cita **1.000 ou mais usuários ao mesmo tempo**, ou um pico com data (evento, lançamento, campanha)? | Transcrições | `false`. "Muita gente vai usar" sem número → `false` + pergunta em `a_confirmar` com `"troca": {"volume_alto": true}` |

> 🔎 **Proposta:** o limite de 1.000 precisa ser validado pela área técnica.

---

## 3.4 Margem de segurança ("gordura")

✅ **Reunião 20/10:** o dimensionamento deve ter uma **margem de segurança explícita** contra imprevistos, em vez de prazo justo. Se o time entregar antes, o tempo vira over delivery para o cliente.

✅ **Reunião 22/10:** a margem **não pode vir das dúvidas**. No CTE, ambiguidades tratadas como margem deram 17 sprints com 13 a 14 esperadas. Dúvida vai para `a_confirmar`, fora da venda. Se o NTec quiser margem, ela é um número explícito (D3), igual para todo projeto.

> ⏳ **D3 — em aberto:** onde e quanto?
> - (a) percentual sobre o F3 (🔎 sugestão: +10% a +15% no central);
> - (b) percentual sobre o total;
> - (c) embutida nos centrais de cada linha.
>
> **Provisório:** sem margem extra na conta. A resposta ao CN avisa: "Margem de segurança ainda não definida pelo NTec (D3)."
