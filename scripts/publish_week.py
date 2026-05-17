#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.webp'}
ROOT = Path(__file__).resolve().parent.parent


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-') or 'semana'


def load_meta(source: Path) -> dict[str, Any]:
    for name in ('portal.json', 'portal-meta.json', 'meta.json'):
        p = source / name
        if p.exists():
            return json.loads(p.read_text(encoding='utf-8'))
    raise SystemExit(f'Metadata file not found in {source}. Expected portal.json, portal-meta.json, or meta.json')


def ensure_week_index(target: Path, meta: dict[str, Any]) -> None:
    posts = meta.get('posts', [])
    approved_refs = meta.get('approvedReferences', [])
    week_title = meta.get('weekTitle') or f"Semana {meta['weekDate']}"
    week_summary = meta.get('weekSummary', '')
    buttons = []
    if (target / 'README.md').exists():
        buttons.append('<a href="README.md">Abrir README estratégico</a>')
    if (target / 'training-notes.md').exists():
        buttons.append('<a href="training-notes.md">Abrir notas de treinamento</a>')
    if (target / 'review-sheet.html').exists():
        buttons.append('<a href="review-sheet.html">Abrir review</a>')

    posts_html = []
    for post in posts:
        image = html.escape(post['image'])
        day = html.escape(post.get('day', ''))
        title = html.escape(post.get('title', ''))
        desc = html.escape(post.get('description', ''))
        posts_html.append(f'<article class="card"><img src="{image}" alt="{title}"><div class="meta"><div class="day">{day}</div><div class="title">{title}</div><div class="desc">{desc}</div></div></article>')

    refs_html = []
    for ref in approved_refs:
        image = html.escape(ref['image'])
        title = html.escape(ref.get('title', 'Referência aprovada'))
        desc = html.escape(ref.get('description', ''))
        refs_html.append(f'<article class="card"><img src="{image}" alt="{title}"><div class="meta"><div class="title">{title}</div><div class="desc">{desc}</div></div></article>')

    downloads = []
    seen = set()
    for entry in posts + approved_refs:
        image = entry['image']
        if image not in seen:
            seen.add(image)
            downloads.append(f'<p><a href="{html.escape(image)}">{html.escape(Path(image).name)}</a></p>')

    page = f'''<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(week_title)} — Portal AutoForce</title>
  <style>
    :root{{--bg:#0a1020;--panel:#131b34;--text:#eef2ff;--muted:#c7cde9;--blue:#1440FF;--line:rgba(255,255,255,.08)}}
    *{{box-sizing:border-box}}body{{margin:0;font-family:Inter,Arial,sans-serif;background:var(--bg);color:var(--text)}}
    .wrap{{max-width:1220px;margin:0 auto;padding:32px 20px 80px}} h1{{margin:0 0 8px;font-size:38px}}.lead{{color:var(--muted);max-width:860px;line-height:1.6}}
    .section{{margin-top:28px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px}}.card{{background:var(--panel);border:1px solid var(--line);border-radius:18px;overflow:hidden}}.card img{{display:block;width:100%;background:#fff}}.meta{{padding:16px}}.day{{font-size:12px;color:#8A92B7;text-transform:uppercase;letter-spacing:.08em}}.title{{font-size:20px;font-weight:700;margin-top:8px}}.desc{{font-size:14px;color:var(--muted);line-height:1.5;margin-top:8px}}.hero{{background:linear-gradient(135deg,#111936,#0e1d59);border:1px solid #223879;border-radius:24px;padding:24px}}.links a{{display:inline-block;margin:10px 10px 0 0;padding:10px 14px;border-radius:12px;background:var(--blue);color:#fff;text-decoration:none;font-weight:700;font-size:14px}}.small a{{color:#8db0ff;text-decoration:none}}.small{{color:var(--muted);font-size:14px;line-height:1.6}}.split{{display:grid;grid-template-columns:1.4fr 1fr;gap:18px}}.panel{{background:var(--panel);border:1px solid var(--line);border-radius:18px;padding:18px}}@media(max-width:900px){{.split{{grid-template-columns:1fr}}}}
  </style>
</head>
<body>
  <div class="wrap">
    <section class="hero">
      <h1>{html.escape(week_title)}</h1>
      <div class="lead">{html.escape(week_summary)}</div>
      <div class="links">{''.join(buttons)}</div>
    </section>

    <section class="section">
      <h2>Posts da semana</h2>
      <div class="grid">{''.join(posts_html)}</div>
    </section>

    <section class="section split">
      <div class="panel">
        <h2>Referências aprovadas</h2>
        <div class="small">{html.escape(meta.get('approvedSummary', 'Banco de referências positivas da semana.'))}</div>
        <div class="grid" style="margin-top:14px">{''.join(refs_html) or '<div class="small">Nenhuma referência aprovada informada.</div>'}</div>
      </div>
      <div class="panel small">
        <h2>Downloads rápidos</h2>
        {''.join(downloads)}
      </div>
    </section>
  </div>
</body>
</html>
'''
    (target / 'index.html').write_text(page, encoding='utf-8')


