import os
from github import Github
import pygal

# Pega token do secret
token = os.getenv("LANGS_TOKEN")
g = Github(token)

user = g.get_user()

# Agrupa bytes de todas as linguagens
lang_totals = {}
for repo in user.get_repos(affiliation="owner,collaborator,organization_member"):
    for lang, size in repo.get_languages().items():
        lang_totals[lang] = lang_totals.get(lang, 0) + size

# Calcula porcentagens e pega top 6
total = sum(lang_totals.values()) or 1
top6 = sorted(lang_totals.items(), key=lambda x: x[1], reverse=True)[:6]
lang_perc = [(lang, round(size/total*100,1)) for lang, size in top6]

# Gera SVG com Pygal
chart = pygal.HorizontalBar(
    width=600,
    show_legend=False,
    style=pygal.style.DarkStyle
)
chart.title = 'Most Used Languages'
for lang, pct in lang_perc:
    chart.add(f"{lang} {pct}%", pct)

os.makedirs('assets', exist_ok=True)
chart.render_to_file('assets/most_used_languages.svg')

