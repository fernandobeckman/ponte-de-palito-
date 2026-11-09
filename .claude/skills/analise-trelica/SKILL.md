---
name: analise-trelica
description: Calcula esforços axiais, reações e deslocamentos de treliças 2D/3D (ponte de palito, treliça Pratt, Warren, Howe) pelo método da rigidez direta. Use sempre que precisar dos esforços nas barras, verificar estaticidade ou comparar geometrias.
---

# Análise de treliça

Script sem dependências: `scripts/trelica.py` (Python 3).

## Uso
```bash
python3 .claude/skills/analise-trelica/scripts/trelica.py .claude/skills/analise-trelica/exemplos/pratt_6paineis.json
```
Adicione `--json` para saída completa em JSON (útil para alimentar `ponte-3d-threejs`).

## Formato de entrada
Unidades: **mm, N, MPa**. Veja `exemplos/pratt_6paineis.json`.
- `dim`: 2 ou 3
- `nos`: id → coordenadas
- `barras`: `id`, `i`, `j` e opcionalmente `A` (mm²) e `E` (MPa)
- `apoios`: id → lista de 0/1 por direção (1 = restrito)
- `cargas`: id → força em N (gravidade = y negativo)

## Convenção
N > 0 tração, N < 0 compressão. O campo "equilíbrio" deve sair ~0; se não sair, o modelo está errado.

## Verificação obrigatória
1. Estaticidade (2D): b + r = 2n → isostática. Matriz singular = mecanismo/falta de apoio.
2. Confira uma barra pelo método das seções à mão. Exemplo validado: Pratt 600 mm × 100 mm, P = 1000 N no meio → banzo superior central = −1500 N (M = 500·300 = 150 000 N·mm; N = M/h).
3. Treliça ideal: cargas apenas nos nós. Peso do tabuleiro deve ser distribuído aos nós.

## Próximos passos
- Barras comprimidas → skill `flambagem-euler`.
- Dimensionamento → skill `dimensionamento-barras-palito`.
