# Memorial de cálculo: ponte de palito UCB 2026/2 (Pratt, 8 painéis, vão de 800 mm)

Gerado por `projeto/gerar_memorial_ucb.py` a partir dos resultados dos scripts. Números com 5 casas decimais.
Regras da competição: `docs/requisitos.md`. Erros já cometidos e como evitá-los: `ERROS.md`.

## 1. Objetivo

Ponte só de palito de picolé e cola branca para a IV Competição da Ponte de Palito de Picolé (UCB, 2026/2).
A meta da equipe é **garantir o bônus de 30 kgf** com folga, numa ponte simples de construir em dois dias.
A nota premia a carga por peso: NF = (carga de ruptura ÷ peso) × 0,8 + estética × 0,2.

## 2. Regras que definem o projeto

| regra | valor exigido | projeto | situação |
|---|---|---|---|
| Vão livre | 800 mm | 800 mm entre as bordas dos blocos | ✓ |
| Comprimento total | 1000 a 1100 mm | 1020 mm | ✓ (ver nota) |
| Largura | 200 a 250 mm | 220 mm | ✓ |
| Altura | até 300 mm | 116,4 mm | ✓ |
| Peso | até 1 kg | 462,19250 g (estimado) | ✓ |
| Palitos por seção | até 5 | 3 | ✓ |
| Materiais | palito e cola branca | palito e cola branca, inclusive os espaçadores provisórios | ✓ |
| Ligações | encaixe ou sobreposição | sobreposição (chapas coladas nas duas faces) | ✓ |
| Apoio | só no topo dos blocos, sem usar a face vertical | a ponta da ponte apoia no rolete pela transversina do nó b0 | ✓ |

**Nota sobre o comprimento.** O regulamento pede comprimento de 100 a 110 cm e, no item dos apoios, “prolongamento
de até 10 cm de cada lado”. As duas frases só fecham juntas com exatamente 100 cm, e o regulamento não tem tolerância.
Adotamos 1020 mm (110 mm além de cada apoio), 20 mm acima do mínimo. **Confirmar com a organização**;
se exigirem no máximo 100 mm de cada lado, basta lixar 10 mm de cada ponta do banzo inferior (fica 1000 mm, sem folga).

## 3. Material (valores com origem)

| propriedade | valor | origem |
|---|---|---|
| Palito | 8,4 × 2,0 × 110 mm, parte reta útil 101,6 mm | palito tradicional (o regulamento cita cerca de 115 × 8,4 mm); espessura e comprimento **[PENDENTE: medir o lote comprado]** |
| Módulo de elasticidade E | 7350 MPa | valor usual em pontes de palito; abaixo do Pinus elliottii da NBR 7190 (conservador) |
| Resistência à tração f_t | 52,55 MPa | AVILA (2009), média de 8 palitos (fonte secundária) |
| Resistência à compressão f_c0 | 40,4 MPa | ABNT NBR 7190, Pinus elliottii |
| Compressão normal às fibras f_c90 | 10,1 MPa | 0,25 × f_c0 (ABNT NBR 7190) |
| Densidade | 560 kg/m³ | ABNT NBR 7190, Pinus elliottii |
| Cisalhamento da cola PVA τ | 2,0 MPa | **estimativa conservadora [PENDENTE ensaio]** |
| Consumo de cola | 200 g/m² | ficha técnica Cascola Cascorez Extra (Henkel) |

## 4. Escolha do formato

O script `estudo_ucb.py` comparou Pratt, Howe, Warren e Parker com 6 a 12 painéis e várias alturas, dimensionando cada barra
com o menor número de palitos (1 a 5) e estimando o peso da ponte inteira. Foram 4470 combinações viáveis.
Melhor resultado teórico de cada tipo (carga-alvo, peso e eficiência são do modelo simplificado, sem emendas nem chapas reais):

| tipo | painéis | altura (mm) | carga-alvo (kgf) | peso (g) | kgf por kg | barra mais longa (mm) | palitos por barra |
|---|---|---|---|---|---|---|---|
| Pratt | 6 | 120 | 160 | 357,84705 | 447,11839 | 179,38165 | 5 |
| Parker | 6 | 150 | 160 | 358,32611 | 446,52062 | 166,66667 | 5 |
| Warren | 6 | 135 | 160 | 381,55013 | 419,34201 | 150,56375 | 5 |
| Howe | 6 | 135 | 160 | 405,09021 | 394,97375 | 189,74398 | 5 |

