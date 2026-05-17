# Semana piloto AutoForce — 2026-05-17

## Resumo estratégico
Esta semana piloto foi montada a partir de sinais reais sobre a mudança de descoberta em busca com IA, mais leituras de CRM/operação que reforçam a tese central da AutoForce: tecnologia sem processo e sem visão única aumenta vazamento, não resultado.

A semana foi pensada para Instagram-first e organizada em dois tipos de saída:
- posts simples headline-first
- um carrossel de tendência/notícia da semana

## Backbone da semana
1. **Autoridade** — IA está mudando a descoberta, e site fraco perde relevância antes mesmo do clique.
2. **Produto** — concessionária não precisa de mais ferramenta solta; precisa de visão única entre site, CRM e operação.
3. **Awareness** — o jogo está saindo de ranking puro para reconhecimento, autoridade e estrutura.
4. **Lead gen** — descobrir onde a operação perde lead antes da venda acontecer.
5. **Fechamento** — responder mais rápido não resolve se os sistemas continuam quebrados.

## O que ficou forte
- Tese da semana com boa conexão entre notícia real e leitura AutoForce.
- Material com cara mais executiva e menos genérica.
- Ponte clara entre IA search, site, CRM e operação comercial.
- Carrossel com narrativa natural para Instagram.

## O que ainda precisa de curadoria humana
- Refino do peso comercial vs institucional em alguns títulos.
- Validação visual final das artes (aqui ainda estão em formato placeholder/review base).
- Decidir se o fechamento da semana entra como novo simples ou vira uma segunda rota de carrossel.

## Conteúdo do pacote
- `weekly-research.md` — shortlist, fontes e scoring
- `portal.json` — estrutura para o portal
- `post-01-ia-sem-operacao.svg`
- `post-02-visao-unica-crm-site.svg`
- `post-03-reconhecimento-mais-que-ranking.svg`
- `post-04-diagnostico-de-leads.svg`
- `post-05-velocidade-sem-processo.svg`
- `carousel-01-cover.svg`
- `carousel-01-slide-02.svg` até `carousel-01-slide-07.svg`

## Publicação
Quando aprovado, este pacote pode ser publicado com:

```bash
python3 scripts/publish_week.py \
  --source /data/.openclaw/workspace/deliverables/autoforce-pilot-week-2026-05-17 \
  --week-date 2026-05-17 \
  --publish
```
