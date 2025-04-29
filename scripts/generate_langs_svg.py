import os
from github import Github
import pygal
from pygal.style import Style

# 1) Autentica e coleta bytes por linguagem
token = os.getenv("LANGS_TOKEN")
g = Github(token)
user = g.get_user()

lang_totals = {}
for repo in user.get_repos(affiliation="owner,collaborator,organization_member"):
    for lang, size in repo.get_languages().items():
        lang_totals[lang] = lang_totals.get(lang, 0) + size

# 2) Calcula porcentagens e ordena top6
total = sum(lang_totals.values()) or 1
top6 = sorted(lang_totals.items(), key=lambda x: x[1], reverse=True)[:6]
languages, percentages = zip(*[(l, round(s/total*100,1)) for l, s in top6])

# 3) Define um style customizado
custom_style = Style(
    font_family='sans-serif',
    background='transparent',
    plot_background='#1a1b23',
    foreground='#ffffff',
    foreground_strong='#ffffff',
    foreground_subtle='#aaaaaa',
    opacity='.8',
    opacity_hover='.9',
    transition='400ms ease-in',
    colors=('#61dafb', '#4fc08d', '#f56565', '#ecc94b', '#9f7aea', '#fd79a8')
)

# 4) Cria o gráfico
chart = pygal.HorizontalBar(
    width=700,
    style=custom_style,
    show_legend=False,
    show_values=True,
    value_formatter=lambda v: f'{v}%',
    show_y_guides=False,
    truncate_label=15
)
chart.title = 'Most Used Languages'
chart.y_labels = list(languages)
chart.add('', list(percentages))

# 5) Renderiza o SVG
os.makedirs('assets', exist_ok=True)
chart.render_to_file('assets/most_used_languages.svg')
