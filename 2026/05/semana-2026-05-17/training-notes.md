# Resumo operacional de treinamento — rodada AutoForce

## O que funcionou
- Travar o modo visual antes do prompt evitou mistura confusa entre campanha e produto.
- Referenciar explicitamente `autoforce-brand-campaign` vs `autoforce-product-saas` melhorou bastante a coerência.
- Mencionar a palette oficial com azuis AutoForce e neutros controlados ajudou a sair do look SaaS genérico.
- Pedir headline dominante, poucos elementos e leitura mobile elevou a qualidade geral.
- O post 2 funcionou melhor porque conectou tese de mercado + operação + marca em uma composição só.
- O post 3 funcionou porque o prompt restringiu bem o produto: base clara, cards executivos, azul só como acento.

## O que ainda ficou genérico
- Quando o prompt fala de "diagnóstico", "funil" e "leads" sem ancoragem automotiva explícita, a imagem tende a parecer B2B genérica.
- Inserir logo como referência não garante aplicação perfeita; o modelo ainda pode transformar a marca em badge/sticker visual.
- Temas de IA e busca escorregam facilmente para estética tech genérica se não houver menção forte a site, autoridade e contexto de concessionária.
- Elementos de dashboard pequenos demais viram ruído visual se o prompt não limitar a densidade.

## Correções que treinaram melhor o agente
- "integrated directly without sticker or badge"
- "less landing-page style, more Instagram campaign style"
- "slight automotive/dealership context"
- "blue only as accent" para produto
- "no fake dashboards" e "no generic SaaS cards clutter"

## Regras práticas para próximas rodadas
1. Sempre declarar o modo visual no começo do prompt.
2. Sempre explicitar se a peça é de tese, produto, awareness ou oferta.
3. Em peças comerciais, ancorar a dor no contexto de concessionária para evitar visual SaaS abstrato.
4. Em peças de produto, pedir poucos módulos de UI e um benefício central.
5. Sempre revisar se a peça parece AutoForce ou apenas uma empresa azul de martech.
6. Se a logo sair como adesivo ou placa branca, considerar a rodada fraca e regenerar.

## Avaliação honesta
- Post 2: muito bom, mais próximo de identidade real AutoForce.
- Post 3: bom, com leitura de produto convincente.
- Post 1: bom, mas ainda com acabamento visual abaixo do ideal de marca madura.
- Post 4: bom/publicável, porém mais conceitual do que proprietário.
- Post 5: aceitável após regeneração, ainda o mais fraco e mais genérico do lote.

## Próxima melhoria recomendada
Criar prompts base por família de post com blocos fixos de contexto automotivo (concessionária, showroom, leads, CRM, atendimento, site, mídia, operação comercial) para reduzir deriva genérica nas peças de awareness e lead gen.