Os formatos mais eficientes no papel usam barras de 5 palitos com até 180 mm, muitas emendas e ângulos diferentes em cada nó.
Com dois dias até a entrega e a meta de garantir o bônus, escolhemos a **Pratt de 8 painéis de 100 mm e 100 mm de altura**:

- todo montante tem 100 mm entre eixos e cabe num palito;
- as diagonais são todas iguais (141,42136 mm, 45°), então há poucos tipos de corte;
- todas as barras têm 3 palitos, logo as chapas das duas faces ficam planas;
- na Pratt as diagonais trabalham tracionadas (com a carga no centro) e as barras comprimidas são curtas.

## 5. Geometria adotada

| item | valor |
|---|---|
| Treliças | 2 treliças Pratt, 8 painéis de 100 mm, altura entre eixos de 100 mm |
| Barras | 3 palitos colados face a face (seção 8,4 × 6,0 mm). Banzos contínuos com emendas desencontradas entre as camadas |
| Nós | chapas de palito nas duas faces (2 mm cada); cada ponta de barra entra 40 mm na chapa |
| Largura | 220 mm entre as faces externas das treliças |
| Travamento | transversinas inferiores nos nós b0 a b8 (menos b4), escoras superiores nos nós t1 a t7 e diagonais em zigue-zague em cima e embaixo |
| Ponto de carga | mini-treliça transversal no meio do vão (altura 70 mm), apoiada em consolos colados nas faces internas do nó b4; a haste de aço é pendurada no nó do meio |

Conferência do modelo físico peça por peça (`verificar_modelo.py`):

```
Caixa da ponte: x -110.00000 a 910.00000 | y 260.00000 a 376.40000 | z -110.00000 a 110.00030
comprimento 1020.00000 mm (regra 1000 a 1100) | largura 220.00030 mm (200 a 250) | altura 116.40000 mm (até 300)
prolongamento além dos apoios: esquerda 110.00000 mm, direita 110.00000 mm

806 peças conferidas, 0 pares que se atravessam

RESULTADO: OK
```

## 6. Hipóteses de cálculo

- Treliça plana com nós articulados, resolvida pelo método da rigidez direta (`calculo_ucb.py`, que usa o solver da skill `analise-trelica`).
- Carga total P no meio do vão: P/2 em cada treliça, no nó b4. Peso próprio desprezado (ver item 11).
- **Envoltória**: carga no centro e carga deslocada um painel para cada lado (a haste pode não ficar exatamente no meio).
  Cada caso usa a resistência do seu próprio sinal (tração ou compressão).
- Tração: f_t × área dos palitos efetivos. Barras com emenda (banzos contínuos e diagonais maiores que um palito) contam 2 dos 3 palitos.
- Compressão: menor entre a flambagem de Euler (comprimento entre nós, K = 1, eixo mais fraco) e o esmagamento f_c0 × área.
  Os nós do banzo superior são travados fora do plano pelas escoras e pelo contraventamento. Nas emendas comprimidas o topo dos palitos encosta.
- Nenhum coeficiente reduz as resistências: o resultado é uma **estimativa da carga de colapso**, comparada depois com os 30 kgf do bônus.

## 7. Esforços, resistências e carga de colapso de cada barra

Saída de `calculo_ucb.py` para P = 1000 N (N > 0 tração, N < 0 compressão; “N desloc” é o caso deslocado que governa):

