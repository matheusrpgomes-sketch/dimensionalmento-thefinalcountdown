# Glossário — dimensionamento NTec

Definição única de cada termo usado nos arquivos F0 a F6. Se outro arquivo da skill definir um termo de outro jeito, **vale este glossário**.

**Desde 22/10/2026 a entrada padrão são as transcrições das reuniões de diagnóstico + o protótipo navegável.** Cada definição vale para essa entrada. Quando um termo tem leitura própria na PRD (revalidação depois do contrato), ela aparece como **Na revalidação (PRD)**.

---

## Estrutura do produto

**Jornada (fluxo)** — Unidade de esforço do F3. Uma pessoa de um **perfil** cumpre um **objetivo** sobre uma **entidade principal**, do começo ao fim (ex.: "recepção · gerencia a agenda · consulta"; "tutor · agenda e paga · consulta"). Contar assim, nesta ordem:
1. **Uma jornada = perfil + objetivo + entidade principal.** Listar, ver o detalhe, criar, editar e excluir a mesma entidade pelo mesmo perfil é **uma** jornada.
2. **A mesma entidade, outro perfil com outro objetivo, é outra jornada** (o tutor agenda ≠ a recepção gerencia a agenda).
3. **Cadastro auxiliar não é jornada:** categorias, tipos, status, configurações simples e listas de apoio entram na jornada que os usa.
4. **Fora da contagem:** login, cadastro de conta e recuperação de senha (F2); publicação (F5, F6); telas de offline e sincronização quando `offline` não é `nao` (extra de offline).
5. **Jornada grande conta 2:** quando cruza **3 ou mais entidades principais** ou tem **mais de 6 telas próprias** no protótipo. (🔎 Proposta: os limites 3 e 6 precisam ser calibrados no primeiro projeto rodado por este caminho, ex.: CTE.)
6. **Cada agrupamento vai para *Suposições*** com as telas juntadas: "Jornada 'recepção gerencia a agenda' = telas Agenda, Detalhe do horário, Remarcar".

Uma tela solta não é jornada. A jornada só **entra na conta** se passar no Passo 3 de `leitura-transcricoes-prototipo.md` (o cliente pediu ou falou dela na gravação).

**Na revalidação (PRD):** **Módulo** é uma subseção da seção 2 da PRD; **item A(cli)D** é cada linha "Adicionar, Consultar, Listar, Inativar, Deletar"; **folha** é a subseção mais funda com itens A(cli)D. Partir das folhas, juntar as da mesma jornada (mesma entidade, mesmo código, uma continua a outra; folha com até 2 itens que só serve outra jornada entra nela) e contar 2 quando a jornada tem mais de 8 itens A(cli)D. O número tem de bater com o das transcrições: se não bater, a diferença vai para a área de projetos.

**Formato** — Cada **código separado** que vai para o ar. Painel admin dentro do mesmo app web é o mesmo formato. App nativo + painel web são dois formatos. **O protótipo não decide o formato** (todo protótipo do Lovable é web): o formato vem da fala do cliente.

**Fluxo compartilhado** — Jornada com tela em mais de um código (ex.: o tutor agenda no app e a recepção gerencia a mesma agenda no painel). Só ela recebe o formato extra (D1). Jornada que vive num código só recebe só o fator daquele código (`F3-desenvolvimento.md`, 3.2).

**Web** — Abre no navegador, sem instalar.

**PWA** — Web que instala pelo navegador (ícone na tela do celular), sem passar por loja. Substitui o antigo `webapp`.

**App nativo** — Precisa estar na App Store ou Play Store, **ou** usa um recurso nativo desta lista: Bluetooth, GPS em segundo plano, NFC, notificação com o app fechado em iOS, leitura de sensores. Fora da lista → PWA.

## Perfis e acesso

**Perfil (nível de acesso)** — Cada tipo de pessoa que usa o sistema com permissões próprias. Admin conta como perfil. Só conta o perfil que o cliente **citou nas reuniões** (quem usa, quem aprova, quem só consulta). Perfil que só existe no protótipo (seletor de perfil, usuário de demonstração) sem fala nas reuniões **não conta** e vai para `a_confirmar`. **Na revalidação (PRD):** os perfis da seção 2.1.

**Tela exclusiva** — Tela ou rota que um perfil abre e pelo menos um outro perfil não abre. **Não contam:**
- um item a mais num menu que leva a uma tela que todos abrem;
- o **painel admin básico** (ver abaixo).

**Painel admin básico** — O que o template NTec já entrega para o admin, sem custo de prazo: gerenciar usuários (listar, criar, editar, desativar, trocar o perfil) e ver, editar ou remover os registros que os outros perfis criam, nas mesmas telas de listagem e detalhe das jornadas. Qualquer tela de admin **além disso** é tela exclusiva: dashboard ou relatório, aprovação de cadastro, configuração de regra de negócio, auditoria, financeiro. (🔎 Proposta: confirmar com a área técnica o que o painel admin do template cobre hoje.)

**Status de cadastro** — O cadastro de um perfil passa por estados (pendente, aprovado, rejeitado) que bloqueiam o acesso até alguém aprovar.

**Filtro por dono** — O perfil só vê os registros que ele mesmo criou ou que são dele (ex.: paciente só vê o próprio diário).

## Multitenancy

**Tenant** — Cada empresa, clínica, unidade ou filial que usa o mesmo sistema com seus próprios dados.

**Separado** — Um banco só, cada registro marcado com o tenant, filtro no código. Um administrador geral vê os dados de todos os tenants.

**Isolado** — Vazamento de dado entre tenants é quebra de contrato ou de LGPD. Exige isolamento no banco (RLS, schema ou banco por tenant). Ligar ou desligar features de uma lista fixa, ou trocar logo e cores por tenant, continua sendo isolado.

