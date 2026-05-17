# Automação do Portal AutoForce

## Objetivo
Publicar uma nova semana no portal com estrutura fixa por data:
- `YYYY/MM/semana-YYYY-MM-DD/`

## Script principal
- `scripts/publish_week.py`

## Entrada esperada
O script recebe uma pasta de entrega com:
- arquivos da semana
- `portal.json`

## Metadados
Use `templates/portal-meta.example.json` como base.
O arquivo deve incluir:
- `weekTitle`
- `weekSummary`
- `homeSummary`
- `approvedSummary`
- `posts[]`
- `approvedReferences[]`

## Exemplo de uso
```bash
python3 scripts/publish_week.py \
  --source /caminho/para/entrega-da-semana \
  --week-date 2026-05-24
```

## O que o script faz
1. copia a entrega para a pasta da semana
2. salva `portal.json` dentro da semana
3. gera/atualiza `index.html` da semana
4. reconstrói a home do portal

## Publicação manual
Depois de revisar:
```bash
git add .
git commit -m "chore: publish 2026-05-24"
git push
```

## Publicação em um comando
Se quiser que o script já publique no GitHub:
```bash
python3 scripts/publish_week.py \
  --source /caminho/para/entrega-da-semana \
  --week-date 2026-05-24 \
  --publish
```

Nesse modo ele:
1. publica a semana localmente
2. faz `git add .`
3. cria o commit
4. faz `git push`

O GitHub Pages publica automaticamente.

## Regra operacional
A pasta de origem deve conter tudo que precisa aparecer naquela semana.
O script espelha a entrega da semana em vez de tentar adivinhar arquivos faltantes.
