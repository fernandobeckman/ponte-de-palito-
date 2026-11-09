---
name: flambagem-euler
description: Verifica barras comprimidas de palito/madeira quanto à flambagem de Euler (eixos fraco e forte) e ao esmagamento, e calcula o fator de segurança. Use para toda barra com esforço de compressão na ponte.
---

# Flambagem de Euler

P_cr = π²·E·I / (K·L)². A resistência da barra é o menor valor entre flambagem no eixo fraco, flambagem no eixo forte e esmagamento (f_c·A).

```bash
python3 .claude/skills/flambagem-euler/scripts/flambagem.py --b 9.5 --h 2 --n 3 --L 100 --E 10000 --fc 40 --N 1500
```

## Cuidados
- **E e f_c precisam vir de ensaio** do lote de palitos (skill `propriedades-palito-madeira`). Os padrões do script são só ilustrativos.
- Seção composta (n palitos colados) só funciona como uma peça se a colagem for contínua; com colagem por pontos use n = 1 e some as cargas (conservador).
- Verifique os dois planos: no plano da treliça o comprimento é entre nós; fora do plano é entre pontos de contraventamento — geralmente maior.
- K = 1,0 para nós rotulados (hipótese de treliça). Não use K < 1 sem justificativa.
- Imperfeições reais reduzem a carga: adote fator de segurança ≥ 1,5 a 2,0 sobre Euler.
