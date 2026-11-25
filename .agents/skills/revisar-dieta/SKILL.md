---
name: revisar-dieta
description: >-
  Use quando o aluno relatar o que comeu, mandar foto de prato, pedir avaliação da dieta, sugestão de
  refeições para ganhar peso, estimativa de proteína/calorias ou falar de apetite e suplementos.
---

# Revisar alimentação

## Registro

Salve o que ele relatar em `dados/dieta/AAAA-MM-DD.md`: refeição, horário, alimento, quantidade (medida caseira ou gramas) e se a quantidade é estimada.

## Estimativa de macros

- `./coach taco "<alimento>" <gramas>` usa a Tabela TACO (alimentos brasileiros).
- Medidas caseiras (colher, concha, unidade) estão em `referencias/taco/pof_medidas_caseiras.csv` (coluna `quantidade_g`); busque com grep.
- Produtos industrializados (whey etc.): peça o rótulo; não invente.
- Foto de prato: estimativa grosseira, sempre com faixa e aviso. Melhor pedir as quantidades.

## Como avaliar

1. A métrica principal é a média semanal de peso (`./coach peso`), não a conta de calorias. Se a média não sobe por 2–3 semanas com pesagens suficientes, falta energia, independentemente do que a conta diz.
2. Proteína diária vs. alvo de 1,6 g/kg (até 2,2 é opcional), distribuída em 3–5 refeições.
3. Ajuste à rotina real: manhã com pouco apetite (líquidos densos: leite+aveia+banana+whey), almoço como refeição principal, noite cansado (opções sem preparo). Uma mudança por vez, a mais fácil de manter.
4. Água: lembrete prático no trabalho (garrafa com marcação), não meta abstrata.

## Limites

- Não prescrever meta calórica exata sem pelo menos 2 semanas de peso + registro alimentar.
- Qualquer medicamento para apetite: só encaminhar a médico/farmacêutico.
- Suplemento novo só com justificativa e evidência; creatina e whey já cobrem o básico.

Atualize `dados/estado.md` (seção Alimentação) com padrões observados e mudanças combinadas.
