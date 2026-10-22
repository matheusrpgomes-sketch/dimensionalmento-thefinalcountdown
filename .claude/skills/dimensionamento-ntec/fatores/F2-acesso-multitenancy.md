# F2 — Infra, níveis de acesso, cadastro e login

**Baseline do formulário:** 1 a 4 semanas. **Teto de referência:** 4 (ver ⏳ **D4**).

✅ **Reunião 20/10:** níveis de acesso (casos básicos) e multitenancy ficam em **tabelas separadas**, cada linha com um discriminante claro. O F2 é a soma de **F2a + F2b**.

✅ **Reunião 20/10:** o fator Claude Code (×0,7 / ×0,85 / ×1 no F2) foi **removido**. Os valores abaixo já são os finais, sem multiplicador.

**O que o template já entrega (0 semanas):** login por e-mail e senha, recuperação de senha, login com Google e painel admin básico.

**Onde ler:** transcrições + protótipo (caminho padrão). Na revalidação, a PRD (2.1, linha Superfície, RNs, 3.4). O silêncio de cada campo está em `leitura-transcricoes-prototipo.md`, Passo 4.

---

## F2a — Níveis de acesso

### Passo 1: contar os perfis

| Pergunta | Onde ler | Sem resposta |
|---|---|---|
| Quantos **perfis** o cliente citou nas reuniões? (admin conta; ver *Perfil* no glossário) | Transcrições ("quem vai usar", "o gestor aprova", "o paciente só vê") + protótipo (menus por perfil, troca de perfil, login de demonstração) para confirmar as telas de cada um | Contar só os citados. Perfil que só aparece no protótipo → `a_confirmar` com `"troca": {"niveis_acesso": "<linha com ele>"}` |

### Passo 2: o teste de "grandes diferenças" (só para 2 a 5 perfis)

É **grandes diferenças** se **qualquer** pergunta for sim. Se todas forem não, é **poucas diferenças**.

| # | Pergunta | Onde ler | Sem resposta |
|---|---|---|---|
| a | Algum perfil abre uma **tela exclusiva** (tela ou rota que pelo menos um outro perfil não abre)? O **painel admin básico** do template não conta (ver glossário) | Protótipo (menu de cada perfil) + fala que confirma a tela (Passo 3 de `leitura-transcricoes-prototipo.md`) | Não. Tela exclusiva só no protótipo → `a_confirmar` |
| b | Algum perfil tem **status de cadastro** (pendente, aprovado, rejeitado) que bloqueia o acesso até alguém aprovar? | Transcrições ("a gente aprova antes", "só entra depois de validar") + protótipo (tela de aprovação) | Não |
| c | Algum perfil só vê os **próprios registros** (filtro por dono)? | Transcrições ("cada um só vê o seu") + protótipo | Não |

**Exemplos:**
- Admin e usuário, em que o admin só vê um item a mais no menu que leva a uma tela que o usuário também abre → poucas.
- Admin e usuário, em que o admin só gerencia usuários e edita os registros dos usuários (painel admin básico) → poucas.
- Admin e usuário, em que o admin abre um dashboard de relatórios que o usuário não abre → grandes (a).
- Nutricionista com cadastro pendente que bloqueia rotas → grandes (b).
- Paciente só vê o próprio diário → grandes (c).

### Tabela F2a

| Linha | Mín | Central | Máx |
|---|---|---|---|
| Nenhum (sem login, sem backend) | 0 | 0 | 0 |
| 1 perfil | 0,5 | 0,5 | 1 |
| 2 a 5, poucas diferenças | 0,5 | 1 | 1,5 |
| 2 a 5, grandes diferenças ⏳ **D2** | 1,5 | 2 | 2,5 |
| 6 ou mais | 2,5 | 3 | 4 |

> A faixa antiga era "2 a 6" e "6 ou mais", que valiam as duas para 6 perfis. Agora: **2 a 5** e **6 ou mais**.

> ⏳ **D2 — em aberto:** a reunião mandou **aumentar** o prazo de níveis de acesso complexos, sem dizer quanto. **Provisório:** valores atuais (1,5 / 2 / 2,5). 🔎 Sugestão: 2 / 2,5 / 3.

---

## F2b — Multitenancy

### O teste

Fazer as perguntas **na ordem**. A primeira que der sim decide a linha.

| # | Pergunta (pronta para o CN repassar ao cliente) | Onde ler | Se sim |
|---|---|---|---|
| 1 | "O sistema vai ser usado por mais de uma empresa, clínica, unidade ou filial, cada uma com os seus dados?" | Transcrições (termos: "cada unidade", "várias clínicas", "por filial", "outras empresas") | Vai para a 2. Se **não**, ou ninguém falou: linha "Não" |
| 2 | "Alguma empresa vai ter uma **regra** ou **funcionalidade** que funciona diferente das outras?" (Trocar logo ou cores, ou ligar e desligar features de uma lista fixa, **não** conta) | Transcrições | **F0** — parada obrigatória (`instancias`) |
| 3 | "Se a empresa A vir um dado da empresa B por causa de um erro, isso quebra o contrato ou a LGPD?" | Transcrições | **Isolado** |
| 4 | "Um administrador geral pode ver os dados de todas as empresas juntas?" | Transcrições + protótipo (visão consolidada) | **Separado** |

**Multitenancy citado, mas 2, 3 e 4 sem resposta:** **separado** + duas perguntas em `a_confirmar`: a 3 (`"troca": {"multitenancy": "isolado"}`) e a 2 (`"troca": {"multitenancy": "instancias"}`, que vira parada).

### Tabela F2b

| Linha | O que significa | Mín | Central | Máx |
|---|---|---|---|---|
| Não | Uma empresa só | 0 | 0 | 0 |
| Separado | Um banco, filtro por tenant no código, admin geral vê tudo | +0,5 | +0,5 | +1 |
| Isolado ⏳ **D2** | Vazamento entre tenants quebra contrato ou LGPD; isolamento no banco (RLS, schema ou banco por tenant) | +1 | +1,5 | +2 |
| Instâncias | Código ou regra diferente por tenant | — vai para o **F0** — | | |

> ⏳ **D2 — em aberto:** a reunião mandou **aumentar** o prazo de isolamento de dados, sem dizer quanto. **Provisório:** valores atuais (1 / 1,5 / 2). 🔎 Sugestão: 1,5 / 2 / 3.

---

## Teto

> ⏳ **D4 — em aberto:** "6 ou mais" (4) + "isolado" (2) = 6 no máximo. **Provisório:** manter a soma e marcar ⚠️ "F2 acima do teto de 4 semanas: revisar com a área de projetos". Não cortar.

## Origem na resposta

```
F2a: 4 perfis, grandes diferenças (origem: T1 · 00:14:05 — "o veterinário vê o prontuário, a recepção não"; Protótipo · tela "Prontuário")
F2b: isolado (origem: T2 · 00:31:40 — "cada clínica não pode nem sonhar em ver o dado da outra")
```
