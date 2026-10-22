# Insumos e perguntas — como tirar os fatores do CN

**A entrada padrão são as transcrições das reuniões de diagnóstico + o protótipo navegável** (`leitura-transcricoes-prototipo.md`). Deste arquivo, o caminho padrão usa a **tabela de perguntas do Passo 2** (para as lacunas) e o **vocabulário do Passo 3** (para traduzir a fala do cliente).

O caminho completo deste arquivo vale quando **não há transcrição**: o formulário **Dimensionamento Tec** (inteiro ou em parte), uma ficha de qualificação ou um briefing solto. Toda resposta feita assim sai como ⚠️ **Estimativa preliminar: faltam as transcrições**, com a recomendação de mandar as transcrições e o protótipo antes de fechar a proposta.

---

## Passo 1 — Identificar o que chegou

| Entrada | O que aproveitar | Cuidado |
|---|---|---|
| **Transcrições + protótipo** | Tudo | Não é este arquivo: ir para `leitura-transcricoes-prototipo.md` |
| **PRD ("[Requisitos] {projeto}")** | Conferência | Revalidação depois do contrato: `leitura-prd.md` |
| Formulário Dimensionamento Tec | Seções 1 (perfis de usuário), 3 (fluxos críticos, features atípicas), 5 (porte e maturidade do cliente) e 6 (perfil da demanda: formato, níveis, multitenancy, integrações, dados, offline) | Seções 7 e 8 (baseline e buffer) preenchidas pelo CN são **palpite**: não usar como entrada, só comparar no fim |
| Ficha de qualificação ou proposta | Produto, setor, porte, o que o cliente pediu | Costuma **subestimar o escopo** (Projeto B: o escopo real ficou maior que o da ficha) |
| Transcrição de call (Fathom, Granola, notas) | Fluxos descritos pelo cliente, integrações citadas, urgência, quem aprova | Filtrar a conversa: só o que mexe em prazo. Desejo vago ("seria legal ter…") não é escopo até o CN confirmar |
| Texto livre do CN | O que tiver | Tudo é `origem: palpite do CN` até ser confirmado |

## Passo 2 — Preencher os fatores, perguntando o que faltar

**Se veio transcrição do Fathom (ou de outra ferramenta):** procurar a resposta de cada pergunta nela antes de perguntar, com a regra zero de `leitura-transcricoes-prototipo.md` (só vale o que foi dito explicitamente, citar a reunião e o trecho). O que não estiver lá fica no **valor do silêncio** (tabela do Passo 4 de `leitura-transcricoes-prototipo.md`) e vira pergunta em `a_confirmar`, fora da venda ("+ até X"). Quem valida sem resposta vira `f0.sem_validador_nomeado: true` (🚩).

**Critérios completos e pesos:** no arquivo de cada fase em `fatores/`. A tabela abaixo é o atalho das perguntas para o CN. **O JSON exige todos os campos**, inclusive o bloco `"f0"` (formato em `exemplos/*.json`): o que ninguém respondeu entra com o valor do silêncio (`leitura-transcricoes-prototipo.md`, Passo 4), vai para *Suposições* e vira pergunta em `a_confirmar`.

**Primeiro o F0** (`fatores/F0-viabilidade.md`): se o cliente exige tecnologia fora da lista aceita ou offline com sincronização em MongoDB, o projeto é rejeitado e não há o que perguntar do resto.

Perguntar **no máximo 5 por rodada**, primeiro as que mais mexem no prazo (na ordem da tabela). Usar as perguntas como estão: foram escritas para o CN repassar ao cliente sem precisar traduzir.