```
========================================================================================================
PONTE UCB — PRATT 8 PAINÉIS · VÃO 800 mm · ALTURA 100 mm · LARGURA 220 mm · 3 PALITOS POR BARRA
Esforços para carga total de 1000.00000 N (101.97162 kgf), metade em cada treliça
Reações por treliça: {'b0': [0.0, 250.0], 'b8': [0.0, 250.0]} | equilíbrio = [0.0, 0.0]
========================================================================================================
barra         L (mm)     N/1000 N     N desloc        R (N)  P colapso (kgf)  modo
b0-b1      100.00000    250.00000    312.50000   1765.68000        576.15761  tração (emenda: 2 efetivos) (carga deslocada)
b1-b2      100.00000    250.00000    312.50000   1765.68000        576.15761  tração (emenda: 2 efetivos) (carga deslocada)
b2-b3      100.00000    500.00000    625.00000   1765.68000        288.07880  tração (emenda: 2 efetivos) (carga deslocada)
b3-b4      100.00000    750.00000    937.50000   1765.68000        192.05254  tração (emenda: 2 efetivos) (carga deslocada)
b4-b5      100.00000    750.00000    937.50000   1765.68000        192.05254  tração (emenda: 2 efetivos) (carga deslocada)
b5-b6      100.00000    500.00000    625.00000   1765.68000        288.07880  tração (emenda: 2 efetivos) (carga deslocada)
b6-b7      100.00000    250.00000    312.50000   1765.68000        576.15761  tração (emenda: 2 efetivos) (carga deslocada)
b7-b8      100.00000    250.00000    312.50000   1765.68000        576.15761  tração (emenda: 2 efetivos) (carga deslocada)
t1-t2      100.00000   -500.00000   -625.00000   1096.82888        178.95267  flambagem (carga deslocada)
t2-t3      100.00000   -750.00000   -937.50000   1096.82888        119.30178  flambagem (carga deslocada)
t3-t4      100.00000  -1000.00000   -750.00000   1096.82888        111.84542  flambagem
t4-t5      100.00000  -1000.00000   -750.00000   1096.82888        111.84542  flambagem
t5-t6      100.00000   -750.00000   -937.50000   1096.82888        119.30178  flambagem (carga deslocada)
t6-t7      100.00000   -500.00000   -625.00000   1096.82888        178.95267  flambagem (carga deslocada)
b0-t1      141.42136   -353.55339   -441.94174    548.41444        126.53865  flambagem (carga deslocada)
t7-b8      141.42136   -353.55339   -441.94174    548.41444        126.53865  flambagem (carga deslocada)
b1-t1      100.00000      0.00000      0.00000   2648.52000                —  tração
b2-t2      100.00000   -250.00000   -312.50000   1096.82888        357.90534  flambagem (carga deslocada)
b3-t3      100.00000   -250.00000   -187.50000   1096.82888        447.38168  flambagem
b4-t4      100.00000      0.00000      0.00000   2648.52000                —  tração
b5-t5      100.00000   -250.00000   -187.50000   1096.82888        447.38168  flambagem
b6-t6      100.00000   -250.00000   -312.50000   1096.82888        357.90534  flambagem (carga deslocada)
b7-t7      100.00000      0.00000      0.00000   2648.52000                —  tração
t1-b2      141.42136    353.55339    441.94174   1765.68000        407.40495  tração (emenda: 2 efetivos) (carga deslocada)
t2-b3      141.42136    353.55339    441.94174   1765.68000        407.40495  tração (emenda: 2 efetivos) (carga deslocada)
t3-b4      141.42136    353.55339   -265.16504    548.41444        210.89774  flambagem (carga deslocada)
t5-b4      141.42136    353.55339   -265.16504    548.41444        210.89774  flambagem (carga deslocada)
t6-b5      141.42136    353.55339    441.94174   1765.68000        407.40495  tração (emenda: 2 efetivos) (carga deslocada)
t7-b6      141.42136    353.55339    441.94174   1765.68000        407.40495  tração (emenda: 2 efetivos) (carga deslocada)
--------------------------------------------------------------------------------------------------------
Barra crítica: t3-t4 (flambagem) -> colapso calculado das barras = 111.84542 kgf
```

As oito barras mais críticas:

| barra | L (mm) | N centro (N/1000 N) | N deslocado | resistência (N) | colapso (kgf) | modo |
|---|---|---|---|---|---|---|
| t3-t4 | 100,00000 | -1000,00000 | -750,00000 | 1096,82888 | 111,84542 | flambagem |
| t4-t5 | 100,00000 | -1000,00000 | -750,00000 | 1096,82888 | 111,84542 | flambagem |
| t2-t3 | 100,00000 | -750,00000 | -937,50000 | 1096,82888 | 119,30178 | flambagem (carga deslocada) |
| t5-t6 | 100,00000 | -750,00000 | -937,50000 | 1096,82888 | 119,30178 | flambagem (carga deslocada) |
| b0-t1 | 141,42136 | -353,55339 | -441,94174 | 548,41444 | 126,53865 | flambagem (carga deslocada) |
| t7-b8 | 141,42136 | -353,55339 | -441,94174 | 548,41444 | 126,53865 | flambagem (carga deslocada) |
| t1-t2 | 100,00000 | -500,00000 | -625,00000 | 1096,82888 | 178,95267 | flambagem (carga deslocada) |
| t6-t7 | 100,00000 | -500,00000 | -625,00000 | 1096,82888 | 178,95267 | flambagem (carga deslocada) |