def find_weeks(root: Path) -> list[dict[str, str]]:
    weeks = []
    for p in root.glob('[0-9][0-9][0-9][0-9]/[0-9][0-9]/semana-*'):
        if p.is_dir():
            week = p.name
            weeks.append({
                'path': str(p.relative_to(root)).replace(os.sep, '/'),
                'weekDate': week.replace('semana-', ''),
            })
    weeks.sort(key=lambda x: x['weekDate'], reverse=True)
    return weeks


def load_week_card(root: Path, week_rel: str) -> dict[str, str]:
    meta_path = root / week_rel / 'portal.json'
    data = json.loads(meta_path.read_text(encoding='utf-8')) if meta_path.exists() else {}
    return {
        'title': data.get('weekTitle', week_rel.split('/')[-1].replace('semana-', 'Semana ')),
        'summary': data.get('homeSummary', data.get('weekSummary', 'Entrega semanal AutoForce.')),
        'link': f"{week_rel}/index.html",
        'year': week_rel.split('/')[0],
        'month': week_rel.split('/')[1],
        'weekDate': week_rel.split('/')[-1].replace('semana-', ''),
    }


def rebuild_home(root: Path) -> None:
    weeks = find_weeks(root)
    cards = [load_week_card(root, w['path']) for w in weeks]
    latest = cards[0] if cards else None
    latest_html = ''
    if latest:
        latest_html = f'''<article class="card"><h3>{html.escape(latest['title'])}</h3><p>{html.escape(latest['summary'])}</p><a href="{html.escape(latest['link'])}">Abrir semana</a></article>'''
    grouped: dict[str, dict[str, list[dict[str, str]]]] = {}
    for c in cards:
        grouped.setdefault(c['year'], {}).setdefault(c['month'], []).append(c)
    tree_parts = ['<strong>Estrutura</strong><ul>']
    for year in sorted(grouped.keys(), reverse=True):
        tree_parts.append(f'<li>{year}<ul>')
        for month in sorted(grouped[year].keys(), reverse=True):
            tree_parts.append(f'<li>{month}<ul>')
            for c in grouped[year][month]:
                tree_parts.append(f'<li><a href="{html.escape(c["link"])}" style="color:#8db0ff">semana-{html.escape(c["weekDate"])} </a></li>')
            tree_parts.append('</ul></li>')
        tree_parts.append('</ul></li>')
    tree_parts.append('</ul>')
    page = f'''<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Portal Semanal AutoForce</title>
  <style>
    :root{{--bg:#08101f;--panel:#121a34;--panel2:#0e1730;--text:#eef2ff;--muted:#c7cde9;--blue:#1440FF;--line:rgba(255,255,255,.08)}}
    *{{box-sizing:border-box}} body{{margin:0;font-family:Inter,Arial,sans-serif;background:linear-gradient(180deg,#08101f,#0d1530);color:var(--text)}}
    .wrap{{max-width:1180px;margin:0 auto;padding:40px 20px 80px}}
    .hero{{background:linear-gradient(135deg,#111936,#0c1f63);border:1px solid #243b93;border-radius:24px;padding:28px 28px 24px;box-shadow:0 16px 40px rgba(0,0,0,.25)}}
    h1{{margin:0 0 8px;font-size:42px;line-height:1.02}}.lead{{max-width:780px;color:var(--muted);font-size:16px;line-height:1.6}}
    .meta{{display:flex;gap:12px;flex-wrap:wrap;margin-top:18px}}.chip{{padding:8px 12px;border-radius:999px;background:rgba(255,255,255,.08);font-size:13px;color:#fff}}
    h2{{margin:34px 0 14px;font-size:24px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px}}
    .card{{background:var(--panel);border:1px solid var(--line);border-radius:20px;padding:18px;box-shadow:0 10px 24px rgba(0,0,0,.18)}}
    .card h3{{margin:0 0 8px;font-size:20px}}.card p{{margin:0;color:var(--muted);line-height:1.5;font-size:14px}}
    .card a{{display:inline-block;margin-top:14px;color:#fff;background:var(--blue);text-decoration:none;padding:10px 14px;border-radius:12px;font-size:14px;font-weight:700}}
    .tree{{background:var(--panel2);border:1px solid var(--line);border-radius:20px;padding:18px}}.tree ul{{margin:8px 0 0 20px;padding:0}}.tree li{{margin:8px 0;color:var(--muted)}}
    .footer{{margin-top:28px;color:var(--muted);font-size:14px}}
  </style>
</head>
<body>
  <div class="wrap">
    <section class="hero">
      <h1>Portal Semanal AutoForce</h1>
      <div class="lead">Acervo permanente das artes, planejamentos e entregas do agente da AutoForce. Cada semana fica guardada por ano, mês e semana para a equipe acessar, revisar e baixar sem perder histórico.</div>
      <div class="meta"><div class="chip">Instagram-first</div><div class="chip">Histórico por semana</div><div class="chip">Feito para social media</div></div>
    </section>
    <h2>Semana mais recente</h2>
    <div class="grid">{latest_html}</div>
    <h2>Arquivo</h2>
    <div class="tree">{''.join(tree_parts)}</div>
    <div class="footer">Portal atualizado automaticamente pelo fluxo semanal do agente.</div>
  </div>
</body>
</html>'''
    (root / 'index.html').write_text(page, encoding='utf-8')


def main() -> None:
    ap = argparse.ArgumentParser(description='Publish a weekly deliverable into the AutoForce content portal.')
    ap.add_argument('--source', required=True, help='Source deliverable directory containing files and portal.json metadata')
    ap.add_argument('--week-date', required=True, help='Week date in YYYY-MM-DD format')
    ap.add_argument('--publish', action='store_true', help='Also commit and push after publishing')
    args = ap.parse_args()

    source = Path(args.source).resolve()
    if not source.is_dir():
        raise SystemExit(f'Source directory not found: {source}')
    try:
        dt = datetime.strptime(args.week_date, '%Y-%m-%d')
    except ValueError as e:
        raise SystemExit(str(e))

    meta = load_meta(source)
    year = dt.strftime('%Y')
    month = dt.strftime('%m')
    week_slug = f'semana-{args.week_date}'
    target = ROOT / year / month / week_slug
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target)
    meta['weekDate'] = args.week_date
    (target / 'portal.json').write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')

    ensure_week_index(target, meta)
    rebuild_home(ROOT)
    print(target)

    if args.publish:
        os.system(f"git -C {ROOT} add . && git -C {ROOT} commit -m 'chore: publish {args.week_date}' && git -C {ROOT} push")


if __name__ == '__main__':
    main()
