---
name: avaliacao-fotos
description: >-
  Use quando o aluno enviar fotos do shape/físico ou pedir avaliação visual, comparação de antes/depois
  ou análise de proporções. Define protocolo de padronização, onde salvar e como comparar sem
  estimar percentual de gordura.
---

# Avaliação por fotos

## Protocolo

**O protocolo vigente, completo e pronto para enviar, está em `dados/fotos/PROTOCOLO.md` (10 poses). Envie ao aluno ~2 dias antes de cada reavaliação.** Se uma limitação da avaliação vier de pose que o protocolo não pediu, é falha do protocolo: corrija o `PROTOCOLO.md`, não cobre o aluno. Resumo abaixo.


- Mesmo local, mesma luz (de preferência luz de teto/frontal, sem contraluz), mesma distância e altura da câmera (altura do umbigo, ~2–3 m, timer).
- Manhã, em jejum, depois do banheiro, antes do treino. Sem pump.
- Mesma roupa (sunga/short curto).
- Poses: frente relaxado, frente com dorsal aberta, lado direito relaxado, costas relaxado, costas com dorsal aberta, duplo bíceps de frente. Opcional: lado esquerdo.
- Poses extras (a partir de 12/2026), para os itens que as 6 poses não mostram: duplo bíceps de costas (deltoide posterior e espessura das costas), frente com quadríceps contraído e short dobrado até a virilha (coxa inteira), panturrilha de costas na ponta dos pés, lado com abdômen contraído (espessura do reto abdominal). Cabeça neutra, câmera mostrando os pés.
- Frequência: a cada 4 semanas. Mais que isso não mostra mudança real.

## Onde salvar

`dados/fotos/AAAA-MM-DD/` com nomes `frente.jpg`, `frente-dorsal.jpg`, `lado.jpg`, `costas.jpg`, `costas-dorsal.jpg`, `duplo-biceps.jpg` (extras: `costas-duplo-biceps.jpg`, `frente-quadriceps.jpg`, `panturrilha.jpg`, `lado-abdomen.jpg`). Se as fotos vierem pelo chat ou por `entrada/`, mova/copie para lá e renomeie.

## Como avaliar

1. Liste o que é comparável: mesmas poses, luz e distância parecidas? Se não, diga quais comparações não são confiáveis e por quê.
2. Avalie todas as regiões (ombros lateral/anterior/posterior, peito superior/inferior, costas, braços, quadríceps, posteriores, panturrilhas, cintura e abdômen) e termine com o ranking de pontos fracos e fortes em relação à proporção-alvo (definida no objetivo de `dados/perfil.md`). Esse ranking é o que define a prioridade de volume da ficha:
   - largura de ombro relativa à cintura (silhueta em V), arredondamento do deltoide lateral, deltoide posterior visível;
   - peitoral superior, densidade dos braços, largura de dorsal;
   - cintura e linha abdominal.
3. Use os rótulos Fatos / Hipóteses / Interpretação / Recomendação do AGENTS.md. "Fato" aqui é só o que é visível e comparável.
3b. Antes de fechar o ranking, confira:
   - cada item é UM músculo (ou porção), não região mista. Cintura (largura/gordura) ≠ reto abdominal (músculo); costas largura ≠ espessura;
   - músculo "aparecendo" por gordura baixa não é músculo grande: avalie espessura/relevo, não só definição;
   - "forte" só se estiver à frente da proporção-alvo; o resto é "menos atrasado";
   - rótulos de avaliação anterior foram reconferidos na foto atual, não copiados.
4. Cruze com dados: média de peso (`./coach peso`), cintura e volume semanal por músculo (`./coach treino`). Uma região que parece atrasada só vira recomendação depois de olhar volume, progressão e execução.
5. Dê nível de confiança (baixa/média/alta) para cada observação.

## Proibido

- Estimar percentual de gordura por foto.
- Afirmar mudança entre fotos com luz/pose diferentes.
- Comentários sobre aparência fora do objetivo de treino.

## Registro

Ao final, acrescente em `dados/estado.md` (seção Medidas) a data das fotos e 2–4 linhas com as observações principais. Se for a primeira série, marque como "referência".
