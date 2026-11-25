"""Converte exports de apps de treino para o log canonico (dados/treinos/log.csv), que nao depende de app.

Fontes reconhecidas pelo cabecalho: Hevy, Strong, FitNotes e CSV canonico ("manual").
Formato canonico (uma linha por serie):
  inicio,fim,sessao,exercicio,serie,tipo,kg,reps,rpe,distancia_km,duracao_s,fonte
  - inicio/fim: AAAA-MM-DDTHH:MM (fim pode ficar vazio); tipo: trabalho | aquecimento
  - no CSV manual so `inicio`, `exercicio` e `reps` sao obrigatorios (data sem hora e aceita)
Nomes de exercicio viram o nome canonico (chaves de musculos.json) via apelidos.json.

Uso:
  python3 scripts/importar.py <arquivo.csv> [--fonte hevy|strong|fitnotes|manual] [--lb]
Hevy/Strong/FitNotes exportam o historico inteiro: reimportar substitui tudo que veio daquele app.
CSV manual substitui so as sessoes com o mesmo `inicio`.
"""
import argparse
import csv
import json
import re
import sys
import unicodedata
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

AQUI = Path(__file__).resolve().parent
LOG = str(AQUI.parent / "dados" / "treinos" / "log.csv")
CAMPOS = ["inicio", "fim", "sessao", "exercicio", "serie", "tipo", "kg", "reps", "rpe",
          "distancia_km", "duracao_s", "fonte"]
MESES = {"jan": 1, "fev": 2, "feb": 2, "mar": 3, "abr": 4, "apr": 4, "mai": 5, "may": 5, "jun": 6,
         "jul": 7, "ago": 8, "aug": 8, "set": 9, "sep": 9, "out": 10, "oct": 10, "nov": 11,
         "dez": 12, "dec": 12}
LB = 0.45359237
_apelidos = None


def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", s).strip()


def canonico(nome):
    """Nome canonico do exercicio; se nao houver apelido, devolve o proprio nome."""
    global _apelidos
    if _apelidos is None:
        mapa = json.loads((AQUI / "musculos.json").read_text(encoding="utf-8"))
        extra = json.loads((AQUI / "apelidos.json").read_text(encoding="utf-8"))
        _apelidos = {norm(k): k for k in list(mapa) + mapa["_cardio"] if not k.startswith("_")}
        _apelidos.update({norm(k): v for k, v in extra.items() if not k.startswith("_")})
    return _apelidos.get(norm(nome), nome.strip())


def iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M")


def data_texto(s):
    """'4 de nov. de 2026, 18:40' (pt) ou '4 Nov 2026, 18:40' (en)."""
    m = re.match(r"\s*(\d{1,2})\s+(?:de\s+)?([^\W\d_]{3})[^\W\d_]*\.?\s+(?:de\s+)?(\d{4}),?\s+(\d{1,2}):(\d{2})", s)
    if not m:
        raise ValueError(f"data nao reconhecida: {s!r}")
    d, mes, ano, h, mi = m.groups()
    return datetime(int(ano), MESES[norm(mes)], int(d), int(h), int(mi))


def data_iso(s):
    s = s.strip().replace("T", " ")
    for f in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, f)
        except ValueError:
            pass
    raise ValueError(f"data nao reconhecida: {s!r}")


def duracao(s):
    """'1h 5m', '45m', '00:10:00' ou segundos -> segundos (None se vazio)."""
    s = (s or "").strip()
    if not s:
        return None
    if ":" in s:
        p = [int(x) for x in s.split(":")]
        return sum(v * 60 ** i for i, v in enumerate(reversed(p)))
    m = re.findall(r"(\d+)\s*([hms])", s)
    if m:
        return sum(int(v) * {"h": 3600, "m": 60, "s": 1}[u] for v, u in m)
    return int(float(s))


def kg(valor, lb):
    if valor in ("", None):
        return ""
    v = float(str(valor).replace(",", "."))
    return f"{v * LB if lb else v:g}"


def linha(**c):
    return {k: ("" if c.get(k) is None else str(c.get(k)).strip()) for k in CAMPOS}


def de_hevy(rows, lb):
    for r in rows:
        peso = kg(r.get("weight_kg"), False) or kg(r.get("weight_lbs"), True)
        yield linha(inicio=iso(data_texto(r["start_time"])), fim=iso(data_texto(r["end_time"])),
                    sessao=r["title"], exercicio=canonico(r["exercise_title"]), serie=r["set_index"],
                    tipo="aquecimento" if r["set_type"] == "warmup" else "trabalho", kg=peso,
                    reps=r["reps"], rpe=r.get("rpe"), distancia_km=r.get("distance_km"),
                    duracao_s=r.get("duration_seconds"), fonte="hevy")


