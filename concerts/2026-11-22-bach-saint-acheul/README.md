# Récital Bach — Amiens, 22 novembre 2026

Programme et biographie de Lucien Hennecart pour le récital à l’église Saint-Acheul d’Amiens, le dimanche 22 novembre 2026 à 16 h.

**Ordre du concert :** Suite n° 3 en ut majeur, BWV 1009 ; Suite n° 2 en ré mineur, BWV 1008 ; Suite n° 1 en sol majeur, BWV 1007.

## Contenu
- `BIOGRAPHIE.md` : courte biographie, comprenant Alain Brunier à Rennes et une note sur le violoncelle de Geoffroy Mercier.
- `photo-lucien.jpg` : photographie de Lucien Hennecart au violoncelle (version miniature optimisée pour GitHub).
- `programme_bach_4_pages_A5.tex` : quatre pages du programme, dont une page biographique avec photo.
- `programme_bach_livret_A4.tex` : mise en livret sur feuille A4 paysage recto verso.
- `generer_couverture.py` : construit la couverture à partir de l'affiche publique du récital.

## Compilation

La compilation requiert Python 3 avec Pillow, `pdflatex`, et les extensions LaTeX `ebgaramond`, `pdfpages`, `tikz`, `microtype` et `fancyhdr`.

```sh
python -m pip install Pillow
python generer_couverture.py
pdflatex -interaction=nonstopmode programme_bach_4_pages_A5.tex
pdflatex -interaction=nonstopmode programme_bach_livret_A4.tex
```

Pour l'impression : A4 paysage, recto verso, retournement **sur les bords courts**, échelle 100 %, puis pli central.

La version PDF haute résolution avec la photo originale a été préparée séparément. Le fichier `photo-lucien.jpg` stocké ici est volontairement léger.
