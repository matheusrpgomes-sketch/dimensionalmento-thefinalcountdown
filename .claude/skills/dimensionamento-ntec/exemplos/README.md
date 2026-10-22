# Exemplos — base de precedentes do NTec

Cada projeto tem uma ficha `.md` (o que era, como a régua classificou, comparação com o realizado) e um `.json` (a entrada do script, para rodar de novo quando a régua mudar).

| Projeto | Formato | Perfis | Fluxos (comuns + RN) | Faixa da régua (otim. / prov. / cons.) | Vendido | Situação |
|---|---|---|---|---|---|---|
| [Projeto A](projeto-a.md) | PWA | 3, poucas diferenças | 4 + 0 | 9 / 12 / 16 | 12 | No prazo |
| [Projeto B](projeto-b.md) | App nativo, offline | nenhum | 0 + 1 | 9 / 12 / 18 | 12 | Em execução |
| [Projeto C](projeto-c.md) | Web + app | 5, grandes diferenças | 3 + 1 | 13 / 18 / 24 | 11 | Atrasou (~14) |
| [Projeto D](projeto-d.md) | App + painel web | 2–3, poucas diferenças | 5 + 0 | 13 / 18 / 23 | 18 | Em execução, sem atraso |
| [Projetos E e F](projetos-e-f-pendente.md) | ? | ? | ? | não calibrado | 34 / 38 | Em execução |
| [PetAgenda (fictício)](ficticio-petagenda.md) | App + painel web | 4 | 4 + 0 | 14 / 18 / 24 | — | Resposta completa de exemplo (sem PRD) |
| [PetAgenda via PRD (fictício)](ficticio-petagenda-prd.md) | App + painel web | 4 | 3 + 1 | 14 / 19 / 26 | — | Como ler a PRD e traduzir para a régua |
| [PetAgenda proposta (fictício)](ficticio-petagenda-proposta.json) | App + painel web | 4 | 3 + 1 | 14 / 19 / 26 | — | JSON modelo da Proposta Técnica (`scripts/gerar_proposta.py`) |

**`fluxos_por_formato` (desde 22/10/2026):** com mais de um formato, o JSON diz em que código cada fluxo existe. Nos Projetos C e D, todos os fluxos estão como `compartilhado` (mesmo resultado de antes), porque as fichas não dizem onde cada jornada vive. É um palpite a conferir no hand-off: se as jornadas forem de um código só, a régua do C cai (o que aproxima do realizado) e a do D pode ficar abaixo do vendido. Os PetAgenda já usam a distribuição pela Superfície da PRD.

Os projetos reais desta tabela são **anteriores ao formato de PRD**: os fluxos foram contados a partir das tasks do Notion, e não pela regra "1 módulo = 1 fluxo". Quando um projeto com PRD terminar, ele vira o primeiro precedente para conferir essa regra.

**Números da tabela = saída do script hoje.** O fator Claude Code saiu da régua em 20/10/2026. As faixas acima são as que `scripts/calcular_faixa.py` calcula para cada `.json`, e `scripts/testar_exemplos.py` confere isso a cada mudança (também no CI do repositório). Mudou um peso? Rode `python scripts/testar_exemplos.py --atualizar`, confira a diferença e atualize esta tabela e a ficha `.md` do exemplo.

## Como achar um precedente

1. Mesmo **formato** primeiro (app com lojas, PWA, web).
2. Depois o número de **fluxos** e o tipo de **níveis de acesso**.
3. Se nenhum bate, escrever "sem precedente comparável". Não forçar.

## Como adicionar um projeto novo

Quando um projeto terminar:
1. Criar `nome.json` com os fatores, como a área de projetos classificaria hoje.
2. Rodar `python ../scripts/calcular_faixa.py nome.json`.
3. Criar `nome.md` no mesmo formato dos outros, com **vendido × realizado** e a causa dos desvios (puxar da retrospectiva).
4. Atualizar a tabela acima e a tabela de Calibração em `regua-dimensionamento.md`.
5. Se 2 ou mais projetos errarem para o mesmo lado no mesmo fator, ajustar o peso no script **e** na régua, e registrar no "Registro das fontes".

Não copiar valores de contrato nem dados pessoais de clientes para estas fichas.
