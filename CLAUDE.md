# Projeto: Ponte de Palito

Projeto de engenharia: concepção, cálculo, modelagem 3D, construção, ensaio e site de uma ponte de palitos de madeira.

## Regras para o Claude
1. **Leia `ERROS.md` e `docs/requisitos.md` antes de qualquer tarefa** e não repita os erros listados. Ao errar, registre o erro lá (skill `registro-de-erros`).
2. Responda em português do Brasil. Use unidades SI (mm, N, MPa, g).
3. Cálculos estruturais saem das skills `analise-trelica` e `flambagem-euler`, nunca de conta de cabeça. Confira sempre o equilíbrio e uma barra à mão.
4. Valores de material precisam ter origem (ensaio ou fonte citada). Dado que não existe fica como [PENDENTE].
5. O mesmo JSON de nós e barras alimenta o cálculo, o CAD (`openscad-ponte`) e o 3D web (`ponte-3d-threejs`).
6. Antes de copiar skills ou agentes de terceiros, confira a licença e procure scripts suspeitos.

## Onde está cada coisa
- `.claude/agents/`: 83 subagentes (catálogo em `.claude/CATALOGO.md`)
- `.claude/skills/`: 76 skills
- `.claude/licencas/`: licenças das fontes de terceiros
- `ERROS.md`: registro de erros e de como evitá-los

## Fluxo sugerido
`regras-competicao-ponte-palito` → `projetista-de-pontes` → `analise-trelica` → `dimensionamento-barras-palito` → `revisor-seguranca-estrutural` → `ponte-3d-threejs` / `openscad-ponte` → `planejador-construcao` → `ensaio-de-carga` → `relatorio-tecnico-engenharia`
