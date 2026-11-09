# Memorial de cálculo: Ponte de palito Parker, 8 painéis

> Versão 2, de 2026-11-09. Mudanças em relação à v1: todas as barras passaram a ter 3 camadas, as chapas ganharam 2 faixas sobre as pontas das barras e a transversina central foi para consolos (ver seção 9).
> Versão 1, de 2026-11-09. Cálculo reproduzível: `python3 projeto/calculo_ponte.py` (saída completa em `projeto/saida_calculo.txt`).
> Todos os números estão com 5 casas decimais. Unidades: mm, N, MPa, g.

## 1. Requisitos (informados pela equipe)

| item | valor |
|---|---|
| Vão livre entre apoios | 500 mm |
| Carga a resistir | 40 a 45 kg. Projeto feito para **45 kg = 441,29925 N** (g = 9,80665 m/s²) |
| Aplicação da carga | concentrada, no meio do vão |
| Materiais | somente palito de picolé e cola branca (PVA) |
| Limite de massa ou de palitos | nenhum |
| Fator de segurança (FS) | 2,0 com a carga no centro; 1,5 com a carga deslocada um painel (envoltória) |

O FS = 2,0 compensa a incerteza do material, que ainda não foi ensaiado, e as imperfeições de montagem. A verificação com a carga deslocada existe porque, na prática, a carga nunca fica exatamente no centro.

## 2. Material (valores com origem)

| propriedade | valor adotado | origem |
|---|---|---|
| Seção do palito | 8,40000 × 2,00000 mm | Menor largura citada em trabalhos de ponte de palito (8,4 a 10 mm). É a opção conservadora. **[MEDIR o seu lote]** |
| Comprimento do palito | 110 mm | Trabalhos citam de 105 a 115 mm. **[MEDIR]** |
| Módulo de elasticidade E | 7350 MPa | Valor mais usado nos trabalhos de ponte de palito. É menor que o do Pinus elliottii na NBR 7190, logo é conservador |
| Resistência à tração f_t | 52,55 MPa | Média de 8 palitos ensaiados (AVILA, 2009, citado em trabalhos acadêmicos) |
| Resistência à compressão f_c | 40,4 MPa | ABNT NBR 7190, Pinus elliottii (madeira usual dos palitos) |
| Densidade | 560 kg/m³ | ABNT NBR 7190, Pinus elliottii |
| Cisalhamento da cola PVA τ_k | 2,0 MPa | **ESTIMATIVA conservadora [PENDENTE ensaio]**. É bem abaixo do f_v da madeira (7,4 MPa na NBR 7190) |

Conferência dos valores: com E = 7350 MPa e b = 8,4 mm, Euler prevê 268,7 N para 2 palitos de 110 mm colados. Trabalhos publicados mediram 264,87 N (27 kgf). A concordância indica que os valores adotados são coerentes.

## 3. Estudo comparativo de geometrias

Script: `projeto/estudo_geometrias.py`. Foram comparadas 4 famílias de treliça (Pratt, Howe, Warren e Parker de banzo superior triangular), com 4, 6, 8 e 10 painéis e alturas de 60 a 180 mm, num total de 208 modelos. Cada barra foi dimensionada pelo número mínimo de camadas que atende à envoltória de FS. O critério de comparação é o consumo de palitos por treliça.

| tipo | variante | painéis | h (mm) | palitos/treliça | barras > 110 mm (precisam de emenda) | nós | N máx (N) | flecha (mm) |
|---|---|---|---|---|---|---|---|---|
| Pratt | melhor geral | 4 | 80 | 36.46272 | 10 | 8 | 344.76504 | 1.27431 |
| Pratt | sem emenda | 6 | 60 | 36.70551 | 0 | 12 | 459.68672 | 1.79433 |
| Howe | melhor geral | 4 | 70 | 35.35624 | 10 | 8 | 394.01719 | 1.69838 |
| Howe | sem emenda | 8 | 60 | 36.14744 | 0 | 16 | 459.68672 | 1.78984 |
| Warren | melhor geral | 4 | 60 | 33.05653 | 7 | 9 | 459.68672 | 1.65582 |
| Warren | sem emenda | 6 | 60 | 34.87729 | 0 | 13 | 459.68672 | 1.60080 |
| Parker | melhor geral | 10 | 60 | 32.54194 | 0 | 20 | 472.74036 | 4.10140 |
| **Parker** | **escolhida** | **8** | **90** | **33.86000** | **0** | **16** | **325.71146** | **1.97675** |

