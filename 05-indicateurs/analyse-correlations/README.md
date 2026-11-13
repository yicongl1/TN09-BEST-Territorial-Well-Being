# Analyse des corrélations entre indicateurs de bien-être

Exploration statistique des **11 dimensions du Better Life Index de l'OCDE**, réalisée
pendant le stage pour vérifier la cohérence des indicateurs retenus dans le projet BEST
et repérer les interdépendances à intégrer dans le modèle territorial.

## Contenu

| Fichier | Description |
| --- | --- |
| `analyse_correlations.py` | Script autonome : lecture, mise en forme, corrélations, cartes thermiques |
| `notebook/analyse-correlations.ipynb` | Notebook d'origine (Colab), chemins convertis en relatif |
| `data/OECD_BLI_all.csv` | Jeu de données source — [OECD Better Life Index](https://www.oecdbetterlifeindex.org/) (format long) |
| `figures/` | Cartes thermiques exportées (tous pays, hauts revenus, revenus intermédiaires) |

## Démarche

1. **Lecture** du fichier OCDE au format long (`Country`, `Indicator`, `OBS_VALUE`).
2. **Pivot** : une ligne par pays, une colonne par indicateur.
3. **Matrice de corrélation** de Pearson sur les 22 indicateurs.
4. **Visualisation** en carte thermique (`seaborn.heatmap`, palette `coolwarm`).
5. **Comparaison** de deux sous-ensembles de pays (hauts revenus / revenus intermédiaires).

## Résultats principaux

- **Espérance de vie ↔ logements sans équipements de base : r ≈ −0,85** — les logements
  dépourvus d'installations sanitaires dégradent l'hygiène et donc l'état sanitaire.
- **Revenus personnels ↔ satisfaction de vie : r ≈ +0,80** — le bien-être perçu est
  fortement lié à la stabilité financière.
- **Taux de chômage ↔ niveau de compétences : r ≈ −0,68** — relation entre qualification
  et employabilité.
- Résultats contre-intuitifs conservés tels quels : la qualité de l'eau ressort très
  corrélée au taux d'emploi et à la satisfaction de vie (probable effet de structure
  des pays de l'échantillon, à approfondir).

## Exécution

```bash
pip install -r requirements.txt
python analyse_correlations.py
```

Les figures sont régénérées dans `figures/`.

## Limites méthodologiques

- Les valeurs manquantes sont remplacées par `0` (choix de l'analyse d'origine) : cela
  peut surestimer ou sous-estimer certaines corrélations pour les pays incomplets.
- Corrélation de Pearson uniquement : pas de test de significativité ni de contrôle des
  variables confondantes ; l'objectif était exploratoire, pas inférentiel.
- Les pays sont regroupés par niveau de revenu, un découpage grossier qui masque les
  trajectoires nationales.