### Conferência à mão

- **Equilíbrio**: com 500 N por treliça no centro, cada apoio recebe 250 N (a saída mostra 250 + 250 = 500 N e resíduo 0).
- **Banzo superior no meio** (seção pelo nó t4): M = 250 N × 400 mm = 100000 N·mm; N = M ÷ 100 mm = 1000 N de compressão. Igual à tabela.
- **Diagonal da ponta**: a força vertical de 250 N passa por uma barra a 45°: N = 250 × √2 = 353,55339 N. Igual à tabela.
- **Flambagem de t3-t4**: I = 8,4 × 6³ ÷ 12 = 151,20000 mm⁴; P_cr = π² × 7350 × 151,20000 ÷ 100² = 1096,82888 N.
  A barra recebe 1000 N quando P = 1000 N, então o colapso é 1096,82888 ÷ 9,80665 = 111,84542 kgf. Igual à tabela.

## 8. Ligações coladas

Cada ponta de barra de alma entra 40 mm entre as chapas das duas faces. Resistência da cola de uma ponta:
R = τ × 2 faces × 8,4 mm × 40 mm = 2,0 × 2 × 8,4 × 40 = 1344,00000 N.
Comparada à barra mais carregada, a ligação leva a ponte ao colapso com **137,04986 kgf**.
Os banzos passam inteiros pelos nós e não dependem das chapas.

## 9. Ponto de carga: mini-treliça e consolos

O regulamento põe a carga no centro, numa haste de aço de 8 mm pendurada na ponte (figura 5 do regulamento).
Uma haste ou viga de palito de 200 mm entre as treliças, carregada no meio, teria emendas perto do meio do vão.
Por isso a carga entra numa mini-treliça transversal de 70 mm de altura, que se apoia em consolos colados nos nós b4 das duas treliças.

```
MINI-TRELIÇA DO PONTO DE CARGA (vão 194.00000 mm, altura 70.00000 mm):
 banzo de baixo (tração) -> 259.86490 kgf | banzo de cima (flambagem) -> 762.88458 kgf
 diagonais (tração) -> 439.53631 kgf | ligações (3 faixas, 2 faces) -> 140.51779 kgf
 cola dos consolos nas treliças (30 x 8,4 mm por lado) -> 102.78739 kgf
```

Consolo: 30 × 8,4 mm colados na chapa interna de cada treliça; R = 2,0 × 30 × 8,4 = 504,00000 N por lado;
os dois juntos seguram 2 × 504,00000 ÷ 9,80665 = **102,78739 kgf**. É o elo mais fraco calculado, e depende do τ da cola, que ainda é estimado.

## 10. Apoio nos blocos

Pela figura 4 do regulamento, o rolete fica na quina interna do bloco, embaixo do nó da ponta da treliça.
Na carga de colapso calculada, cada ponta de treliça recebe R = P/4 = 252,00000 N, sobre a transversina do nó b0
(8,4 mm × 10 mm de banzo com chapas = 84,00000 mm²): σ = 3,00000 MPa, contra f_c90 = 10,10000 MPa
(fator 3,36667). A ponte não usa a face vertical dos blocos.

## 11. Carga de colapso estimada e eficiência

| modo de colapso | carga (kgf) |
|---|---|
| Cola dos consolos que seguram a mini-treliça | 102,78739 |
| Barras (pior: t3-t4, flambagem) | 111,84542 |
| Ligações coladas das barras de alma (chapas, 40 mm) | 137,04986 |
| Mini-treliça do ponto de carga (pior parte: ligações) | 140,51779 |

