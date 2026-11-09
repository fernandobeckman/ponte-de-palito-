---
name: openscad-ponte
description: Gera modelo 3D paramétrico da ponte em OpenSCAD a partir do JSON de nós e barras da skill analise-trelica, para visualizar, exportar STL (impressão 3D de gabaritos/maquete) ou desenhos. Use quando precisar de modelo CAD da ponte.
---

# Modelo OpenSCAD da ponte

```bash
python3 .claude/skills/openscad-ponte/scripts/json2scad.py .claude/skills/analise-trelica/exemplos/pratt_6paineis.json modelos/ponte.scad --largura 80
openscad -o modelos/ponte.stl modelos/ponte.scad   # se o OpenSCAD estiver instalado
```

- Uma única fonte da verdade: o mesmo JSON do cálculo gera o CAD.
- Treliça 2D vira duas treliças laterais + transversinas nos nós (contraventamento real deve ser adicionado no JSON 3D).
- Verifique `which openscad` antes; sem ele, use a skill `ponte-3d-threejs` para visualizar no navegador.
- Referência da linguagem: https://openscad.org/documentation.html
