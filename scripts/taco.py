"""Busca na Tabela TACO (4a ed., NEPA/UNICAMP). Valores por 100 g, ou pela quantidade pedida.

Uso:
  python3 scripts/taco.py "frango peito"          # lista correspondencias
  python3 scripts/taco.py "arroz branco cozido" 150 # macros para 150 g
"""
import csv
import sys
import unicodedata
from pathlib import Path

ARQ = Path(__file__).parent.parent / "referencias" / "taco" / "taco_composicao.csv"


def norm(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


def f(x):
    try:
        return float(x)
    except ValueError:
        return 0.0


termos = norm(sys.argv[1]).split()
gramas = float(sys.argv[2]) if len(sys.argv) > 2 else 100.0
achados = [r for r in csv.DictReader(open(ARQ, encoding="utf-8"))
           if all(t in norm(r["descricao"]) for t in termos)]
if not achados:
    print("Nada encontrado. Tente menos palavras.")
def val(r, campo, k, casas):
    return f"{f(r[campo]) * k:5.{casas}f}" if r[campo] else "  s/d"


for r in achados[:15]:
    k = gramas / 100
    print(f"{r['descricao'][:55]:55} {gramas:g} g: {val(r, 'energia_kcal', k, 0)} kcal | "
          f"P {val(r, 'proteina_g', k, 1)} | C {val(r, 'carboidrato_g', k, 1)} | G {val(r, 'lipideos_g', k, 1)}")
if any(not r["energia_kcal"] for r in achados[:15]):
    print("s/d = sem dado na TACO (ex.: leites fluidos). Use o rótulo do produto; nao conte como zero.")
