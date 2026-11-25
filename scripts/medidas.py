"""Evolucao das circunferencias e razao ombro/cintura a partir de dados/medidas.csv.

Uso: python3 scripts/medidas.py [dados/medidas.csv]
"""
import csv
import sys

caminho = sys.argv[1] if len(sys.argv) > 1 else "dados/medidas.csv"
linhas = list(csv.DictReader(open(caminho, encoding="utf-8")))
if not linhas:
    sys.exit("Sem medidas registradas.")
campos = [c for c in linhas[0] if c.endswith("_cm")]


def v(r, c):
    return float(r[c]) if r.get(c) else None


print("data       | " + " | ".join(c[:-3][:9] for c in campos) + " | ombro/cintura")
for r in linhas:
    o, c = v(r, "ombros_cm"), v(r, "cintura_cm")
    razao = f"{o / c:.2f}" if o and c else "-"
    print(f"{r['data']} | " + " | ".join(f"{v(r, k):9.1f}" if v(r, k) else "        -" for k in campos) + f" | {razao}")

if len(linhas) > 1:
    a, b = linhas[0], linhas[-1]
    print(f"\nVariacao {a['data']} -> {b['data']}:")
    for k in campos:
        if v(a, k) and v(b, k):
            print(f"  {k[:-3]:12} {v(b, k) - v(a, k):+.1f} cm")
