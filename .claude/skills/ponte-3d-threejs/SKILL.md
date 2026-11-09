---
name: ponte-3d-threejs
description: Gera uma página HTML interativa com o modelo 3D da ponte em Three.js, com barras coloridas por esforço (tração azul, compressão vermelho) e clique para ver o valor. Use para revisar a geometria, apresentar o projeto ou montar o site da ponte.
---

# Visualização 3D da ponte (Three.js)

```bash
python3 .claude/skills/ponte-3d-threejs/scripts/gerar_visualizacao.py .claude/skills/analise-trelica/exemplos/pratt_6paineis.json site/ponte-3d.html --largura 80
```

- Usa o solver da skill `analise-trelica` — os esforços na tela são os mesmos do memorial.
- Three.js 0.160.0 fixado via importmap (unpkg). Para trabalhar offline, baixe a mesma versão e troque os caminhos.
- Abra com um servidor local (`python3 -m http.server`) — módulos ES não carregam via `file://` em alguns navegadores.
- Para recursos avançados (sombras, pós-processamento, IFC) consulte as skills `threejs-*` instaladas.
