# Exemplo de resposta completa (caso fictício)

Este caso **não é um projeto real**. Serve para mostrar ao CN como a resposta da skill fica do começo ao fim. Entrada: `ficticio-petagenda.json`.

**O que o CN mandou:**
> "Rede de 3 clínicas veterinárias quer um app pro tutor marcar consulta, ver a carteirinha de vacina do pet e receber lembrete. A clínica quer um painel pra recepção e pro veterinário. Querem pagar a consulta pelo app (Mercado Pago). Não tem documento, foi só uma call."

**Respostas do CN às perguntas da skill:** cada clínica só vê os próprios dados, mas as regras são as mesmas para todas; o tutor baixa o app na loja; o veterinário registra o atendimento e a recepção gerencia a agenda; o lembrete é por notificação no celular.

---

# Projeto PetAgenda

⚠️ **Estimativa preliminar, sem PRD.** Rodar a skill da PRD antes de fechar a proposta.

**1. Prazo em uma frase.** Recomendado vender **18 semanas (9 sprints)** + semanas off. Não vender abaixo de 14.

**2. Faixa de semanas**

| Cenário | Semanas | Sprints | Quando acontece |
|---|---|---|---|
| Otimista (piso) | 14 | 7 | Escopo congelado, clínica responde rápido |
| **Provável (recomendado)** | **18** | **9** | O que costuma acontecer no NTec |
| Conservador (teto de risco) | 24 | 12 | Se pagamento e lojas derem problema |

**3. Resumo.** App nativo para tutores (lojas) + painel web para as clínicas. 4 perfis (tutor, recepção, veterinário, admin da rede). 4 fluxos críticos: agendar consulta, carteirinha de vacina com lembretes, registro de atendimento, gestão da agenda. Pagamento online e notificações. 3 clínicas com dados separados.

**4. Pontos de atenção**
1. **Pagamento pelo app (Mercado Pago):** a integração é bidirecional (cobra e recebe a confirmação). É um serviço de mercado com API pública, então entra com o peso fixo "com documentação", sem precisar perguntar nada.
2. **Dados separados por clínica (multitenancy (um mesmo sistema atendendo várias empresas com os dados separados)):** confirmar por escrito que as **regras** são iguais para as 3. Se cada clínica quiser regras próprias, o projeto para (🚩).
3. **Demanda sem documento:** veio só de uma call. A imersão fica mais longa (+1 semana no central).

**5. Perguntas para o cliente**
- "Cada clínica tem regras próprias (horários, preços, tipos de consulta) ou todas seguem as mesmas regras?"
- "O pagamento precisa ser pelo app no lançamento, ou pode ser na clínica no começo?"
- "Precisa estar na App Store e na Play Store, ou um app que se instala pelo navegador resolve no início?"
- "Quem da rede vai testar e aprovar as entregas, e tem umas 2 horas por semana para isso?"

**6. Detalhamento por fase**

| Fase | Critério | Mín | Central | Máx |
|---|---|---|---|---|
| F1 Imersão e setup | base + demanda sem documento | 2 | 3 | 3,5 |
| F2 Acesso e login | 4 perfis com telas próprias → 2 a 5 com grandes diferenças; dados separados por clínica | 2 | 2,5 | 3,5 |
| F3 Desenvolvimento | 4 fluxos comuns: 1 no app (x1,2), 2 no painel (x1,0), 1 nos dois (x1,4); Mercado Pago (bi, doc); push (uni, doc) | 5,6 | 7,25 | 9,4 |
| F4 Testes com cliente | base | 1 | 1,5 | 2 |
| F5 Deploy | web + app | 0,5 | 1 | 1,5 |
| F6 Lojas | app comum | 2 | 2,5 | 4 |
| **Total** | | **14** | **18** | **24** |

**7. Precedente.** **Projeto D** (app nas lojas + painel web, 5 fluxos comuns): vendido 18, sem atraso até agora. O PetAgenda fica acima por causa do pagamento, dos perfis com mais diferenças e da demanda sem documento.

**8. O que cortar** (recalculado com o script)

| Corte | Provável | Venda |
|---|---|---|
| Escopo completo | 18 | 18 |
| PWA (app instalado pelo navegador) em vez de app nas lojas | 15 | 16 |
| + pagamento na clínica no MVP (sem Mercado Pago) | 14 | 14 |
| + carteirinha de vacina na fase 2 | 13 | **14** |

**9. Bloco para colar no Dimensionamento Tec**
```
7. Baseline: Imersão/setup 3 sem · Acesso/login 2,5 sem · Desenvolvimento 7,25 sem · Testes com cliente 1,5 sem · Deploy 1 sem · Lojas 2,5 sem
Faixa: otimista 14 · provável 18 (vender 18) · conservador 24 semanas (+ semanas off)
```

**10. Observações**
- *Suposições:* lembretes de vacina são notificações push simples (sem SMS ou WhatsApp); o painel da recepção e o do veterinário estão no mesmo código web; o login por e-mail e o upload de foto do pet usam o template.
- *Ajustes de fronteira:*
  ```
  F2 níveis de acesso: 2-5 poucas diferenças → 2-5 grandes diferenças (+1)
  Motivo: veterinário e recepção têm telas e permissões próprias (registro de atendimento × agenda); na dúvida, a régua vai para o mais pesado.
  ```
