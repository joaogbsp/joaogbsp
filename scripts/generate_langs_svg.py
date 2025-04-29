import os
from github import Github
import pygal
from pygal.style import Style

# 1) Autenticação e coleta de bytes por linguagem
token = os.getenv("LANGS_TOKEN")
g = Github(token)
user = g.get_user()

lang_totals = {}
for repo in user.get_repos(affiliation="owner,collaborator,organization_member"):
    for lang, size in repo.get_languages().items():
        lang_totals[lang] = lang_totals.get(lang, 0) + size

# 2) Cálculo de porcentagens e top 6
total = sum(lang_totals.values()) or 1
top6 = sorted(lang_totals.items(), key=lambda x: x[1], reverse=True)[:6]
languages, percentages = zip(*[(l, round(s/total*100,1)) for l, s in top6])

# 3) Estilo customizado
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

# 4) Gráfico de barras verticais
chart = pygal.Bar(
    width=800,
    style=custom_style,
    show_legend=False,
    show_y_guides=False,
    show_x_guides=False,
    show_values=True,
    value_formatter=lambda v: f'{v}%',
)
chart.title = 'Most Used Languages'
chart.x_labels = list(languages)      # nomes na horizontal, do maior para o menor
chart.truncate_label = 15             # evita rótulos muito longos

# adiciona os percentuais como única série
chart.add('', percentages)

# 5) Gera o SVG
os.makedirs('assets', exist_ok=True)
chart.render_to_file('assets/most_used_languages.svg')
