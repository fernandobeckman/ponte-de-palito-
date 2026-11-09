---
name: propriedades-palito-madeira
description: Referência e protocolo para obter propriedades mecânicas de palitos de madeira e colas (E, resistência à tração e compressão, densidade, resistência da colagem). Use antes de qualquer dimensionamento para definir os valores de material.
---

# Propriedades de palitos de madeira

## Regra de ouro
Valores de tabela servem só para pré-dimensionamento. **Ensaie o lote real**: palitos variam de espécie, densidade, umidade e direção das fibras.

## Fontes confiáveis para valores de referência
- USDA Forest Products Laboratory — *Wood Handbook: Wood as an Engineering Material* (FPL-GTR-282, 2021), cap. 5 (tabelas de propriedades por espécie). https://www.fpl.fs.usda.gov/
- ABNT NBR 7190 — Projeto de estruturas de madeira (partes de ensaio de corpos de prova).
- Palitos de picolé costumam ser de bétula (birch) ou álamo/choupo (poplar); palitos de churrasco geralmente bambu. Consulte a espécie correta na tabela antes de usar.

Ordem de grandeza (madeiras leves a médias, seca ao ar, paralelo às fibras): E ≈ 7 000–14 000 MPa; compressão ≈ 25–55 MPa; tração bem maior que compressão. **Confirme na tabela da espécie.**

## Protocolo mínimo de caracterização (lote)
1. Meça 20 palitos com paquímetro (largura, espessura, comprimento) e balança (0,01 g). Calcule média e desvio-padrão.
2. Tração: ≥ 10 corpos de prova pendurando carga gradual até a ruptura.
3. Compressão/flambagem: ≥ 10 corpos de prova curtos (esmagamento) e de comprimento real (flambagem).
4. Colagem: ≥ 10 ligações sobrepostas idênticas às da ponte, ensaiadas ao cisalhamento.
5. Valor característico = média − 1,645·desvio-padrão (quantil de 5%).
6. Registre: marca do palito, cola, tempo de cura, umidade/ambiente, data. Salve em `dados/ensaios-material.csv`.

## Colas
- PVA (cola branca/de madeira): boa para madeira, cura lenta (24 h para resistência total), barata.
- Epóxi: rígido e forte, mais pesado.
- Cianoacrilato: rápido, quebradiço, ruim para cargas de impacto.
Verifique se o regulamento da competição restringe tipo ou quantidade de cola.
