---
name: avaliacao-fisica
description: >-
  Use quando o aluno pedir avaliação física completa, reavaliação, medir o corpo, registrar
  circunferências/medidas com fita, comparar evolução de medidas ou avaliar proporção (V-taper,
  ombro/cintura). Para fotos, combine com a skill avaliacao-fotos.
---

# Avaliação física

Avaliação completa = medidas + peso médio + fotos + desempenho. Repetir a cada 4 semanas, no mesmo dia das fotos.

## Protocolo de medidas (fita métrica, passe ao aluno)

- Manhã, em jejum, antes de treinar, sem pump. Fita encostada sem apertar. Mesma pessoa medindo se possível. Medir 2x e anotar a média.
- **Ombros:** circunferência na parte mais larga dos deltoides, braços relaxados.
- **Peito:** linha dos mamilos, fim de expiração normal.
- **Cintura:** altura do umbigo, abdômen relaxado (não encolher), fim de expiração.
- **Quadril:** parte mais larga dos glúteos.
- **Braço:** ponto mais grosso, contraído, cada lado.
- **Coxa:** meio da coxa (entre virilha e joelho), relaxada, cada lado.
- **Panturrilha:** ponto mais grosso.

Registre em `dados/medidas.csv` (colunas no cabeçalho; vazio se não mediu). A cintura semanal continua em `dados/peso.csv`.

## Análise

1. `./coach medidas` → tabela, variação e razão ombro/cintura.
2. `./coach peso` → média de peso no mesmo período.
3. Leitura combinada (Fatos / Hipóteses / Interpretação / Recomendação):
   - Peso subindo + cintura estável + ombro/braço/coxa subindo = ganho de qualidade.
   - Peso subindo + cintura subindo mais rápido que o resto = superávit alto; reduzir um pouco.
   - Peso parado + medidas paradas = falta energia (olhar dieta antes de mexer no treino).
   - Variação abaixo de ~0,5–1 cm está dentro do erro da fita; não tire conclusão disso.
4. Razão ombro/cintura serve para acompanhar a silhueta em V **dele ao longo do tempo**, não para comparar com ideal de terceiros.
5. Cruze com as fotos (`avaliacao-fotos`) e com o volume por músculo (`./coach treino`).

## Proibido

- Estimar % de gordura por foto. Fórmulas por circunferência (ex.: Marinha dos EUA) têm erro de vários pontos percentuais; só mencione se ele pedir, como tendência, nunca como número absoluto.
- Diagnóstico médico.

Ao final, salve `relatorios/AAAA-MM-DD-avaliacao.md` e resuma 3–5 linhas em `dados/estado.md` (Medidas).
