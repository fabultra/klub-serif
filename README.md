# Klub Serif

Famille typographique du **K.lub** — quatre styles de qualité fonderie,
fidèles au logotype.

![Specimen Klub Serif](docs/planche.png)

## Styles

| Fichier | Usage |
| --- | --- |
| `KlubSerifDisplay-Regular` | Titres, logotype, affichage |
| `KlubSerifDisplay-Italic` | Emphase en affichage |
| `KlubSerifText-Regular` | Paragraphes, menus, petits corps |
| `KlubSerifText-Italic` | Emphase en texte courant |

Couverture : latin étendu, accents français complets (à â ç é è ê ë î ï ô ù û ü œ æ),
chiffres, ponctuation. Espacement et crénage d'origine professionnelle.

## Installation (print / bureautique)

Télécharger les `.ttf` dans [`fonts/ttf/`](fonts/ttf/), double-clic → « Installer ».

## Web (auto-hébergement recommandé)

Copier les `.woff2` de [`fonts/web/`](fonts/web/) sur le site, puis :

```css
@font-face {
  font-family: "Klub Serif Display";
  src: url("/fonts/KlubSerifDisplay-Regular.woff2") format("woff2");
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}
@font-face {
  font-family: "Klub Serif Text";
  src: url("/fonts/KlubSerifText-Regular.woff2") format("woff2");
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

h1, h2, .logo { font-family: "Klub Serif Display", serif; }
body          { font-family: "Klub Serif Text", serif; }
```

Chaque style pèse ~30 Ko en WOFF2. Alternative sans hébergement : les
mêmes dessins existent sur Google Fonts sous les noms *DM Serif Display*
et *DM Serif Text* (voir provenance ci-dessous).

## Provenance et licence

Klub Serif est une **adaptation renommée** de *DM Serif Display* et
*DM Serif Text* (Colophon Foundry pour Google), elles-mêmes dérivées de
*Source Serif* (Adobe). Aucune modification de dessin dans cette version ;
seuls les noms de famille ont été adaptés à la marque.

L'ensemble est sous licence **SIL Open Font License 1.1** — voir
[`LICENSES/`](LICENSES/). En résumé :

- usage commercial, modification et redistribution autorisés ;
- conserver les fichiers de licence en cas de redistribution des fontes ;
- ne pas vendre les fichiers de fonte seuls ;
- le nom réservé « Source » n'est pas utilisé.

## Outils

[`tools/rebrand.py`](tools/rebrand.py) — script fontTools qui régénère la
famille depuis les fontes DM d'origine (renommage conforme OFL, export
TTF + WOFF2). Reproductible : `pip install fonttools brotli` puis
`python3 rebrand.py` à côté d'un dossier `base/` contenant les DM Serif.

## Feuille de route

- [x] Famille 4 styles (Display/Text × romain/italique)
- [ ] Glyphes signature K.lub (g à un étage, ligature « k.l » du logotype)
- [ ] Graisse supplémentaire si besoin (via l'ascendance Source Serif)
