"""
Projet BEST (TN09) - Analyse des correlations entre indicateurs de bien-etre.

Ce script reproduit l'analyse menee pendant le stage a partir de l'OECD Better
Life Index : mise en forme des donnees (une ligne par pays, une colonne par
indicateur), calcul de la matrice de correlation et production des cartes
thermiques.

Les figures produites sont enregistrees dans figures/.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # execution sans interface graphique (script / CI)

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "OECD_BLI_all.csv"
FIG_DIR = BASE_DIR / "figures"

# Regroupement des pays du jeu de donnees OCDE en deux ensembles.
# (Une premiere version decoupait par continent ; le decoupage par niveau de
# revenu s'est revele plus discriminant pour la lecture des correlations.)
REGIONS = {
    "high-income": [
        "Australia", "Austria", "Belgium", "Canada", "Costa Rica", "Denmark",
        "Estonia", "Finland", "France", "Germany", "Iceland", "Ireland",
        "Israel", "Italy", "Japan", "Korea", "Latvia", "Lithuania",
        "Luxembourg", "Netherlands", "New Zealand", "Norway", "OECD - Total",
        "Poland", "Portugal", "Slovenia", "Spain", "Sweden", "Switzerland",
        "United Kingdom", "United States",
    ],
    "middle-income": [
        "Brazil", "Chile", "Colombia", "Czechia", "Mexico", "Russia",
        "Slovak Republic", "Turkey", "South Africa",
    ],
}

# Palette adaptee aux daltoniens (Color Universal Design).
CB_PALETTE = [
    "#999999", "#E69F00", "#56B4E9", "#009E73",
    "#F0E442", "#0072B2", "#D55E00", "#CC79A7",
]


def load_data(path=DATA_PATH):
    """Lit le CSV OCDE en testant plusieurs encodages."""
    for encoding in ("utf-8", "latin1", "gbk"):
        try:
            data = pd.read_csv(path, encoding=encoding)
            print(f"Fichier lu avec l'encodage : {encoding}")
            return data
        except UnicodeDecodeError:
            print(f"Encodage non valide : {encoding}")
    raise UnicodeDecodeError(
        "utf-8", b"", 0, 1, f"Aucun encodage supporte pour {path}"
    )


def build_indicator_table(data):
    """Pivote le format long OCDE en une ligne par pays / une colonne par indicateur."""
    filtered = data[["Country", "Indicator", "OBS_VALUE"]]
    table = filtered.pivot_table(
        index="Country", columns="Indicator", values="OBS_VALUE"
    )
    # Les valeurs manquantes sont remplacees par 0, comme dans l'analyse
    # d'origine. Limite connue : cela fausse legerement les correlations pour
    # les pays incomplets (cf. note methodologique dans le README).
    table = table.fillna(0)
    return table


def plot_heatmap(table, title, outfile):
    """Trace et enregistre une carte thermique des correlations."""
    correlation = table.corr()

    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation, annot=True, fmt=".2f", cmap="coolwarm")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(outfile, dpi=150)
    plt.close()
    print(f"Figure enregistree : {outfile.name}")
    return correlation


def top_correlations(correlation, n=5):
    """Retourne les n paires d'indicateurs les plus correlees (hors diagonale)."""
    pairs = correlation.stack().reset_index()
    pairs.columns = ["indicateur_1", "indicateur_2", "r"]
    # Chaque paire apparait deux fois (A-B et B-A) : on n'en garde qu'une.
    pairs = pairs[pairs["indicateur_1"] < pairs["indicateur_2"]]
    pairs["abs_r"] = pairs["r"].abs()
    return pairs.sort_values("abs_r", ascending=False).head(n)[
        ["indicateur_1", "indicateur_2", "r"]
    ]


def main():
    sns.set_palette(CB_PALETTE)
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    data = load_data()
    table = build_indicator_table(data)
    print(f"{table.shape[0]} pays x {table.shape[1]} indicateurs")

    correlation = plot_heatmap(
        table,
        "Correlation Heatmap of Indicators",
        FIG_DIR / "heatmap-tous-pays.png",
    )

    print("\nCorrelations les plus fortes (tous pays) :")
    print(top_correlations(correlation).to_string(index=False))

    country_to_region = {
        country: region
        for region, countries in REGIONS.items()
        for country in countries
    }
    table = table.assign(Region=table.index.map(country_to_region))

    for region in REGIONS:
        subset = table[table["Region"] == region].drop(columns="Region")
        plot_heatmap(
            subset,
            f"Correlation Heatmap of Indicators - {region}",
            FIG_DIR / f"heatmap-{region}.png",
        )


if __name__ == "__main__":
    main()