| Fator da régua | Pergunta para o CN / cliente | Como traduzir a resposta |
|---|---|---|
| **Fluxos críticos** (F3) | "Quais são as 3 a 6 coisas principais que alguém faz no sistema, do começo ao fim? Ex.: 'o paciente preenche o diário e a nutricionista vê o relatório'." | Cada jornada completa = 1 fluxo. Telas soltas não contam. Mais de 8 fluxos num MVP → sugerir cortar |
| **Regra de negócio específica** (F3, F4) | "Tem algum cálculo, fórmula ou regra que, se o sistema errar, causa prejuízo, risco à saúde ou problema legal? Já existe isso escrito (planilha, artigo, norma)?" | Sim → fluxo com RN específica + RN crítica no F4. Pedir o documento da regra **antes** da proposta |
| **Formato** (F3, F5, F6) | "As pessoas vão usar pelo navegador, por um app baixado da loja, ou os dois? Precisa estar na App Store / Play Store?" | Navegador = web. "Ícone na tela do celular, mas sem loja" = PWA. Loja = app + F6 |
| **Níveis de acesso** (F2) | "Quantos tipos diferentes de pessoa usam o sistema? Cada tipo vê telas diferentes ou só algumas opções a mais? Alguém precisa aprovar o cadastro de outro?" | Contar os tipos (admin conta). 6 ou mais → `6+`. De 2 a 5: tela exclusiva, aprovação de cadastro ou cada um só vê os próprios registros → "grandes diferenças"; senão "poucas" (`fatores/F2-acesso-multitenancy.md`) |
| **Integrações** (F3) | "O sistema precisa conversar com algum outro sistema (pagamento, ERP, planilha, mapa, WhatsApp)? Ele só *puxa* dados, só *manda*, ou os dois? Esse outro sistema é um serviço conhecido (Mercado Pago, Google Maps…) ou um sistema próprio do cliente?" | Só puxa ou só manda = unidirecional. Os dois = bidirecional. **Não perguntar sobre documentação:** peso fixo da régua (serviço de mercado = com documentação; sistema do cliente ou dúvida = sem documentação, com cláusula e plano B). Google, e-mail e upload de arquivo = template |
| **Dependência de dados** (F3) | "O sistema vai usar dados que hoje estão em planilhas, tabelas públicas ou bases de outros lugares?" | Sim → dependência de dados + chamar o núcleo de Dados |
| **Offline** (F3) | "Precisa funcionar sem internet? Se sim, o que acontece quando a internet volta: os dados precisam subir para algum lugar?" | Sem internet e nada sobe = offline local (0). Precisa sincronizar = offline com sincronização |
| **Multitenancy** (F2) | "O sistema vai ser usado por várias empresas ou unidades diferentes? Cada uma precisa de regras e funções próprias, ou só não pode ver os dados da outra?" | Uma empresa só = não. Regra ou função própria por empresa = `instancias` (🚩 F0). Vazamento quebra contrato ou LGPD = isolado. Admin geral vê tudo = separado. Sem resposta = isolado |
| **Volume** (F3) | "Quantas pessoas devem usar ao mesmo tempo, no pior dia?" | Centenas = normal. Milhares simultâneos ou picos (evento, lançamento) = volume alto |
| **Quem valida** (F0) | "Quem do cliente vai testar e aprovar as entregas?" | Ninguém nomeado, ou "depende" = `sem_validador_nomeado: true` (🚩) |
| **Condições de contrato** (F0) | "O cliente espera suporte 24/7 ou SLA depois da entrega, ou tem uma data limite?" | SLA ou suporte 24/7 = `sla_ou_sustentacao: true` (contrato de manutenção à parte, não rejeita). Data limite = `prazo_exigido_semanas` (abaixo do otimista = 🚩) |
| **Hardware** (F0) | "O sistema precisa conversar com algum aparelho (leitor, impressora fiscal, sensor, Bluetooth)?" | Sim = `hardware: true` (🚩) |
| **Stack e deploy** (F0, F1, F5) | "O cliente exige alguma tecnologia ou que o sistema fique nos servidores dele? Se ficar nos servidores dele, o nosso time vai ter acesso para publicar e corrigir?" | Tecnologia fora da lista do F0 = 🚫. Dentro da lista mas fora do template (ex.: Supabase) = `stack_fora_template`. Servidores do cliente com acesso = `deploy_infra_cliente`; sem acesso = `infra_cliente_sem_acesso: true` (sem garantia, ajustar contrato) |
| **Documentação da demanda** (F1) | "Já existe protótipo navegável ou referência de app parecido?" | Sem protótipo → demanda pouco detalhada |
| **Atípico** (F1, F3) | "Existe algum app ou site parecido que a gente possa usar de referência?" | Nenhum benchmark → atípico. Não marcar só porque o *setor* é incomum se o produto é comum |

## Passo 3 — Vocabulário: o que o cliente diz × o que a régua entende

| O cliente / CN diz | A régua entende | Atenção |
|---|---|---|
| "É só um aplicativo simples" | Nada. Perguntar os fluxos | "Simples" quase nunca é simples (Projeto C foi reescopado 2 vezes) |
| "Igual ao [app famoso], só que menor" | Feature atípica até provar o contrário | App famoso = anos de time grande |
| "Painel para eu acompanhar" | +1 fluxo (dashboard), no mesmo formato web se for o mesmo sistema | |
| "Tem que ter login com Google" | Template (0) | |
| "Integra com o nosso sistema" | Integração bidirecional com sistema do cliente (`bi_sem_doc`) | Peso fixo, sem pedir link. Cláusula de contrato + plano B (planilha) |
| "Manda mensagem no WhatsApp" | Link para WhatsApp = 0. Envio automático = integração (API do WhatsApp Business, bidirecional se responder) | |
| "Funciona no celular" | Web responsiva, PWA ou app: perguntar se precisa estar na loja | |
| "Depois a gente vê isso" | Fora do escopo. Registrar no "fora do escopo" do formulário | |
| "Só preparar para o futuro" | Dimensionar como item completo ou deixar fora: não existe meia feature | |

## Passo 4 — Marcar a origem de cada fator

Todo fator preenchido leva a origem entre parênteses:

```
Níveis de acesso: 2 a 5 com grandes diferenças (origem: formulário, seção 6)
Fluxos críticos: 4 (origem: transcrição da call, cliente descreveu 4 jornadas)
Integração com ERP: bidirecional com sistema do cliente (origem: transcrição da call + regra de peso fixo)
```

## Passo 5 — Conferir declarado × encontrado

Se o CN escreveu uma coisa e a transcrição ou os documentos mostram outra, registrar as duas e não corrigir em silêncio:

```
Divergência: formulário diz "sem integrações", mas na call o cliente pediu emissão de nota fiscal.
```

Se o CN já preencheu as seções 7 e 8 do formulário, comparar com a faixa da skill e dizer a diferença em *Observações*.

## Quando parar e devolver para o CN

- Faltam os **fluxos críticos** ou o **formato**: sem eles, não dimensionar (são os fatores que mais mexem no prazo). Devolver as perguntas.
- O CN respondeu "não sei" para 3 ou mais fatores: dimensionar com os valores do silêncio, pôr cada dúvida em `a_confirmar` (o script mostra "+ até X") e marcar ⚠️.
