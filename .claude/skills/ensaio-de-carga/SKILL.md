---
name: ensaio-de-carga
description: Protocolo para ensaio de carga de modelos de ponte (prova ou ruptura): montagem, aplicação gradual da carga, medição de deslocamento, segurança, registro em CSV e análise dos resultados. Use ao planejar ou analisar um ensaio.
---

# Ensaio de carga

## Segurança
Óculos de proteção, ninguém sob a carga, carga suspensa a no máximo poucos centímetros do chão, área isolada.

## Procedimento
1. Pese a ponte (g) e fotografe todas as faces.
2. Posicione nos apoios conforme o regulamento; meça o vão real.
3. Zere o relógio comparador/régua no meio do vão.
4. Aplique carga em incrementos de ~5–10% da carga prevista; aguarde 30 s em cada passo.
5. Registre a cada passo em `dados/ensaio-AAAA-MM-DD.csv`:
   `passo,tempo_s,carga_N,deslocamento_mm,observacao`
6. Filme o ensaio (câmera lenta ajuda a identificar a barra que rompeu primeiro).
7. Na ruptura: anote carga máxima, barra/ligação que falhou e modo (flambagem, tração, colagem).

## Análise
- Curva carga × deslocamento (skill `data-storytelling` / gráfico simples).
- Eficiência = carga de ruptura (N) / peso da ponte (N).
- Compare com a previsão: barra que rompeu era a de menor FS? Se não, registre a lição em `ERROS.md`.
