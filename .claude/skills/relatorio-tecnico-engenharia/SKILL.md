---
name: relatorio-tecnico-engenharia
description: Modelo e regras para escrever relatório técnico / memorial de cálculo de engenharia em português no padrão ABNT (NBR 14724, NBR 6023, NBR 10520). Use para relatórios da ponte de palito, memoriais de cálculo e documentação do projeto.
---

# Relatório técnico de engenharia

## Estrutura (NBR 14724)
1. Capa e folha de rosto
2. Resumo (150–500 palavras) e palavras-chave
3. Introdução: objetivo, regras da competição, requisitos
4. Fundamentação teórica: treliças, método dos nós/rigidez, flambagem de Euler, propriedades da madeira
5. Materiais e métodos: palitos, cola, ensaios de material, ferramentas de cálculo (cite os scripts do repositório)
6. Memorial de cálculo: geometria, carregamento, esforços (tabela), dimensionamento (tabela), massa prevista
7. Construção: etapas, fotos, massa final
8. Ensaio: protocolo, curva carga × deslocamento, carga de ruptura, modo de falha
9. Discussão: previsto × medido, causas das diferenças, lições aprendidas
10. Conclusão
11. Referências (NBR 6023)

## Regras
- Figuras e tabelas numeradas, com título e fonte; todas citadas no texto.
- Unidades SI, vírgula decimal no texto em português.
- Dados ausentes ficam como **[PENDENTE]** — nunca invente resultados.
- Para gerar .docx ou .pdf use as skills `docx` / `pdf`.
