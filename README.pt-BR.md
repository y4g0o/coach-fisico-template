🇧🇷 Português · [🇺🇸 English](README.md)

# Coach físico

Um coach de musculação e alimentação que vive numa pasta. As regras, o estado do aluno e os scripts são arquivos comuns, então qualquer agente ou modelo pode assumir o papel de coach.

Os dados em `dados/` são de um aluno fictício, só para demonstração. Licença MIT; `referencias/hypertrophy-training/` é de disco-trooper/skills (MIT) e `referencias/taco/` é a Tabela TACO (NEPA/UNICAMP).

## O que é o quê

| Peça | Onde | Para quê |
|---|---|---|
| Regras do coach | `AGENTS.md` | Persona, método, erros que não se repetem, comandos |
| Procedimentos | `.agents/skills/*/SKILL.md` | Check-in, fotos, medidas, ficha, treino, dieta |
| Estado do aluno | `dados/estado.md` | Fonte da verdade: ficha atual, peso, decisões, pendências |
| Dados | `dados/` | Log de treino, peso, medidas, fotos, fichas, dieta, check-ins |
| Programa | `./coach` | Um comando para tudo; só precisa de Python 3 |
| Evidências | `referencias/evidencias.md` | Fonte conferida de cada regra |

## Comandos

```
./coach importar <arquivo>       export do Hevy/Strong/FitNotes ou CSV manual -> dados/treinos/log.csv
./coach treino [--semanas N]     sessões, séries por músculo, progressão
./coach ficha <ficha.md>         confere séries por sessão e por músculo
./coach peso | medidas           médias semanais e circunferências
./coach taco "<alimento>" [g]    macros pela Tabela TACO
./coach contexto [--skill nome] ["tarefa"]   pacote único para colar em qualquer modelo
python3 -m unittest discover tests
```

## Dados de treino sem depender de app

Tudo vira o log canônico `dados/treinos/log.csv`, uma linha por série:

```
inicio,fim,sessao,exercicio,serie,tipo,kg,reps,rpe,distancia_km,duracao_s,fonte
```

- **Hevy, Strong, FitNotes:** `./coach importar export.csv` (o formato é detectado pelo cabeçalho; `--lb` se os pesos estiverem em libras). Hevy foi testado com export real; Strong e FitNotes seguem descrições de terceiros.
- **Qualquer outra fonte** (outro app, caderno, treino ditado): um CSV com `inicio,exercicio,kg,reps` e, se tiver, `sessao,rpe,tipo`. Exemplo em `tests/exemplos/manual.csv`.
- **Nomes de exercício:** o nome canônico é a chave de `scripts/musculos.json`. Nomes em português ou de outros apps entram em `scripts/apelidos.json`. O que não for reconhecido aparece como `NAO MAPEADOS`.

## Como ligar em cada agente ou modelo

| Onde | Como | Situação |
|---|---|---|
| Antigravity CLI (`agy`) | `cd coach-fisico-template && agy` | Lê `AGENTS.md` e `.agents/skills` |
| Claude Code | `cd coach-fisico-template && claude` | Lê `CLAUDE.md` (que importa o `AGENTS.md`) e `.claude/skills` (atalho para `.agents/skills`) |
| opencode, Codex CLI, Cursor e outros que leem `AGENTS.md` | abrir a pasta | Leem `AGENTS.md`; Codex e Gemini CLI também leem `.agents/skills` |
| Modelo sem acesso a arquivos (ChatGPT, Gemini, modelo local) | `./coach contexto --skill checkin-semanal "check-in da semana" > contexto.md` e colar ou anexar | O pacote traz regras, estado, ficha e números já calculados. O modelo termina com um bloco `ATUALIZAR ESTADO`, que alguém aplica no `dados/estado.md` |
| Modelo local pelo Ollama | `./coach contexto "pergunta" \| ollama run <modelo>` | Precisa de janela de contexto de ~32 mil tokens ou mais |

Observações:
- O pacote de contexto tem dados pessoais de saúde. Colar num serviço de terceiros é decisão do dono dos dados.
- Fotos não entram no pacote. Para avaliação visual, use um agente que leia arquivos ou anexe as fotos junto.
- Um agente por vez edita o `dados/estado.md`. O histórico fica no git.

## Para outra pessoa usar

O que é específico de um aluno fica todo em `dados/` (os arquivos deste repositório são um aluno fictício de exemplo). O resto (método, skills, scripts, evidências) serve para qualquer aluno: troque `dados/perfil.md` e `dados/estado.md`, apague os CSVs de exemplo e importe os seus treinos.
