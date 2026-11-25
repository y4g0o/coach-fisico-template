---
name: registrar-treino
description: >-
  Use quando o aluno enviar um export de app de treino (Hevy, Strong, FitNotes ou outro), um treino escrito/colado ou print de treino,
  ou pedir análise de progressão, volume semanal, frequência ou duração das sessões.
---

# Registrar e analisar treino

## Entrada

O log canônico é `dados/treinos/log.csv` (uma linha por série, independente de app). Tudo entra nele por `./coach importar`.

- Export de app (hoje ele usa o Hevy: Perfil > Configurações > Exportar dados): salve em `dados/treinos/<app>-AAAA-MM-DD.csv` e rode `./coach importar <arquivo>`. O formato é detectado pelo cabeçalho (Hevy, Strong, FitNotes). Esses apps exportam o histórico inteiro, então reimportar substitui o que veio do mesmo app, sem duplicar. Pesos em libras: `--lb`.
- Treino colado, print ou ditado: transcreva para CSV com as colunas `inicio,sessao,exercicio,kg,reps,rpe,tipo` (data `AAAA-MM-DD` ou com hora; `tipo` = `aquecimento` só no aquecimento), salve em `dados/treinos/manual-AAAA-MM-DD.csv`, mostre a tabela ao aluno para confirmar e só então importe. Não chute número ilegível.
- App sem adaptador: converta para esse mesmo CSV.
- Confira a saída do importador: número de sessões, período e `NAO MAPEADOS`. Nome não mapeado: acrescente o apelido em `scripts/apelidos.json` (nome do app → nome canônico) ou, se for exercício novo, em `scripts/musculos.json` (primário primeiro), e importe de novo.

## Análise

1. `./coach treino --semanas 4`
   - Mostra sessões (duração, minutos de cardio, séries), séries semanais por músculo e progressão por exercício.
   - Critério de contagem: primário = 1 série, secundários = 0,5. Diga isso ao apresentar números.
   - Se aparecer `NAO MAPEADOS`, adicione o exercício em `scripts/musculos.json` (primário primeiro) e rode de novo.
2. Para um exercício específico ao longo do ano: `--exercicio "Nome canônico"` (chave de `scripts/musculos.json`).
3. Compare com a ficha atual e com a divisão acordada em `dados/estado.md`: dias pulados, músculo sem estímulo há mais de 10 dias, sessão acima de ~25 séries, exercício estagnado há 3+ sessões na mesma carga e reps.

## Cuidados conhecidos neste histórico

- Halteres: ele costuma anotar a soma dos dois (supino inclinado 56–60 = 28–30/mão; remada 64–72 = 32–36/mão; elevação lateral 32 = 16/mão), mas nem sempre. Confirme antes de concluir progressão.
- Elevação lateral na máquina: passou a ser anotada em número de placas. Flexoras: há séries com peso e reps invertidos.
- Boxe/aeróbico registrados dentro da sessão de musculação inflam a duração; o script separa em "cardio".
- O aluno deve marcar aquecimento como `warmup` e anotar RPE no app (o `./coach treino` mostra o RPE na progressão; RPE 9 = RIR 1). Se faltar, cobre no check-in.
- O app está em português, mas o export vem em inglês (ex.: "Abdominal na Polia (Corda)" = `Cable Crunch`). Nome novo em `NAO MAPEADOS`: mapeie em `scripts/musculos.json`.

## Saída

Resposta com Fatos / Hipóteses / Interpretação / Recomendação. Atualize `dados/estado.md` se houver mudança de ficha, recorde relevante ou nova pendência. Análises longas vão para `relatorios/AAAA-MM-DD-<tema>.md`.