### Por que o Parker de 8 painéis e 90 mm de altura
1. **Forma que segue o momento fletor.** Com a carga no meio, o diagrama de momento é um triângulo. No Parker triangular o banzo superior acompanha esse triângulo, então os banzos ficam com força constante e a alma fica quase sem esforço. É a forma mais eficiente para esse carregamento.
2. **Nenhuma barra maior que um palito.** A maior barra mede 91,99185 mm. Não há emenda tracionada em nenhuma barra de alma, e emenda é o ponto onde pontes de palito costumam romper.
3. **Equilíbrio entre economia e ligações.** A variante de 8 painéis e 80 mm gasta 3,5% menos palitos, mas a força máxima sobe 11% (361,98700 N). Com 90 mm as ligações ficam menos solicitadas e a flecha é menor.
4. **Banzos retos.** Cada metade do banzo superior é uma linha reta de 265,70661 mm e o banzo inferior é reto, com 500 mm. Isso permite fazer os banzos contínuos e laminados, sem ligação de banzo em cada nó.

## 4. Geometria adotada

- Vão de 500 mm, 8 painéis de 62,5 mm e altura de 90 mm no centro. O banzo superior vai em linha reta dos apoios até o topo.
- As duas treliças ficam a **80 mm** de distância entre eixos.
- Modelo de cálculo: `projeto/ponte_parker_8x90.json`. É o mesmo arquivo que gera o 3D (`site/ponte-3d.html`), o CAD (`modelos/ponte_parker_8x90.scad`) e o gabarito (`projeto/gabarito_lateral_1-1.svg`).

## 5. Esforços e dimensionamento (uma treliça, P/2 = 220,64962 N)

Reações: 110,32481 N em cada apoio. O equilíbrio fecha com resíduo de 1e-06 N.

| barras | L (mm) | N com carga no centro (N) | N com carga deslocada (N) | camadas | resistência (N) | FS | modo crítico |
|---|---|---|---|---|---|---|---|
| Banzo inferior (b0…b8) | 62.50000 | +306.45781 | +383.07227 | 3 contínuas (2 efetivas) | 1765.68000 | 5.76158 | tração |
| Banzo superior (b0-t1…t7-b8) | 66.42665 | −325.71146 | −407.13932 | 3 contínuas (2 efetivas) | 736.51294 | **2.26124** | flambagem fora do plano |
| Montante central b4-t4 | 90.00000 | +220.64962 | +165.48722 | 3 | 2648.52000 | 12.00328 | tração |
| Diagonais centrais t3-b4, t5-b4 | 91.99185 | 0.00000 | −225.53296 | 3 | 1296.10495 | 5,74685 (carga deslocada) | flambagem |
| Montantes b3-t3, b5-t5 | 67.50000 | 0.00000 | +220.64962 | 3 | 2648.52000 | 12,00328 (carga deslocada) | tração |
| Demais barras de alma | 22.5 a 77.0 | 0.00000 | 0.00000 | 3 | — | — | contraventamento |

Nota: as barras com esforço zero e carga central são indispensáveis. Elas travam os nós do banzo superior contra a flambagem e recebem esforço quando a carga sai do centro. O detalhamento barra a barra está em `projeto/saida_calculo.txt`.

**Conferência à mão (método das seções no apoio):** tan θ = 90/250, então sen θ = 0,33872.
- Banzo superior: N = R / sen θ = 110,32481 / 0,33872 = 325,71 N ✓
- Banzo inferior: N = R / tan θ = 110,32481 × 250 / 90 = 306,46 N ✓
- Montante central: N = P/2 = 220,65 N ✓

**Flambagem do banzo superior (conferência):** I = 8,4 × 4³ / 12 = 44,8 mm⁴, contando só 2 camadas. Então P_cr = π² × 7350 × 44,8 / 66,42665² = 736,51 N, o que dá FS = 2,26 > 2,0 ✓. Com a carga deslocada: 736,51 / 407,14 = 1,81 > 1,5 ✓.

