import os
from github import Github
import pygal

# token do secret
token = os.getenv("LANGS_TOKEN")
g = Github(token)
user = g.get_user()

# 1) Coleta e soma bytes por linguagem
lang_totals = {}
for repo in user.get_repos(affiliation="owner,collaborator,organization_member"):
    for lang, size in repo.get_languages().items():
        lang_totals[lang] = lang_totals.get(lang, 0) + size

# 2) Calcula porcentagens e pega top6
total = sum(lang_totals.values()) or 1
top6 = sorted(lang_totals.items(), key=lambda x: x[1], reverse=True)[:6]
languages, percentages = zip(*[(lang, round(size/total*100,1)) for lang, size in top6])

# 3) Configura o gráfico
chart = pygal.HorizontalBar(
    width=600,
    style=pygal.style.DarkStyle,
    show_legend=False,     # não precisa de legenda agora
    show_values=True       # mostra valor no fim de cada barra
)
chart.title = 'Most Used Languages'
chart.y_labels = list(languages)        # textos no eixo Y
chart.add('', list(percentages))        # dados da série única
chart.value_formatter = lambda v: f'{v}%'  # formata os números

# 4) Gera arquivo
os.makedirs('assets', exist_ok=True)
chart.render_to_file('assets/most_used_languages.svg')
