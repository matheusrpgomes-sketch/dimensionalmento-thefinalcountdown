# Leitura da PRD — do documento de requisitos para os fatores da régua

> **Desde 22/10/2026 a PRD não é mais a entrada padrão.** A skill dimensiona a partir das transcrições das reuniões de diagnóstico + o protótipo navegável (`leitura-transcricoes-prototipo.md`). A PRD vem **por último**, depois da assinatura do contrato, e este arquivo serve para **revalidar** o dimensionamento quando ela existir. Regras que continuam valendo daqui no caminho padrão: a tabela do Passo 3 (fatores de complexidade → linhas da régua) e o "não contar duas vezes". **Nunca contar módulos da PRD:** a quantidade de módulos depende de quem escreveu, não do trabalho. Contar jornadas.

A **PRD** (Documento de Requisitos de produto do NTec) é gerada pela skill `documento-requisitos-ntec` ([repositório](https://github.com/rivasaugustus/documento-requisitos-ntec)) a partir das reuniões com o cliente e vira anexo de contrato.

Este arquivo diz onde, na PRD, está cada campo do JSON do `scripts/calcular_faixa.py`. O critério completo de cada fator (pergunta, onde ler, o que fazer sem resposta) está no arquivo da fase em `fatores/`; se este arquivo e `fatores/` divergirem, vale `fatores/`. **Todo campo é obrigatório:** o script não tem valor padrão e para se faltar algum.

---

## Passo 1 — O que o CN manda

| Peça | De onde vem | Como usar |
|---|---|---|
| **PDF "[Requisitos] {projeto}"** (ou o `.md` que gerou o PDF) | Saída da skill da PRD | **Fonte principal.** Seções 1 (Visão Geral), 2 (Requisitos Funcionais por módulo), 3 (Não Funcionais) e 4 (Exclusões) |
| **Bloco "Inventário para dimensionamento"** | Chat da skill da PRD, logo depois do PDF | Atalho: uma linha por módulo, com `Módulo \| Superfície \| Itens A(cli)D \| Itens SID \| Integrações \| Fluxos de dados \| Fatores de complexidade`. Se o CN não colar, **montar o inventário a partir do PDF** com as mesmas colunas |
| **Bloco "Pontos para a imersão"** | Chat da skill da PRD | Detalhes que não mudam o tamanho. Não somam prazo: entram como atividades da imersão (F1) na resposta |
| Blocos "Perfis de acesso", "Funcionalidades" e "Integrações" | Chat da skill da PRD | Conferência. As fontes (`[Fathom · AT 12/03]`, `[chat]`…) mostram de onde veio cada item |
| **Transcrições do Fathom** (ou resumo do Fathom/Granola) das reuniões com o cliente | As mesmas reuniões que geraram a PRD | Responder o Passo 4 sem perguntar ao CN. O que não estiver nelas vira **lacuna** |

**Sem PRD:** é o caminho padrão (`leitura-transcricoes-prototipo.md`). Não marcar nada como preliminar por falta de PRD.

**PDF e inventário divergem** (ex.: o inventário tem um módulo que o PDF não tem): vale o PDF, que é o anexo de contrato. Registrar a divergência em *Pontos de atenção*.

## Passo 2 — Onde está cada fator

**Primeiro o F0** (`fatores/F0-viabilidade.md`). Preencher o bloco `"f0"` antes do resto:

| Campo do bloco `"f0"` | Onde ler | Como traduzir |
|---|---|---|
| `stack_exigida_fora_da_lista` | 3.1; Fathom ("tem que ser em…") | `true` só se o cliente **exige** tecnologia fora da lista aceita do F0. "Vocês decidem" → `false`. 🚫 rejeita |
| `offline_sync_com_mongodb_exigido` | Termo "offline"; 3.1; Fathom | `true` se grava sem internet para subir depois **e** o cliente exige MongoDB. 🚫 rejeita |
| `sla_ou_sustentacao` | Seção 3; Fathom | Suporte 24/7, SLA ou sustentação além da garantia de 30 dias → `true`. Não rejeita: alerta de contrato de manutenção à parte (22/10/2026) |
| `infra_cliente_sem_acesso` | 3.1; Fathom | Roda na infra do cliente sem acesso do time do NTec para publicar e corrigir → `true`. Não rejeita: sem garantia, ajustar o contrato (22/10/2026) |
| `sem_validador_nomeado` | Fathom | `true` se ninguém do cliente foi nomeado para testar e aprovar. Sem Fathom, `true` + lacuna. 🚩 |
| `feature_sem_referencia_nem_doc` | Fatores de complexidade; Fathom | `true` se alguma feature não tem referência citada **nem** documentação técnica pública. 🚩 |
| `hardware` | PRD; Fathom | Bluetooth com dispositivo próprio, IoT, leitor, impressora fiscal → `true`. 🚩 |
| `prazo_exigido_semanas` | Fathom; briefing do CN | Número de semanas que o cliente exige, ou `null` se não exigiu. Abaixo do otimista → 🚩 |

Multitenancy com regra diferente por tenant e integração sem API também são critérios do F0, mas entram pelos campos `multitenancy: "instancias"` e `integracoes: ["sem_api"]` da tabela abaixo.

**Depois F1 a F6:**

| Fator da régua (campo do JSON) | Onde ler na PRD | Como traduzir |
|---|---|---|
| `formatos` | Linha `**Superfície:**` de cada módulo (ou o título da seção-mãe, ex.: "Fluxo do Consultor (Aplicativo Mobile)") + 3.1 *Ambientes de entrega* | `app mobile` → `"app"`. `site` ou `painel web` → `"web"` (ou `"pwa"` se a PRD disser que instala pelo navegador; `"webapp"` não existe mais). Cada formato entra uma vez. App mobile + painel web = dois formatos. Site + painel web no mesmo sistema = um formato só |
| `fluxos_por_formato` | Superfície de cada fluxo | **Só com mais de um formato.** Para cada fluxo: existe só num código → a chave daquele formato; tem tela nos dois → `"compartilhado"`; não dá para saber → `"compartilhado"`. Cada chave leva `{"comuns", "rn_especifica", "atipicas"}` e as somas batem com os três campos de contagem (`fatores/F3-desenvolvimento.md`, 3.2) |
| `lojas` | Módulo *Disponibilização do Produto* + 3.1 | Publicação na App Store ou Play Store → `"normal"`. Se a 3.4 fala de dado de saúde, financeiro ou de menores → `"sensivel"`. Sem loja → `"nao"` |
| `niveis_acesso` | 2.1 *Autenticação e Perfis de Acesso* | Contar os perfis (admin conta). 1 → `"1"`. 6 ou mais → `"6+"`. De 2 a 5, o teste de `fatores/F2-acesso-multitenancy.md` (tela exclusiva, status de cadastro ou filtro por dono → `"2-5-grandes"`; senão `"2-5-poucas"`). Sem 2.1 (sem login) → `"nenhum"` |
| `multitenancy` | Visão Geral, 2.1, RNs e 3.4 (termos: multiempresa, por unidade, por clínica, por filial) | Teste em ordem de `fatores/F2-acesso-multitenancy.md`: uma empresa só → `"nao"`. Regra ou funcionalidade diferente por empresa → `"instancias"` (🚩 F0). Vazamento entre empresas quebra contrato ou LGPD → `"isolado"`. Admin geral vê tudo → `"separado"`. Sem resposta → `"isolado"` + lacuna |
| `fluxos_comuns` | Folhas da seção 2 | **Contar jornadas, não a numeração** (glossário, *Fluxo*): partir das folhas (a subseção mais funda com itens A(cli)D), tirar 2.1 Autenticação (F2), *Disponibilização do Produto* (F5 e F6) e as folhas de offline quando `offline` não for `"nao"`; juntar folhas da mesma jornada; mais de 8 itens A(cli)D = 2 fluxos. Registrar as junções em *Suposições* |
| `fluxos_rn_especifica` | Módulos com `### Regras de Negócio` + coluna *Fatores de complexidade* | O módulo sai de `fluxos_comuns` e entra aqui quando tem RN de cálculo, fórmula, regra clínica, legal ou de dinheiro, ou quando tem um dos fatores da tabela do Passo 3 que viram RN específica. Conta **uma vez por módulo**, mesmo com várias RNs. **Relatório em template fixo** (PDF, Word, Excel) **não** é RN específica: "Hardcoded" e "template fixo" querem dizer que não há regra a configurar |
| `features_atipicas` | Coluna *Fatores de complexidade* | Só pelos fatores da tabela do Passo 3 que viram feature atípica. O "produto sem benchmark" não está na PRD: procurar no Fathom (Passo 4) |
| `integracoes` | Itens `**SID** integrar com…` (Sentido, Dados, Meio) + coluna *Integrações* | **Peso fixo, sem perguntar ao CN** (teste de `fatores/F3-integracoes.md`). Troca de arquivo disparada por uma pessoa não é integração, é `dependencia_dados`. Sentido `envia` ou `recebe` → unidirecional. `envia e recebe` → bidirecional. Serviço de mercado (documentação pública e sandbox que o NTec acessa sozinho) → `_doc`. Sistema do cliente (ERP, legado, sob medida, SaaS que depende da TI do cliente) ou dúvida → `_sem_doc`, com cláusula de contrato e plano B. `"sem_api"` (🚩 F0) se a PRD ou o Fathom disserem que o sistema não tem API, uni ou bi. Google, e-mail e upload de arquivo → `"template"`. Sem integração → `[]` |
| `dependencia_dados` | Fluxos com `**Origem:**` / `**Processamento:**` / `**Destino:**` | `true` (e chamar o núcleo de Dados) quando dados que já existem fora do sistema precisam ser **migrados, limpos, convertidos ou cruzados**: histórico do cliente, base pública, sistema antigo. **Upload simples do usuário dentro do produto**, com formato fixado na PRD (ex.: planilha de uma coluna que vira perguntas), é `false`: faz parte do módulo. Consulta automática a um serviço é integração, não dependência de dados |
| `offline` | Termo "offline" (a PRD sempre diz o mecanismo) | Só consulta sem internet → `"local"`. Registro com sincronização depois → `"sync"` |
| `volume_alto` | 3.3 *Performance* | Milhares de usuários simultâneos ou picos declarados → `true`. Sem 3.3 → `false` |
| `rn_critica` (F4) | RNs e 3.4 | `true` se **o código do NTec calcula** dinheiro, dose, dado clínico, prazo legal ou dado fiscal (`fatores/F4-testes.md`). Só repassar valor ao gateway não conta |
| `demanda_pouco_detalhada` | Seção 2 inteira | `true` se algum módulo não tem **Superfície**, alguma integração não tem Sentido, Dados ou Meio, algum fluxo de dados não tem Origem, Processamento ou Destino, ou algum módulo com fator de complexidade não tem **Regras de Negócio** (`fatores/F1-imersao-setup.md`, 1.2). Senão `false`. Com `true`, a resposta abre com o alerta de discovery |
| `stack_fora_template` | 3.1 (serviços de terceiros definidos com o cliente) | A PRD não fixa stack de propósito. `true` só se o cliente exige uma tecnologia **da lista aceita do F0** que não é a do template (ex.: Supabase ou Postgres no lugar de MongoDB). Exigência fora da lista é rejeição no F0. Se a 3.1 não citar, procurar no Fathom (Passo 4) |
| `deploy_infra_cliente` | 3.1 | `true` se a 3.1 disser que roda nos servidores ou na nuvem do cliente. Se não disser, procurar no Fathom (Passo 4) |
| `atipico` | — | Não está na PRD. Procurar no Fathom; se não estiver, lacuna (Passo 4) |

**Hardcoded** (decisão fixa do cliente) não muda nenhum peso. Ele só confirma que não há tela de configuração daquele item, e a skill não deve somar tela de configuração por conta própria.

**Exclusões Explícitas (seção 4)** não somam nada. Usar para duas coisas: conferir que nenhum item excluído foi contado e montar a seção "O que cortar" (um corte não pode ser algo que já está excluído).

## Passo 3 — Fatores de complexidade da PRD que a régua não tem

A PRD marca fatores que não têm linha própria na régua. Eles **encaixam nas linhas que já existem**, sem peso novo (não há dado de calibração para criar pesos).

| Fator na PRD | Linha da régua | Observação |
|---|---|---|
| Pagamento (gateway, Pix, cartão) | Integração `bi_doc` (cobra e recebe a confirmação) | Gateway é serviço de mercado. `bi_sem_doc` só se o pagamento passar pelo sistema próprio do cliente |
| IA (classificar, extrair, gerar, responder) | Integração `uni_doc` (API do modelo) | Se a PRD disser que a IA decide sem humano no fim, marcar também ⚠️ em *Pontos de atenção* |
| Notificação por push no app | Integração `uni_doc` | |
| Notificação por WhatsApp automático | Integração `uni_doc`, ou `bi_doc` se o sistema lê a resposta | Link para abrir o WhatsApp não é integração (0) |
| Notificação por e-mail | `template` | |
| Aviso dentro do sistema | 0 (faz parte do módulo) | |
| Tempo real por aviso do servidor (push) | +1 em `features_atipicas` | Atualização periódica (polling) = 0 |
| Relatório configurável pelo usuário (construtor) | +1 em `features_atipicas` | Tela fixa ou exportação para PDF ou Excel = 0 (faz parte do módulo) |
| Concorrência (ex.: aceite atômico, "o primeiro que aceitar leva") | O módulo vira `fluxos_rn_especifica` | |
| Imutabilidade ou versionamento (ex.: prontuário que não se edita) | O módulo vira `fluxos_rn_especifica` | |
| Rotina agendada (gatilho por horário, não por evento) | O módulo vira `fluxos_rn_especifica` | Gatilho por evento no sistema = 0 |
| Upload e armazenamento de arquivos | `template` (S3) | |
| Migração ou carga de base existente (histórico, base pública, sistema antigo) | `dependencia_dados: true` | Upload simples do usuário dentro do produto, com formato fixado na PRD = 0 (faz parte do módulo) |
| Relatório ou documento em template fixo (PDF, Word, Excel) | 0 (faz parte do módulo, fluxo comum) | Não vira RN específica, mesmo gerado em mais de um formato |
| Multiempresa | `multitenancy` (ver Passo 2) | |
| Offline | `offline` (ver Passo 2) | |

**Não contar duas vezes.** O mesmo módulo vira RN específica uma vez só, mesmo que tenha concorrência **e** imutabilidade. Um fator que já virou integração não vira também feature atípica (a exceção é a IA que decide sozinha, que só ganha ⚠️, sem peso).

## Passo 4 — O que a PRD não responde: transcrição do Fathom primeiro, lacuna para o CN depois

A PRD descreve o produto, não o projeto. Os fatores abaixo ficam de fora dela, mas quase sempre aparecem nas reuniões com o cliente. A skill **procura cada um na transcrição do Fathom** antes de perguntar qualquer coisa. O que não estiver lá vira **lacuna** e volta para o CN.

**Sem transcrição na conversa:** pedir uma vez ao CN para colar a transcrição ou o resumo do Fathom das reuniões com o cliente. Se ele não tiver, todos viram lacuna.

| Fator | O que procurar na transcrição | Como traduzir | Pergunta da lacuna (pronta para o CN repassar) |
|---|---|---|---|
| Quem valida (`f0.sem_validador_nomeado`) | Nome de quem vai testar e aprovar ("a Ana valida toda sexta") | Pessoa nomeada → `false`. Ninguém nomeado, "depende" → `true` (🚩 F0) | "Quem do cliente vai testar e aprovar as entregas?" |
| Condições de contrato (`f0.multa_por_atraso`, `f0.sla_ou_sustentacao`, `f0.prazo_exigido_semanas`) | Multa, SLA, suporte, "precisa estar pronto até…" | Dito explicitamente → preencher. Silêncio → `false` / `null`, registrado em *Suposições* | "O contrato vai ter multa por atraso, exigência de suporte ou data limite de entrega?" |
| Stack e infra (`f0.stack_exigida_fora_da_lista`, `stack_fora_template`, `f0.infra_cliente_sem_acesso`, `deploy_infra_cliente`) | Tecnologia exigida ("tem que ser em…"), "nossos servidores", "a nossa TI hospeda", nuvem própria | Exigência fora da lista do F0 → rejeição. Exigência dentro da lista mas fora do template → `stack_fora_template: true`. Infra do cliente com acesso do NTec → `deploy_infra_cliente: true`; sem acesso → rejeição. "Vocês decidem", "tanto faz" → `false`. Pular se a 3.1 da PRD já responde | "O cliente exige alguma tecnologia, ou que o sistema fique nos servidores dele?" |
| Atípico (`atipico`, `features_atipicas`) | App ou site citado como referência ("tipo o…", "igual ao…", "vi um que…") | Referência citada → `false`. "Não existe nada parecido" → `true` | "Existe algum app ou site parecido que a gente possa usar de referência?" |
| Publicação nas lojas (`lojas`) | "vai pra loja", "baixar na App Store", "só a nossa equipe usa" | Pular se a PRD tem o módulo *Disponibilização do Produto*. Loja aberta ao público → `"normal"` ou `"sensivel"` (`fatores/F6-lojas.md`). Só uso interno → `"nao"`. Silêncio → publica + `"lojas"` em `lacunas_fathom` | "O app vai para a App Store e a Play Store, ou só para uso interno?" |
| Semanas off | Data ou mês de início, prazo de lançamento | Data → contar férias, provas e recesso | "Qual é a data prevista de início? (para contar férias, provas e recesso)" |

**O que conta como resposta encontrada:**
- O cliente (ou o CN, na reunião) **disse explicitamente**. Registrar com a reunião e um trecho curto: `(origem: Fathom · 12/03 — "a Ana valida toda sexta")`.
- Duas reuniões dizem coisas diferentes → vale a mais recente, e a divergência vai para *Pontos de atenção*. Se não der para saber qual vale, é lacuna.
- **Não é resposta:** dedução a partir do tom da conversa, silêncio sobre o assunto, ou fala vaga ("vamos ver", "acho que sim"). Tudo isso é lacuna.

**O que fazer com a lacuna:**
1. Dimensionar mesmo assim com o **valor mais pesado plausível** (`f0.sem_validador_nomeado: true`, `stack_fora_template: true` só se houver algum indício, `atipico: true` só se nenhuma referência foi citada). Semanas off sem data de início: não somar, e dizer isso no prazo em uma frase.
2. **Mostrar quanto da venda depende das lacunas.** No JSON da régua, listar os fatores em lacuna em `"lacunas_fathom"` (só `atipico`, `stack_fora_template`, `deploy_infra_cliente` e `lojas` entram; ex.: `["atipico", "lojas"]`; `lojas` entra quando não se sabe **se** o app vai para as lojas, e o valor leve é `"nao"`) e marcar `"fathom": true` se havia transcrição (o Fathom existe, mas não fala do assunto). O script refaz a conta com esses fatores no valor leve e diz a diferença em sprints inteiras. O prazo vende o número com as lacunas e mostra a parte delas com "+": *"Recomendado vender 14 semanas (7 sprints) = 12 + 2 que dependem do Fathom (referência de produto), mais as semanas off."* Confirmando as lacunas no leve, a venda cai para o primeiro número. Com Fathom que não fala do assunto, a frase diz "dependem de confirmar com o cliente". Se a diferença não muda as sprints, não há "+".
3. Listar na seção **5. Lacunas para o CN** da resposta: o fator, o que foi procurado e não achado, a pergunta pronta e o valor provisório usado na conta.
4. Registrar o valor provisório em *Suposições*, com `(origem: lacuna — não está no Fathom)`.
5. **Status:** lacuna em quem valida deixa o status em 🚩 (F0). Lacuna em stack/infra ou atípico mexe na faixa → ⚠️ *Precisa de revisão* até o CN responder. Lacuna só na data de início não muda a faixa: não rebaixa o status.

Quando o CN responder uma lacuna, trocar o valor provisório, tirar o fator de `lacunas_fathom`, rodar o script de novo e mudar a origem para `(origem: CN)`.

**Não perguntar sobre a documentação das integrações.** O CN não tem como responder: a skill aplica o peso fixo do Passo 2 e registra a classificação em *Suposições* (ex.: `Integração ERP: bidirecional com sistema do cliente (origem: PRD 2.4 + regra de peso fixo)`).

**Lacuna dentro da PRD** (módulo sem superfície, integração sem meio, fluxo de dados sem uma das três partes, "tempo real" sem mecanismo): não deveria acontecer, porque a skill da PRD pergunta antes de gerar o PDF. Se aparecer, tratar como fator desconhecido (perguntar, ou usar o valor mais pesado) e registrar em *Pontos de atenção* que a PRD precisa de revisão antes de virar anexo de contrato.

## Passo 5 — Origem de cada fator

Com PRD, a origem cita a seção:

```
Níveis de acesso: 2 a 5 com grandes diferenças (origem: PRD 2.1 — 4 perfis, recepção e veterinário com módulos próprios)
Fluxos comuns: 4 (origem: PRD 2.2 a 2.5)
Integração Mercado Pago: bidirecional com serviço de mercado (origem: PRD 2.3 + regra de peso fixo)
Quem valida: Ana, toda sexta (origem: Fathom · 12/03 — "a Ana valida toda sexta")
Data de início: lacuna (origem: lacuna — não está no Fathom)
```
