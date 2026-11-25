"""Pacote unico de contexto em Markdown, para colar em qualquer modelo sem acesso a arquivos
(chat web, modelo local...). Junta regras, estado, ficha atual, numeros dos scripts e, se pedido, uma skill.

Uso: python3 scripts/contexto.py [--skill checkin-semanal] [--semanas 4] ["tarefa ou pergunta"]
Saida no stdout. Ex.: ./coach contexto --skill checkin-semanal "check-in da semana" > /tmp/contexto.md
"""
import argparse
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

ap = argparse.ArgumentParser()
ap.add_argument("tarefa", nargs="?", default="")
ap.add_argument("--skill")
ap.add_argument("--semanas", default="4")
a = ap.parse_args()


def rodar(*args):
    r = subprocess.run([sys.executable, *args], cwd=RAIZ, capture_output=True, text=True)
    return (r.stdout + r.stderr).strip()


def arquivo(rel):
    return (RAIZ / rel).read_text(encoding="utf-8").strip()


fichas = sorted(p for p in (RAIZ / "dados/fichas").glob("*.md") if re.fullmatch(r"\d{4}-\d{2}-\d{2}\.md", p.name))
partes = [
    f"# Coach fisico: pacote de contexto ({date.today():%d/%m/%Y})",
    "Voce vai atuar como o coach descrito em REGRAS. Voce NAO tem acesso aos arquivos nem aos scripts: "
    "onde as regras mandam ler um arquivo ou rodar um comando, use as secoes abaixo. Todo numero de treino, peso "
    "ou medida vem da secao NUMEROS; nao calcule nem invente outros. Fotos nao estao incluidas: se a tarefa "
    "depender delas, peca. Termine a resposta com um bloco `ATUALIZAR ESTADO` listando o que deve mudar em "
    "dados/estado.md, para ser aplicado depois.",
    "## REGRAS (AGENTS.md)\n\n" + arquivo("AGENTS.md"),
    "## PERFIL (dados/perfil.md)\n\n" + arquivo("dados/perfil.md"),
    "## ESTADO (dados/estado.md)\n\n" + arquivo("dados/estado.md"),
]
if fichas:
    rel = fichas[-1].relative_to(RAIZ)
    partes.append(f"## FICHA ATUAL ({rel})\n\n" + fichas[-1].read_text(encoding="utf-8").strip())
    partes.append("## NUMEROS\n\n### Ficha conferida\n```\n" + rodar("scripts/ficha.py", str(rel)) + "\n```")
else:
    partes.append("## NUMEROS")
partes.append(f"### Treino, ultimas {a.semanas} semanas\n```\n" + rodar("scripts/treino.py", "--semanas", a.semanas) + "\n```")
partes.append("### Peso\n```\n" + rodar("scripts/peso.py") + "\n```")
partes.append("### Medidas\n```\n" + rodar("scripts/medidas.py") + "\n```")
if a.skill:
    partes.append(f"## PROCEDIMENTO (skill {a.skill})\n\n" + arquivo(f".agents/skills/{a.skill}/SKILL.md"))
if a.tarefa:
    partes.append("## TAREFA\n\n" + a.tarefa)
print("\n\n".join(partes))