def de_strong(rows, lb):
    # Cabecalho varia entre versoes: "Duration" ou "Workout Duration", "Weight" ou "Weight (kg)".
    for r in rows:
        r = {k.split(" (")[0].replace("Workout Duration", "Duration"): v for k, v in r.items()}
        ini = data_iso(r["Date"])
        dur = duracao(r.get("Duration"))
        ordem = r["Set Order"].strip()
        yield linha(inicio=iso(ini), fim=iso(ini + timedelta(seconds=dur)) if dur else "",
                    sessao=r["Workout Name"], exercicio=canonico(r["Exercise Name"]), serie=ordem,
                    tipo="aquecimento" if ordem.upper().startswith("W") else "trabalho",
                    kg=kg(r.get("Weight"), lb), reps=r.get("Reps"), rpe=r.get("RPE"),
                    distancia_km=r.get("Distance"), duracao_s=r.get("Seconds"), fonte="strong")


def de_fitnotes(rows, lb):
    conta = defaultdict(int)
    for r in rows:
        ini = data_iso(r["Date"])
        ex = canonico(r["Exercise"])
        conta[ini, ex] += 1
        col = next(c for c in r if c.lower().startswith("weight") and "unit" not in c.lower())
        em_lb = lb or "lb" in col.lower() or "lb" in (r.get("Weight Unit") or "").lower()
        yield linha(inicio=iso(ini), sessao="", exercicio=ex, serie=conta[ini, ex], tipo="trabalho",
                    kg=kg(r[col], em_lb), reps=r.get("Reps"), distancia_km=r.get("Distance"),
                    duracao_s=duracao(r.get("Time")), fonte="fitnotes")


def de_manual(rows, lb):
    conta = defaultdict(int)
    for r in rows:
        ini = iso(data_iso(r["inicio"]))
        ex = canonico(r["exercicio"])
        conta[ini, ex] += 1
        yield linha(inicio=ini, fim=iso(data_iso(r["fim"])) if r.get("fim") else "", sessao=r.get("sessao"),
                    exercicio=ex, serie=r.get("serie") or conta[ini, ex], tipo=r.get("tipo") or "trabalho",
                    kg=kg(r.get("kg"), lb), reps=r.get("reps"), rpe=r.get("rpe"),
                    distancia_km=r.get("distancia_km"), duracao_s=r.get("duracao_s"),
                    fonte=r.get("fonte") or "manual")


FONTES = {"hevy": de_hevy, "strong": de_strong, "fitnotes": de_fitnotes, "manual": de_manual}


def detectar(cab):
    c = {x.strip().lower() for x in cab}
    if {"exercise_title", "set_type", "start_time"} <= c:
        return "hevy"
    if {"workout name", "exercise name", "set order"} <= c:
        return "strong"
    if {"exercise", "category", "reps"} <= c:
        return "fitnotes"
    if {"inicio", "exercicio", "reps"} <= c:
        return "manual"
    sys.exit(f"Formato nao reconhecido. Cabecalho: {sorted(c)}\n"
             "Converta para o CSV canonico (veja o topo de scripts/importar.py) e importe de novo.")


def ler(arquivo, fonte=None, lb=False):
    """Le um export ou o log canonico e devolve as series no formato canonico, em ordem."""
    with open(arquivo, encoding="utf-8-sig", newline="") as f:
        cab = f.readline()
        f.seek(0)
        rows = list(csv.DictReader(f, delimiter=";" if cab.count(";") > cab.count(",") else ","))
    if not rows:
        return []
    fonte = fonte or detectar(rows[0].keys())
    saida = list(FONTES[fonte](rows, lb))
    ordem = {id(r): i for i, r in enumerate(saida)}
    return sorted(saida, key=lambda r: (r["inicio"], ordem[id(r)]))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("arquivo")
    ap.add_argument("--fonte", choices=list(FONTES))
    ap.add_argument("--lb", action="store_true", help="pesos do arquivo estao em libras")
    ap.add_argument("--log", default=LOG)
    a = ap.parse_args()

    novas = ler(a.arquivo, a.fonte, a.lb)
    if not novas:
        sys.exit("Arquivo sem series.")
    fonte = novas[0]["fonte"]
    antigas = ler(a.log, "manual") if Path(a.log).exists() else []
    if fonte in ("hevy", "strong", "fitnotes"):
        antigas = [r for r in antigas if r["fonte"] != fonte]
    inicios = {r["inicio"] for r in novas}
    antigas = [r for r in antigas if r["inicio"] not in inicios]
    todas = sorted(antigas + novas, key=lambda r: r["inicio"])
    with open(a.log, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        w.writeheader()
        w.writerows(todas)

    mapa = json.loads((AQUI / "musculos.json").read_text(encoding="utf-8"))
    conhecidos = set(mapa) | set(mapa["_cardio"])
    fora = sorted({r["exercicio"] for r in novas} - conhecidos)
    print(f"Fonte: {fonte}. {len(inicios)} sessoes, {len(novas)} series, "
          f"de {novas[0]['inicio'][:10]} a {novas[-1]['inicio'][:10]}.")
    print(f"Log: {a.log} ({len({r['inicio'] for r in todas})} sessoes no total).")
    if fora:
        print("NAO MAPEADOS (adicione o apelido em scripts/apelidos.json ou o exercicio em scripts/musculos.json):")
        print("  " + ", ".join(fora))


if __name__ == "__main__":
    main()
