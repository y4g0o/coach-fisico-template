"""Media semanal de peso, variacao e cintura a partir de dados/peso.csv.

Formato do CSV: data,peso_kg,cintura_cm   (data AAAA-MM-DD; cintura opcional)
Uso: python3 scripts/peso.py [dados/peso.csv]
"""
import csv
import sys
from collections import defaultdict
from datetime import date

caminho = sys.argv[1] if len(sys.argv) > 1 else "dados/peso.csv"
semanas = defaultdict(lambda: {"peso": [], "cintura": []})
for r in csv.DictReader(open(caminho, encoding="utf-8")):
    if not r.get("peso_kg"):
        continue
    d = date.fromisoformat(r["data"])
    iso = d.isocalendar()
    k = f"{iso[0]}-S{iso[1]:02d}"
    semanas[k]["peso"].append(float(r["peso_kg"]))
    if r.get("cintura_cm"):
        semanas[k]["cintura"].append(float(r["cintura_cm"]))

print("semana   | n | media kg | var kg | var %  | cintura")
ant = None
for k in sorted(semanas):
    p = semanas[k]["peso"]
    media = sum(p) / len(p)
    c = semanas[k]["cintura"]
    cint = f"{sum(c) / len(c):.1f}" if c else "-"
    if ant is None:
        print(f"{k} | {len(p)} | {media:8.2f} |    -   |   -    | {cint}")
    else:
        print(f"{k} | {len(p)} | {media:8.2f} | {media - ant:+6.2f} | {100 * (media - ant) / ant:+5.2f}% | {cint}")
    ant = media
print("\nSemanas com menos de 4 pesagens sao pouco confiaveis.")
