# Projeto A — PWA de guia local

**Situação:** finalizando, no prazo. **Vendido:** 12 semanas (+1 off), 6 sprints.

## O que era
Guia de eventos, gastronomia e hospedagem de uma região, centrado num mapa. WebApp PWA mobile-first, mais o painel de gestão no mesmo sistema web. App nativo nas lojas ficou fora do escopo. Cliente pessoa física, sem conhecimento de tecnologia.

## Como a régua classificou

| Fator | Classificação | Origem |
|---|---|---|
| Formato | PWA (o painel está no mesmo código → não é formato extra) | hand-off |
| Níveis de acesso | visitante, cadastrado e admin → 2 a 6 com poucas diferenças | hand-off |
| Fluxos comuns | 4: mapa com filtros, agenda (hoje/amanhã), detalhe do local, cadastro de estabelecimentos e eventos | palpite, média confiança |
| Integrações | API de mapa (uni, doc), notificações (uni, doc); login Google e S3 = template; links para apps de navegação e WhatsApp = 0 | plannings S3–S5 |
| Demais fatores | nenhum | — |

## Resultado da régua

_Recalculado em 22/10/2026 com a régua atual; conferido por `scripts/testar_exemplos.py`._

| Fase | Mín | Central | Máx |
|---|---|---|---|
| F1 Imersão e setup | 1,5 | 2 | 2,5 |
| F2 Acesso e login | 0,5 | 1 | 1,5 |
| F3 Desenvolvimento — pwa x1,1 (4 fluxos) | 5,4 | 6,5 | 8,6 |
| F4 Testes com cliente | 1 | 1,5 | 2 |
| F5 Deploy | 0,5 | 0,5 | 1 |
| **Faixa** | **9** | **12** | **16** |

## Vendido × realizado
- **Provável da régua = vendido (12).** Projeto no prazo.
- Sprints: S1–S3 Delivery, S4–S5 Overdelivery.
- No real, imersão e setup ocuparam S1 e S2, e o login (Better Auth + Google + guarda de rotas + recuperar senha) ficou na S3, cerca de 2 semanas.

## Lição para a régua
A proposta original tinha **14 sprints** e foi cortada para um MVP de 6. Esse é o exemplo de "negociar escopo, não prazo": o corte foi no escopo, e o prazo do MVP foi cumprido.
