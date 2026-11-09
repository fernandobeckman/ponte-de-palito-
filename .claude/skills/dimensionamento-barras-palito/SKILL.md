---
name: dimensionamento-barras-palito
description: Fluxo completo para dimensionar cada barra da ponte de palito (número de palitos por barra) a partir dos esforços da treliça, verificando tração, compressão/flambagem e ligações coladas. Use após a análise da treliça.
---

# Dimensionamento das barras

## Fluxo
1. Esforços: rode `analise-trelica` com a carga de projeto = carga alvo × fator de segurança (sugestão 1,5).
2. Para cada barra **tracionada**: n ≥ N / (f_t,k · A_palito). Verifique também a ligação: N ≤ n_colagens · R_colagem,k.
3. Para cada barra **comprimida**: aumente n até `flambagem-euler` dar fator ≥ 1,5 nos dois planos.
4. Barras nulas: mantenha a seção mínima (estabilidade e montagem), nunca remova sem verificar outras combinações de carga.
5. Monte a tabela final:

| barra | L (mm) | N (N) | tipo | n palitos | resistência (N) | FS | modo crítico |
|---|---|---|---|---|---|---|---|

6. Massa estimada = Σ (n · L / L_palito · massa_palito) + cola (estimar 10–20%).
7. Envie para o agente `revisor-seguranca-estrutural`.

## Erros comuns
- Esquecer a flambagem fora do plano (contraventamento insuficiente).
- Dimensionar barra e esquecer a ligação colada.
- Usar valor médio do material em vez do característico.
