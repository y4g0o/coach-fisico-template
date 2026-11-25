---
name: checkin-semanal
description: >-
  Use quando o aluno pedir o check-in/fechamento da semana, revisão semanal ou "como estou indo",
  ou quando ele mandar o resumo da semana (peso, treinos, sono, dieta).
---

# Check-in semanal

Ritmo: semanal nas 3 primeiras semanas de cada ficha nova, depois quinzenal. A cada ~4 semanas vira reavaliação completa (skill `avaliacao-fotos` + `avaliacao-fisica` + revisão da ficha). Em check-in quinzenal, analise as 2 semanas juntas.

## Perguntas (só as que não estiverem já respondidas nos dados)

1. Pesagens da semana (data e kg) e cintura na altura do umbigo, se mediu.
2. Treinos feitos vs. planejados; algum pulado e por quê.
3. Sono médio (horas) e qualidade 1–5.
4. Quantos dias cumpriu os 4 momentos do plano alimentar atual (`dados/dieta/`) e qual momento falhou mais. Apetite 1–5.
5. Dor, desconforto ou fadiga fora do normal.
6. Fotos? (só a cada 4 semanas; ver `avaliacao-fotos`)

## Passos

1. Adicione as pesagens em `dados/peso.csv` e rode `./coach peso`.
2. Se houver export novo ou treino colado, importe (skill `registrar-treino`) e rode `./coach treino --semanas 2` e compare com a ficha atual (`dados/estado.md` diz qual):
   - Aderência à semana 1→2→3→4 (regras em "Organização da semana" da ficha): quantos treinos, algum músculo zerado na semana.
   - Séries semanais por músculo executadas vs. `./coach ficha <ficha atual>`.
   - Progressão dupla: quem bateu o topo da faixa com o RPE-alvo (RPE 9 = RIR 1; RPE 8 = RIR 2) deve subir carga; quem ficou 3+ sessões sem progredir entra na lista de estagnados. RPE aparece na saída do script.
   - Registro: aquecimento marcado como warmup? RPE preenchido? Elevação lateral na máquina em kg? Cobre o que faltar.
   - Sessão com título "Extra…" = treino social com amigo (fora do plano). Conte no volume da semana, mapeie exercícios novos em `musculos.json`, veja se caiu colada num treino com os mesmos músculos e se atrapalhou a carga do treino seguinte. Não cobre aderência a ela nem trate como falha de plano.
   - Cardio extra (corrida/box) aparece na coluna cardio: relacione com o peso só se o peso parou de subir.
3. Escreva `dados/checkins/AAAA-Sxx.md` (semana ISO) com: números, aderência, o que funcionou, o que falhou, 1–3 ajustes para a próxima semana.
4. Atualize `dados/estado.md`.

## Regra de decisão

- Ajuste no máximo 1–2 variáveis por semana para conseguir saber o que funcionou.
- Peso: decida por tendência de 2–3 semanas, não por uma semana.
- Ficha: só mude exercício estagnado após checar carga, reps, RIR e sono/alimentação da semana.
