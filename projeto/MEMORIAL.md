# Memorial de cálculo: Ponte de palito Parker, 8 painéis

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
| Montante central b4-t4 | 90.00000 | +220.64962 | +165.48722 | 2 | 1765.68000 | 8.00219 | tração |
| Diagonais centrais t3-b4, t5-b4 | 91.99185 | 0.00000 | −225.53296 | 2 | ver nota | ≥ 1,5 | flambagem |
| Montantes b3-t3, b5-t5 | 67.50000 | 0.00000 | +220.64962 | 2 | 1765.68000 | — | tração |
| Demais barras de alma | 22.5 a 77.0 | 0.00000 | 0.00000 | 2 | — | — | contraventamento |

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
- Uma chapa de ligação (pedaço de palito) em cada face do nó, colada em diagonais, montantes e banzo.
- Sobreposição mínima calculada: 13,42458 mm. **Adote 20 mm.**

### 6.3 Nó do apoio (encontro dos banzos)
- O banzo superior chega ao inferior num ângulo de 19,79°. Nesse nó, intercale as camadas dos dois banzos (laminação cruzada) e cubra com chapas nas duas faces.
- Sobreposição mínima: 24,23448 mm para 407,13932 N. **Adote 40 mm.**

### 6.4 Transversina central (onde a carga é pendurada)
- Vão de 80 mm entre as treliças. Momento M = P·L/4 = 8825,98500 N·mm.
- Seção: 2 palitos lado a lado × 10 camadas deitadas, ou seja 16,8 × 20 mm.
  - σ = 7,88034 MPa, FS = 5,12668
  - τ na cola = 0,98504 MPa, FS = 2,03037 **[depende do ensaio da cola]**
- Apoie a transversina **sobre** o banzo inferior, no nó b4, e não apenas colada na lateral. Assim a carga passa por contato direto, e não por cisalhamento na cola.

### 6.5 Contraventamento
- Transversinas inferiores em todos os nós b1 a b7.
- Escoras superiores ligando os nós t1 a t7 das duas treliças.
- Diagonais em X nos planos superior e inferior.
- **Isso é obrigatório:** o cálculo de flambagem fora do plano supõe que cada nó do banzo superior esteja travado lateralmente.

## 7. Quantitativo
| item | palitos |
|---|---|
| Banzos (2 treliças) | 62 |
| Alma (2 treliças) | 52 |
| Chapas de ligação | 64 |
| Transversinas (inclui a central) | 36 |
| Escoras superiores | 14 |
| Contraventamento | 32 |
| **Total** | **≈ 260 (compre ≈ 312, com 20% de perda)** |

Massa estimada: 309,42912 g (madeira mais 15% de cola). O peso próprio corresponde a 0,69% da carga (0,30943 kg ÷ 45 kg) e foi desprezado.

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
