#!/usr/bin/env bash
# ============================================================
# Klub Serif — installateur pour site web
# ------------------------------------------------------------
# Telecharge les fontes web (woff2) et la feuille de style
# prete a l'emploi dans un dossier de votre projet.
#
# Usage :
#   ./install.sh                 -> installe dans ./fonts
#   ./install.sh public/fonts    -> installe dans public/fonts
#
# Ou sans cloner le repo, depuis n'importe quel projet :
#   curl -fsSL https://raw.githubusercontent.com/fabultra/klub-serif/main/install.sh | bash
# ============================================================
set -euo pipefail

DEST="${1:-./fonts}"
BASE="${KLUB_BASE:-https://raw.githubusercontent.com/fabultra/klub-serif/main/fonts/web}"
FILES="klub-serif.css
KlubSerifDisplay-Regular.woff2
KlubSerifDisplay-Italic.woff2
KlubSerifText-Regular.woff2
KlubSerifText-Italic.woff2"

echo "Installation de Klub Serif dans $DEST ..."
mkdir -p "$DEST"

# Si le script est lance depuis un clone du repo, copie locale ;
# sinon telechargement.
SRC_LOCAL="$(cd "$(dirname "$0")" 2>/dev/null && pwd)/fonts/web"
for f in $FILES; do
  if [ -f "$SRC_LOCAL/$f" ]; then
    cp "$SRC_LOCAL/$f" "$DEST/$f"
    echo "  copie   -> $DEST/$f"
  else
    curl -fsSL "$BASE/$f" -o "$DEST/$f"
    echo "  reseau  -> $DEST/$f"
  fi
done

WEBPATH="/${DEST#./}"
cat <<FIN

Klub Serif est installee. Deux lignes a ajouter dans le <head> :

  <link rel="stylesheet" href="$WEBPATH/klub-serif.css">
  <link rel="preload" href="$WEBPATH/KlubSerifDisplay-Regular.woff2" as="font" type="font/woff2" crossorigin>

Puis dans votre CSS :

  h1, h2, .logo { font-family: "Klub Serif Display", Georgia, serif; }
  body          { font-family: "Klub Serif Text", Georgia, serif; }

Rappels : la ligature « k.lub » est automatique ; g classique via
font-feature-settings: "ss01" 1;  Licence : SIL OFL 1.1 (dossier LICENSES).
FIN
