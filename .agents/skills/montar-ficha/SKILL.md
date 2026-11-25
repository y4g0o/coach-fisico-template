---
name: montar-ficha
description: >-
  Use quando o aluno pedir para montar, revisar, trocar ou ajustar a ficha/treino/rotina da academia,
  trocar exercício, reorganizar a divisão semanal ou definir séries, repetições, RIR e descanso.
---

# Montar ou revisar a ficha

## Pré-requisitos (não pule)

1. `dados/estado.md`: a proposta de volume tem que estar aprovada pelo aluno. Se não estiver, discuta o volume primeiro e não entregue ficha.
2. `./coach treino --semanas 4`: cargas e reps atuais de cada exercício. A ficha nova parte delas.
3. Critério: o objetivo de `dados/perfil.md`. Divisão e número de dias são meio, não restrição. Recomende UMA estrutura, a que melhor entrega volume e frequência nos pontos fracos do ranking da última avaliação (`relatorios/` + `dados/estado.md`) com aderência realista (frequência real das últimas semanas no `./coach treino`) e sessões de ~60–80 min. Mostre a atual só como ponto de comparação dos números (`./coach ficha` nas duas), sem debate de divisão.
   A ficha atual está indicada em `dados/estado.md`.
4. Consulta: `referencias/hypertrophy-training/references/programs.md`, `periodization.md` e `exercises.md` (com a ressalva do AGENTS.md).

## Regras de montagem

- Prioridade de volume: pela ordem de pontos fracos da última avaliação (não existe lista fixa). Ponto forte fica em volume de manutenção/progressão. Glúteo sem trabalho específico além do que vem dos compostos.
- Cada exercício tem que ter uma função que nenhum outro da sessão cumpre (ângulo, comprimento muscular, estabilidade). Escreva a função.
- Mantenha exercícios que ele já progride. Troca só com motivo (estagnação de 3+ sessões com RIR e alimentação ok, desconforto, falta de estímulo distinto).
- Ele treina perto da falha: use isso. Compostos RIR 1–2, isoladores RIR 0–1. Menos séries com esforço alto em vez de mais séries.
- Descanso: compostos 2–3 min, isoladores 60–120 s.
- Progressão dupla: faixa de reps (ex.: 6–10); atingiu o topo em todas as séries com o RIR-alvo → sobe a carga no menor incremento.
- Halteres: escreva a carga **por mão** na ficha e diga que no app ele registra a soma.
- Aquecimento fica fora da contagem e escrito à parte ("2 aproximações").

## Formato do arquivo

Salve em `dados/fichas/AAAA-MM-DD.md`. Um `## ` por dia. Use o nome canônico (chave de `scripts/musculos.json`, que é o nome em inglês do Hevy) na coluna Exercício; apelidos de `scripts/apelidos.json` também valem. Assim bate com o script e com o app dele:

```markdown
## Seg — Peito
| Exercício | Séries | Reps | RIR | Descanso | Função |
|---|---|---|---|---|---|
| Bench Press (Barbell) | 3 | 6–10 | 1–2 | 2–3 min | Composto principal, carga máxima |
```

## Validação obrigatória

1. `./coach ficha dados/fichas/AAAA-MM-DD.md`
2. Confira na saída: nenhum `NAO MAPEADOS`; séries por sessão dentro do combinado; séries semanais por músculo batendo com a proposta aprovada (diferença > 1 série = corrija a ficha ou explique).
3. Cole a saída do script na resposta. Não escreva totais de cabeça.
4. Compare os totais com a média das semanas reais cheias do `./coach treino` (não com a ficha teórica). Ponto fraco do ranking que cair mais de 1 série precisa de justificativa explícita.
5. Duração estimada por sessão = séries × (descanso + ~1 min) + ~10 min de aquecimento. Acima de 85 min: corte e diga onde.

## Entrega

- Ficha + saída do script + o que mudou em relação ao que ele fazia, e por quê (Fatos / Interpretação / Recomendação).
- Critério de revisão: em 4 semanas ou antes se houver estagnação/dor.
- Atualize `dados/estado.md` ("Ficha atual: dados/fichas/AAAA-MM-DD.md, em uso desde ...") e o histórico de decisões.
- Lembre: no app, marcar aquecimento como aquecimento (`warmup`) e anotar RPE.