**Instâncias** — Código ou regra de negócio **diferente** por tenant. Vai para o F0 (parada obrigatória).

## Regras de negócio

**RN específica** (F3) — Regra que o cliente precisa entregar **escrita**: fórmula, tabela, norma, protocolo. Também: concorrência ("o primeiro que aceitar leva") e imutabilidade/versionamento. Só conta com **fala na transcrição** que descreva a regra ou diga onde ela está escrita. **Não são** RN específica: validação padrão de mercado (CPF, CNPJ, e-mail, CEP) e documento gerado num **template fixo** (relatório em PDF, Word ou Excel), mesmo em mais de um formato.

**RN crítica** (F4) — **O código do NTec calcula** valor em dinheiro, dose, dado clínico, prazo legal ou dado fiscal, e um erro causa dano ao usuário final. Só repassar um valor para o gateway de pagamento não é RN crítica.

**Rotina agendada** — Algo que roda sozinho por horário (todo dia às 8h), não por ação do usuário.

## Referência e risco

**Produto atípico** (F1) — Nas reuniões, o cliente ou o CN disseram que **não existe** app ou site parecido para o **produto inteiro**. Setor incomum com produto comum não é atípico. Ninguém falar de referência **não** é atípico: vira pergunta em `a_confirmar`.

**Feature atípica** (F3) — Uma **feature** específica que foi pedida nas reuniões e está nesta lista: tempo real por aviso do servidor (push em tempo real, chat, rastreio ao vivo) ou relatório configurável pelo usuário (construtor). É uma **contagem** (quantas features), não semanas.

**Pergunta em aberto (`a_confirmar`)** — Tudo que as transcrições não decidem: jornada ou perfil só no protótipo, integração citada de forma vaga, regra citada sem detalhe, fator de projeto sem resposta. **Não entra na venda.** Vai no JSON com o efeito se a resposta for sim; o script calcula o custo e a venda sai "+ até X". Enquanto houver pergunta em aberto, o status é ⚠️.

**Lacuna** — Nome antigo da pergunta em aberto de fator de projeto. Até 22/10/2026 entrava na venda com o valor mais pesado (`lacunas_fathom`); agora vai para `a_confirmar`.

**Citação** — Trecho literal de uma transcrição, com a reunião e a marcação de tempo (`T1 · 00:12:30 — "trecho"`), ou a tela do protótipo (`Protótipo · tela "Agenda"`). Resumo de reunião (Gemini, Fathom) não é citação da transcrição: cita-se como `(resumo T1)` e o status fica ⚠️ preliminar. **Na revalidação (PRD):** o trecho da PRD com a seção.

**Silêncio** — Nenhuma transcrição fala do assunto. O valor de cada campo no silêncio está numa tabela só: `leitura-transcricoes-prototipo.md`, Passo 4. Nenhum arquivo de fator decide o silêncio por conta própria.

## Integrações e dados

**Integração** — Troca **automática** de dados com outro sistema, sem uma pessoa disparar.

**Unidirecional** — O sistema só envia **ou** só recebe.

**Bidirecional** — O sistema envia **e** recebe.

**Serviço de mercado** — Produto vendido para qualquer empresa, com documentação pública **e** ambiente de teste (sandbox) que o NTec consegue acessar sozinho, sem depender da TI do cliente. Ex.: Mercado Pago, Google Maps, Expo Push, OpenAI, WhatsApp Business.

**Sistema do cliente** — ERP, sistema legado, sistema sob medida, ou SaaS em que o acesso depende da TI do cliente (ex.: Totvs, Bling ou RD Station sem sandbox liberado). Também: troca automática por arquivo e qualquer caso em dúvida.

**Sem API** — Uma transcrição diz explicitamente que o outro sistema não tem API (ex.: "o sistema deles não tem integração, é tudo na mão").

**Dependência de dados** — Dados que **já existem fora do sistema** (planilha legada, base pública, sistema antigo) e precisam ser migrados, limpos, convertidos ou cruzados para o produto funcionar; **uma pessoa dispara** a importação (carga única ou recorrente). **Não é:** upload simples feito pelo usuário dentro do produto, com formato fixo, que vira registros na hora (ex.: planilha de uma coluna, uma pergunta por linha). Isso é parte da jornada.

**Offline local** — O app **só lê** sem internet o que já está no aparelho, sem gravar nada para subir depois.

**Offline com sincronização** — O app **grava** sem internet e sobe os dados quando a conexão volta.

**Volume alto** — Uma transcrição cita **1.000 ou mais usuários ao mesmo tempo**, ou um pico com data (evento, lançamento, campanha). "Muita gente vai usar" sem número não é volume alto: vira pergunta em `a_confirmar`. (🔎 Proposta: o limite 1.000 precisa ser validado.) **Na revalidação (PRD):** a seção 3.3.

## Deploy e lojas

**Infra do cliente** — A conta de nuvem ou o servidor é do cliente, **ou** a TI do cliente aprova cada publicação.

**App sensível** — Categoria Medical, Finance ou Kids na loja, **ou** coleta de dado sensível (LGPD, art. 5º, II: saúde, biometria, origem racial, religião etc.), **ou** pagamento dentro do app, **ou** público com menos de 13 anos.

## Conta

**Linha pesada** — Entre duas linhas possíveis, a que tem o valor central maior. Só se usa para **classificar** um fator que foi citado e encaixa em duas linhas (`regra-fronteira-e-faixa.md`), nunca para decidir **se** algo entra no escopo.

**Teto** — Valor máximo de referência de uma fase. Ver D4 sobre o que acontece quando a soma passa dele.

**Piso** — O cenário otimista. Nunca vender abaixo dele.
