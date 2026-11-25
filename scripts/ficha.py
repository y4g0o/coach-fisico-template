"""Confere uma ficha: series por sessao e series semanais por musculo (mesmo criterio do treino.py).

A ficha e um Markdown com uma tabela por dia. Cabecalho de dia: '## Seg — Peito' (qualquer '## ').
Colunas obrigatorias da tabela: 'Exercício' (nome canonico de musculos.json ou apelido de apelidos.json) e 'Séries' (series de trabalho).

Uso: python3 scripts/ficha.py dados/fichas/AAAA-MM-DD.md
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

from importar import canonico

mapa = json.loads((Path(__file__).parent / "musculos.json").read_text())
dia, cols = None, None
por_dia = defaultdict(int)
semana = defaultdict(float)
nao_mapeados = []

for linha in open(sys.argv[1], encoding="utf-8"):
    linha = linha.strip()
    if linha.startswith("## "):
        dia, cols = linha[3:], None
        continue
    if not linha.startswith("|") or dia is None:
        continue
    cel = [c.strip() for c in linha.strip("|").split("|")]
    if cols is None:
        cols = [c.lower() for c in cel]
        continue
    if set("".join(cel)) <= set("-: "):
        continue
    ex = canonico(cel[cols.index("exercício")])
    series = int(cel[cols.index("séries")].split()[0])
    por_dia[dia] += series
    musc = mapa.get(ex)
    if not musc:
        nao_mapeados.append(ex)
        continue
    semana[musc[0]] += series
    for m in musc[1:]:
        semana[m] += 0.5 * series

print("# Series por sessao")
for d, n in por_dia.items():
    print(f"{d:30} {n:3d}")
print(f"{'TOTAL':30} {sum(por_dia.values()):3d}")
print("\n# Series semanais por musculo (primario=1, secundario=0.5)")
for m, n in sorted(semana.items(), key=lambda x: -x[1]):
    print(f"{m:20} {n:5.1f}")
if nao_mapeados:
    print("\nNAO MAPEADOS (adicione em scripts/apelidos.json ou scripts/musculos.json):", ", ".join(nao_mapeados))