- **Carga de colapso estimada: 102,78739 kgf.**
- Fator sobre o bônus: 102,78739 ÷ 30 = **3,42625**.
- Peso estimado da ponte: 462,19250 g (palitos e cola seca), 537,80750 g abaixo do limite de 1 kg.
- Relação carga ÷ peso estimada: 102,78739 ÷ 0,46219 = 222,39087 kgf/kg; parcela de 80% da nota: 177,91270.
- Peso próprio ÷ carga de colapso: 0,44966%. Por isso foi desprezado.
- A carga inicial do ensaio (10 kg) é 9,72882% da carga de colapso estimada.

## 12. Quantitativo (do modelo físico, peça por peça)

| item | quantidade |
|---|---|
| Peças da ponte | 778 peças em 46 tipos (códigos no manual de corte) |
| Espaçadores provisórios | 28 peças (saem antes da entrega) |
| Palitos na ponte | 530 |
| Palitos dos espaçadores | 28 |
| Palitos para ensaios de material | 50 |
| **Palitos a comprar** (com 15% de perda) | **700** |
| Área colada | 2853,53976 cm² |
| Cola na ponte | 57,07080 g; comprar ao menos 171,21239 g |

Os tipos com mais peças:

| código | peça | comprimento (mm) | quantidade |
|---|---|---|---|
| C5 | Chapa de ligação | 40,0 | 192 |
| B2 | Banzo | 100,0 | 82 |
| X1 | Diagonal de contraventamento | 76,4 | 70 |
| T3 | Transversina | 73,3 | 40 |
| E1 | Escora superior | 73,3 | 35 |
| C8 | Chapa de ligação | 24,2 | 32 |
| M2 | Montante | 91,6 | 30 |
| X2 | Diagonal de contraventamento | 38,2 | 28 |

## 13. Riscos e pendências

1. **τ da cola [PENDENTE ensaio]**: governa os consolos e as ligações. Teste caseiro: colar dois palitos com só 5 mm de sobreposição
   (42,0 mm²), esperar 24 h, pendurar um balde e encher de água aos poucos até soltar. τ = massa (kg) × 9,80665 ÷ 42,0.
   Com τ = 2,0 MPa, deve soltar perto de 8,57 kg. Se soltar antes, avise: o reforço é aumentar os consolos.
2. **Propriedades do lote**: E, f_t e f_c são de literatura. A folga sobre o bônus (fator 3,4) cobre uma variação grande.
3. **Comprimento e prolongamento**: confirmar com a organização (item 2).
4. **Data**: o regulamento diz “2ª feira, 17/11”, mas 17/11/2026 é terça. Confirmar.
5. **Cura curta**: a cola branca fica bem mais forte com 24 h. Montar as treliças primeiro e deixar o ponto de carga por último.
6. **Emendas comprimidas**: cortar os palitos do banzo superior em esquadro e encostar bem as pontas antes de colar.

## 14. Cronograma até a entrega (17/11, 17:30)

| quando | tarefa |
|---|---|
| Dom 15/11 | Imprimir o manual de corte e o gabarito em 100%; cortar as peças por código e escrever o número em cada uma |
| Seg 16/11 manhã | Montar a treliça A e a treliça B no gabarito (chapas, 3 camadas, chapas); deixar prensadas |
| Seg 16/11 tarde | Levantar as treliças, encaixar os espaçadores, colar transversinas, escoras e contraventamentos |
| Seg 16/11 noite | Consolos e mini-treliça; tirar os espaçadores; deixar secar a noite toda |
| Ter 17/11 | Conferir medidas e peso, lixar rebarbas, transportar com cuidado; entrega às 17:30 |

## Referências

- ABNT NBR 7190: Projeto de estruturas de madeira (Pinus elliottii: f_c0, densidade, f_c90 = 0,25 f_c0).
- USDA Forest Products Laboratory. *Wood Handbook* (FPL-GTR-282), 2021.
- AVILA (2009), ensaio de tração em palitos, citado em trabalhos acadêmicos de ponte de palito (fonte secundária).
- Henkel. Ficha técnica Cascola Cascorez Extra (consumo de 160 a 200 g/m²; não adere a polietileno).
- Regulamento da IV Competição da Ponte de Palito de Picolé, UCB, Grupo PET Estruturas, 2026/2 (resumo em `docs/requisitos.md`).
