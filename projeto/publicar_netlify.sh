#!/usr/bin/env bash
# Publica a pasta docs/ no site ponte-de-palito.netlify.app (deploy por zip na API da Netlify).
# A chave da Netlify NÃO fica aqui: o proxy da sessão do Claude injeta a credencial salva no ambiente.
set -euo pipefail
SITE_ID="9eb816a3-3b5a-4a4d-b50f-fc9a5954177b"
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
ZIP="$(mktemp -d)/site.zip"
python3 "$RAIZ/projeto/gerar_site.py" >/dev/null
(cd "$RAIZ/docs" && zip -qr "$ZIP" . -x "requisitos.md")
curl -s -X POST -H "Content-Type: application/zip" --data-binary @"$ZIP" \
  "https://api.netlify.com/api/v1/sites/$SITE_ID/deploys" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('state'), d.get('ssl_url'))"