**Resultados globais**
- Barra crítica: banzo superior (flambagem). FS mínimo = **2,26124**.
- Carga de ruptura teórica ≈ **101,75596 kg** (101,75596 = 2,26124 × 45). Na prática deve ficar abaixo disso, por causa das imperfeições, da colagem e da variação dos palitos. Para garantir 45 kg é preciso que o ensaio do lote confirme E e f_c.
- Flecha elástica no meio do vão com 45 kg: **1,97675 mm**.

## 6. Detalhes construtivos

### 6.1 Banzos contínuos (laminados)
- São 3 camadas de palito coladas face a face. As emendas de topo de cada camada ficam desencontradas pelo menos 30 mm umas das outras, de modo que em nenhuma seção haja mais de uma camada emendada.
- Por isso o cálculo considera apenas 2 camadas efetivas.

### 6.2 Ligações das barras de alma
- Todas as barras, inclusive diagonais e montantes, têm **3 camadas (6 mm)**. Assim as chapas das duas faces ficam planas, encostando nos banzos e nas barras ao mesmo tempo.
- Em cada nó e em cada face vai uma peça de chapa sobre o banzo e **duas faixas** de 8,4 mm sobre as pontas das barras.
- Sobreposição necessária: 13,42458 mm. Adotado: 16,80000 mm (2 faixas), FS = 2,50287.
- Nos nós t1 e t7, onde a treliça é baixa, as faixas do nó de baixo cobrem o montante inteiro e servem para os dois nós.

### 6.3 Nó do apoio (encontro dos banzos)
- O banzo superior chega ao inferior num ângulo de 19,79°. Nesse nó, intercale as camadas dos dois banzos: nas camadas 1 e 3 o banzo inferior passa inteiro, e na camada 2 passa o superior. Cubra com chapas nas duas faces.
- Sobreposição mínima: 24,23448 mm para 407,13932 N. **Adote 40 mm.**

### 6.4 Transversina central (onde a carga é pendurada)
- Ela **não pode ficar em cima do banzo inferior**, porque ali passam o montante b4-t4 e as diagonais t3-b4 e t5-b4.
- Fica apoiada em **consolos**: 3 camadas de 30 mm coladas na face interna das chapas do nó b4, de cada treliça, com o topo na altura do topo do banzo.
- Seção: 2 palitos lado a lado × 10 camadas, ou seja 16,8 × 20 mm, com 70 mm de comprimento e 64 mm de vão entre os apoios.
  - Flexão: M = 7060,78800 N·mm, σ = 6,30427 MPa, FS = 6,40835.
  - Cola entre camadas: τ = 0,98504 MPa, FS = 2,03037 **[depende do ensaio da cola]**.
  - Apoio no consolo (compressão normal às fibras): σ = 2,18898 MPa, FS = 4,61401, com f_c90 = 0,25 × f_c0 = 10,1 MPa (NBR 7190).
  - Cola do consolo na chapa: τ = 0,87559 MPa, FS = 2,28416.

### 6.5 Espaçadores provisórios (só palito e cola)
- São dois blocos com 4 camadas de 2 palitos de 74 mm, colados entre si, que mantêm as treliças a 80 mm entre eixos durante a colagem. 74 mm é a distância entre as faces dos banzos inferiores.
- Ficam soltos, sem cola na ponte: um entre os nós b2 e b3, outro entre b5 e b6, fora das chapas. Saem depois que o contraventamento está pronto.
- São feitos de palito para respeitar a regra de usar só palito de picolé e cola branca.

### 6.6 Contraventamento
- Transversinas inferiores (2 camadas, 90 mm) por baixo dos banzos, em todos os nós do banzo inferior menos o central (b4, que tem a transversina central).
- Escoras superiores (2 camadas, 90 mm) por cima dos banzos superiores, ligando os nós t1 a t7 das duas treliças.
- Uma diagonal por painel, alternando a direção (zigue-zague): 8 painéis embaixo e 6 em cima. Cada diagonal fica a 12 mm dos nós para não bater nas transversinas e escoras.
- **Isso é obrigatório:** o cálculo de flambagem fora do plano supõe que cada nó do banzo superior esteja travado lateralmente.

## 7. Quantitativo (do modelo físico, peça por peça)
Gerado por `projeto/gerar_montagem.py`. O plano de corte encaixa as peças em palitos de 101,6 mm úteis.

