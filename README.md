🇺🇸 English · [🇧🇷 Português](README.pt-BR.md)

# Coach físico

A strength-training and nutrition coach that lives in a folder. The rules, the trainee's state and the scripts are plain files, so any AI agent or model can take on the coach role.

The data in `dados/` belongs to a fictional trainee, for demonstration only. MIT license; `referencias/hypertrophy-training/` comes from disco-trooper/skills (MIT) and `referencias/taco/` is the TACO food composition table (NEPA/UNICAMP). File names, commands and content are in Portuguese.

## What is what

| Piece | Where | Purpose |
|---|---|---|
| Coach rules | `AGENTS.md` | Persona, method, mistakes that must not repeat, commands |
| Procedures | `.agents/skills/*/SKILL.md` | Weekly check-in, photos, body measurements, program, training log, diet |
| Trainee state | `dados/estado.md` | Source of truth: current program, weight, decisions, open items |
| Data | `dados/` | Training log, weight, measurements, photos, programs, diet, check-ins |
| Program | `./coach` | One command for everything; needs only Python 3 |
| Evidence | `referencias/evidencias.md` | Checked source for every rule |

## Commands

```
./coach importar <file>          Hevy/Strong/FitNotes export or manual CSV -> dados/treinos/log.csv
./coach treino [--semanas N]     sessions, sets per muscle, progression
./coach ficha <program.md>       checks sets per session and per muscle
./coach peso | medidas           weekly averages and circumferences
./coach taco "<food>" [g]        macros from the TACO table
./coach contexto [--skill name] ["task"]   single bundle to paste into any model
python3 -m unittest discover tests
```

## Training data without depending on an app

Everything becomes the canonical log `dados/treinos/log.csv`, one row per set:

```
inicio,fim,sessao,exercicio,serie,tipo,kg,reps,rpe,distancia_km,duracao_s,fonte
```

- **Hevy, Strong, FitNotes:** `./coach importar export.csv` (format detected from the header; `--lb` if weights are in pounds). Hevy was tested with a real export; Strong and FitNotes follow third-party descriptions.
- **Any other source** (another app, a notebook, a dictated workout): a CSV with `inicio,exercicio,kg,reps` and, if available, `sessao,rpe,tipo`. Example in `tests/exemplos/manual.csv`.
- **Exercise names:** the canonical name is the key in `scripts/musculos.json`. Portuguese names or names from other apps go in `scripts/apelidos.json`. Anything unrecognized shows up as `NAO MAPEADOS`.

## Plugging it into each agent or model

| Where | How | Notes |
|---|---|---|
| Antigravity CLI (`agy`) | `cd coach-fisico-template && agy` | Reads `AGENTS.md` and `.agents/skills` |
| Claude Code | `cd coach-fisico-template && claude` | Reads `CLAUDE.md` (which imports `AGENTS.md`) and `.claude/skills` (a link to `.agents/skills`) |
| opencode, Codex CLI, Cursor and others that read `AGENTS.md` | open the folder | Read `AGENTS.md`; Codex and Gemini CLI also read `.agents/skills` |
| Model without file access (ChatGPT, Gemini, a local model) | `./coach contexto --skill checkin-semanal "weekly check-in" > contexto.md`, then paste or attach | The bundle carries rules, state, program and precomputed numbers. The model ends with an `ATUALIZAR ESTADO` block that someone applies to `dados/estado.md` |
| Local model via Ollama | `./coach contexto "question" \| ollama run <model>` | Needs a context window of ~32k tokens or more |

Notes:
- The context bundle contains personal health data. Pasting it into a third-party service is the data owner's call.
- Photos are not in the bundle. For visual assessment, use an agent that reads files or attach the photos.
- Only one agent at a time edits `dados/estado.md`. History lives in git.

## Using it for someone else

Everything specific to a trainee lives in `dados/` (the files in this repository are a fictional example). The rest (method, skills, scripts, evidence) works for anyone: replace `dados/perfil.md` and `dados/estado.md`, delete the example CSVs and import your own workouts.
