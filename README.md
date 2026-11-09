# ponte-de-palito-

Projeto de engenharia de uma ponte de palitos de madeira: cálculo da treliça, modelagem 3D, construção, ensaio de carga e site do projeto.

## Ferramentas para o Claude Code
- **83 agentes** em `.claude/agents/` e **76 skills** em `.claude/skills/`. A lista completa e as fontes estão em [`.claude/CATALOGO.md`](.claude/CATALOGO.md).
- Regras do projeto para o Claude: [`CLAUDE.md`](CLAUDE.md)
- Registro de erros (ler antes de cada tarefa): [`ERROS.md`](ERROS.md)

## Começo rápido
```bash
python3 .claude/skills/analise-trelica/scripts/trelica.py .claude/skills/analise-trelica/exemplos/pratt_6paineis.json
python3 .claude/skills/flambagem-euler/scripts/flambagem.py --b 9.5 --h 2 --n 3 --L 100 --N 1500
python3 .claude/skills/ponte-3d-threejs/scripts/gerar_visualizacao.py .claude/skills/analise-trelica/exemplos/pratt_6paineis.json ponte-3d.html
```