| item | valor |
|---|---|
| Peças cortadas e coladas (numeradas de 1 a 412, incluindo os 16 espaçadores) | 396 na ponte + 16 espaçadores |
| Palitos usados na ponte | 254 |
| Palitos para os 2 espaçadores provisórios (4 camadas × 2 palitos de 74 mm cada) | 16 |
| Palitos para os ensaios de material | 50 |
| **Palitos a comprar (+15% de perda)** | **368** |
| Área colada (ponte + espaçadores) | 1350,08616 cm² |
| Cola que fica nas juntas (200 g/m²) | 27,00172 g |
| Cola a reservar, com perdas (×3) | 81,00517 g |
| Massa estimada da ponte | 222,53056 g |

A lista de corte completa e o orçamento estão na página de montagem. O consumo de 160 a 200 g/m² e o fato de a cola não aderir a polietileno vêm da ficha técnica da Cascola Cascorez Extra (Henkel).

### Manual de corte (estilo LEGO)
Cada formato de peça tem um código (letra da família + número), e há 37 tipos ao todo. Cada peça tem um número, de 1 a 412, na ordem de montagem. Os moldes em tamanho real, com comprimento, bordas e ângulos de corte, e o índice numerado estão em `projeto/manual/manual_de_corte.pdf`, gerado por `projeto/gerar_manual_pdf.py`. As chapas menores que 80 mm² foram eliminadas do modelo, porque não mudam a resistência e não dá para cortá-las direito.

## 8. Pendências antes de construir
1. **[PENDENTE]** Medir 20 palitos (largura, espessura, comprimento e massa) e atualizar as constantes `B`, `T` e `L_PAL` em `estudo_geometrias.py`.
2. **[PENDENTE]** Ensaiar 10 palitos à tração, 10 pares de palitos à flambagem e 10 juntas coladas ao cisalhamento (skill `propriedades-palito-madeira`). Depois, rodar de novo `calculo_ponte.py`.
3. **[PENDENTE]** Confirmar no regulamento o dispositivo de carga e os limites de largura e altura.
4. Montar sobre o gabarito 1:1 (`projeto/gabarito_lateral_1-1.svg`). Na impressão, a régua do gabarito deve medir 100 mm.
5. Deixar a cola branca curar 24 h, no mínimo, antes de qualquer carga.

## Referências
- ABNT NBR 7190: Projeto de estruturas de madeira (valores de Pinus elliottii).
- USDA Forest Products Laboratory. *Wood Handbook* (FPL-GTR-282), 2021.
- AVILA (2009), ensaio de tração em palitos, citado em [trabalhos de ponte de palito](https://www.studocu.com/pt-br/document/universidade-federal-de-mato-grosso/materiais-de-construcao/projeto-de-ponte-de-palito-calculos-usando-software/6605970). Fonte secundária: precisa ser confirmada pelo ensaio do lote.
- [Unicruz: análise estrutural-experimental em pontes de palito de picolé](https://home.unicruz.edu.br/mercosul/pagina/anais/2018/3%20-Mostra%20de%20Trabalhos%20da%20Gradua%C3%A7%C3%A3o%20e%20P%C3%B3s-Gradua%C3%A7%C3%A3o/Resumos%20Expandidos/AN%C3%81LISE%20ESTRUTURAL%20%E2%80%93%20EXPERIMENTAL%20EM%20PONTES%20DE%20PALITO%20DE%20PICOL%C3%89.pdf)

## 9. Histórico de revisões
- **v2**: a montagem detalhada palito por palito mostrou três problemas da v1, todos registrados no `ERROS.md`:
  1. Diagonais e montantes com 2 camadas (4 mm) e banzos com 3 (6 mm) deixavam as chapas tortas. Agora todas as barras têm 3 camadas.
  2. Uma faixa de chapa só cobria 8,4 mm da ponta das barras, menos que os 13,42 mm calculados. Agora são 2 faixas (16,8 mm).
  3. A transversina central em cima do banzo inferior batia no montante e nas diagonais do nó b4. Agora ela fica sobre consolos.
  - O FS mínimo da ponte não mudou (2,26124, no banzo superior). O peso próprio, 0,22262 kg, equivale a 0,49% da carga e continua desprezado.
