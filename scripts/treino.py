"""Resumo do treino: sessoes, series semanais por musculo e progressao.

Le o log canonico (dados/treinos/log.csv), que nao depende de app. Com um arquivo
como argumento (export do Hevy/Strong/FitNotes ou CSV canonico), le direto sem gravar.

Uso:
  python3 scripts/treino.py [arquivo] [--semanas 8] [--exercicio "Bench Press (Barbell)"]
"""
import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

import importar


def e1rm(kg, reps):
    return kg * (1 + reps / 30) if kg and reps else 0.0


def num(x):
    return float(x) if x not in ("", None) else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("arquivo", nargs="?", default=importar.LOG)
    ap.add_argument("--semanas", type=int, default=8)
    ap.add_argument("--exercicio")
    a = ap.parse_args()

    if not Path(a.arquivo).exists():
        sys.exit(f"{a.arquivo} nao existe. Importe um export primeiro: ./coach importar <arquivo>")
    mapa = json.loads((Path(__file__).parent / "musculos.json").read_text())
    cardio = set(mapa["_cardio"])
    linhas = importar.ler(a.arquivo)
    if not linhas:
        sys.exit("Nenhuma serie encontrada.")

    sessoes = {}
    for r in linhas:
        k = (r["sessao"], r["inicio"])
        s = sessoes.setdefault(k, {"titulo": r["sessao"], "ini": datetime.fromisoformat(r["inicio"]),
                                   "fim": datetime.fromisoformat(r["fim"]) if r["fim"] else None,
                                   "series": 0, "cardio_min": 0.0, "linhas": []})
        if r["exercicio"] in cardio:
            s["cardio_min"] += (num(r["duracao_s"]) or 0) / 60
        elif r["tipo"] != "aquecimento":
            s["series"] += 1
        s["linhas"].append(r)
    ordem = sorted(sessoes.values(), key=lambda s: s["ini"])
    ultimo = ordem[-1]["ini"]
    corte = ultimo - timedelta(weeks=a.semanas)
    recentes = [s for s in ordem if s["ini"] > corte]

    print(f"# Sessoes das ultimas {a.semanas} semanas (ate {ultimo:%d/%m/%Y})")
    print("data/hora        | treino               | duracao | cardio | series | por musculo (primario)")
    for s in recentes:
        dur = f"{(s['fim'] - s['ini']).total_seconds() / 60:5.0f}m" if s["fim"] else "    - "
        por = defaultdict(int)
        for r in s["linhas"]:
            if r["exercicio"] not in cardio and r["tipo"] != "aquecimento":
                por[(mapa.get(r["exercicio"]) or ["?"])[0]] += 1
        det = ", ".join(f"{m} {n}" for m, n in sorted(por.items(), key=lambda x: -x[1]))
        print(f"{s['ini']:%d/%m %a %H:%M} | {s['titulo'][:20]:20} | {dur}  | {s['cardio_min']:4.0f}m  | {s['series']:6} | {det}")

    semana = defaultdict(lambda: defaultdict(float))
    nao_mapeados = set()
    for s in recentes:
        iso = s["ini"].isocalendar()
        chave = f"{iso[0]}-S{iso[1]:02d}"
        for r in s["linhas"]:
            ex = r["exercicio"]
            if ex in cardio or r["tipo"] == "aquecimento":
                continue
            musc = mapa.get(ex)
            if not musc:
                nao_mapeados.add(ex)
                continue
            semana[chave][musc[0]] += 1
            for m in musc[1:]:
                semana[chave][m] += 0.5
    musculos = sorted({m for w in semana.values() for m in w})
    print("\n# Series semanais por musculo (primario=1, secundario=0.5; aquecimento marcado excluido)")
    print("semana   | " + " | ".join(f"{m[:10]:>10}" for m in musculos))
    for k in sorted(semana):
        print(f"{k} | " + " | ".join(f"{semana[k].get(m, 0):>10.1f}" for m in musculos))
    if nao_mapeados:
        print("\nNAO MAPEADOS (adicione em scripts/musculos.json ou em scripts/apelidos.json):", ", ".join(sorted(nao_mapeados)))

    alvo = [a.exercicio] if a.exercicio else sorted({r["exercicio"] for s in recentes for r in s["linhas"]} - cardio)
    print("\n# Progressao (melhor serie por sessao; e1RM = Epley, so referencia)")
    for ex in alvo:
        pontos = []
        for s in ordem if a.exercicio else recentes:
            series = [r for r in s["linhas"] if r["exercicio"] == ex and r["tipo"] != "aquecimento"]
            if not series:
                continue
            melhor = max(series, key=lambda r: e1rm(num(r["kg"]) or 0, num(r["reps"]) or 0))
            kg, reps = num(melhor["kg"]), num(melhor["reps"])
            rpes = [r["rpe"] for r in series if r.get("rpe")]
            rpe = f" RPE {'/'.join(rpes)}" if rpes else ""
            pontos.append(f"{s['ini']:%d/%m} {kg or 0:g}x{reps or 0:g} ({len(series)}s{rpe})")
        if pontos:
            print(f"- {ex}: " + " -> ".join(pontos))


if __name__ == "__main__":
    main()
