# F6 — Publicação nas lojas (só app nativo)

**Baseline do formulário:** 2 a 6 semanas.

✅ **Reunião 20/10:** os prazos de desenvolvimento (F3) **não** incluem a publicação nas lojas. Ela fica toda aqui.

| Linha | Mín | Central | Máx |
|---|---|---|---|
| Não publica | 0 | 0 | 0 |
| App comum | 2 | 2,5 | 4 |
| App sensível | 2,5 | 3 | 6 |

---

## O teste

Fazer na ordem. A primeira resposta que decide encerra o teste.

| # | Pergunta | Onde ler | Resultado |
|---|---|---|---|
| 1 | O formato é app nativo? (ver glossário) | F3, item 3.2 | Não → **não publica** |
| 2 | O app vai para a App Store ou a Play Store abertas ao público? | Transcrições ("baixar na loja", "estar na Play Store" × "só a nossa equipe usa"). Na revalidação: módulo *Disponibilização do Produto*, 3.1 | Sim → segue para a 3. Não (só uso interno ou teste) → **não publica**. Ninguém falou de loja → **não publica** + pergunta em `a_confirmar`: "O app precisa estar na App Store ou na Play Store?", com `"troca": {"lojas": "normal"}` (ou `"sensivel"`, se a 3 der sim) |
| 3 | O app é **sensível**? (qualquer item abaixo) | Transcrições + protótipo (dados que aparecem nas telas) | Sim → **app sensível**. Não → **app comum** |

**App sensível** se qualquer um for sim:
- a categoria na loja é Medical (saúde), Finance (finanças) ou Kids (infantil);
- coleta dado sensível pela LGPD, art. 5º, II (saúde, biometria, origem racial, religião, vida sexual, dado genético);
- tem pagamento **dentro do app**;
- o público inclui menores de 13 anos.

**Sem resposta na pergunta 3:** app comum + pergunta em `a_confirmar`: "O app coleta dado de saúde, recebe pagamento ou é usado por crianças?", com `"troca": {"lojas": "sensivel"}`.

**Exemplo:** app de academia que só agenda aulas → comum. App de academia que registra peso, medidas e restrições médicas → sensível (dado de saúde).

---

## Teste fechado (TestFlight)

Hoje "app só para testes" vale 0.

> 🔎 **Proposta:** o TestFlight externo (testadores fora da equipe) também passa por revisão da Apple. Sugestão: TestFlight externo = +0,5 / +0,5 / +1. **Até validar:** 0.

## Dica que reduz o risco

Pedir ao cliente que abra a conta de desenvolvedor (Apple e Google) **já na imersão**. Conta de empresa pode levar semanas para ser aprovada.
