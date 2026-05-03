# Projet : Analyse de la Qualité de l'Air à Douala (Cameroun)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-blue?logo=pandas)](https://pandas.pydata.org/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3%2B-orange?logo=scikitlearn)](https://scikit-learn.org/)
[![Statsmodels](https://img.shields.io/badge/Statsmodels-0.14%2B-blue)](https://www.statsmodels.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Terminé-brightgreen)]()

---

##  Contexte

Douala, capitale économique du Cameroun, connaît une croissance urbaine rapide et une activité industrielle intense. Cette situation génère une pollution atmosphérique qui impacte la santé des populations. Des capteurs mesurent en continu plusieurs polluants (PM2.5, PM10, NO₂, O₃, CO) ainsi que des variables météorologiques (température, humidité, vitesse du vent).

L'objectif de ce projet est de construire un **pipeline d'analyse complet** pour :
- Comprendre les **patterns temporels** de la pollution,
- Identifier les **périodes et zones** les plus critiques,
- **Prédire les pics de pollution** à partir des conditions météorologiques,
- Proposer des **recommandations** aux autorités locales.

---

##  Questions à traiter

1. **Q1** : Quels polluants sont les plus élevés et à quelles heures de la journée ?
2. **Q2** : Existe-t-il une **saisonnalité** dans les niveaux de pollution ?
3. **Q3** : Peut-on **prédire** un pic de pollution à partir des conditions météorologiques ?
4. **Q4** : Quels quartiers ou zones sont les plus exposés ?

---

##  Données

## Sources envisagées
- **OpenAQ API** (données réelles) : [openaq.org](https://openaq.org/)
- **WHO Air Quality Database** : données historiques mondiales
- **Génération synthétique** (faute de données locales suffisantes)

Pour ce projet, nous utilisons un **jeu de données synthétique réaliste** généré avec `numpy` et `pandas`, respectant les tendances saisonnières et journalières observées à Douala (saison sèche plus polluée, heures de pointe matin/soir, corrélations entre polluants). Le fichier généré est `douala_air_quality.csv` (8 784 enregistrements horaires sur l'année 2024).

---

##  Outils utilisés

| Bibliothèque / Outil | Rôle |
|---------------------|------|
| `pandas`, `numpy` | Manipulation et calcul numérique |
| `matplotlib`, `seaborn` | Visualisations |
| `scikit-learn` | Standardisation, ACP, clustering K‑Means, Random Forest |
| `statsmodels` | Décomposition temporelle, test ADF, modèles SARIMA |
| `pmdarima` (optionnel) | Recherche automatique des paramètres SARIMA |

---

##  Pipeline d’analyse (étapes détaillées)

### 1. Chargement et exploration (EDA)
- Chargement du CSV avec `pandas`.
- Statistiques descriptives (moyenne, écart-type, quartiles).
- Histogrammes des polluants pour visualiser les distributions.
- Matrice de corrélation entre polluants et variables météo.
- Série temporelle brute des PM2.5.

### 2. Prétraitement
- **Gestion des valeurs manquantes** : interpolation linéaire (car données horaires).
- **Standardisation** (centrage réduction) pour l’ACP.
- **Création de variables temporelles** : heure, jour de la semaine, mois, jour de l’année.

### 3. Décomposition temporelle (focus sur PM2.5)
- Agrégation en moyenne journalière.
- Décomposition additive (`seasonal_decompose`) avec période hebdomadaire (7 jours).
- Extraction de la tendance, de la composante saisonnière et des résidus.
- **Test de Dickey-Fuller augmenté (ADF)** pour vérifier la stationnarité.

### 4. Analyse en Composantes Principales (ACP)
- Application sur les 5 polluants standardisés.
- Visualisation de la variance expliquée par composante.
- **Cercle des corrélations** : projection des variables sur les deux premières composantes principales pour interpréter les relations entre polluants.

### 5. Clustering K‑Means (profils journaliers)
- Agrégation des polluants par jour.
- Détermination du nombre optimal de clusters (méthode du coude).
- Choix de 3 clusters correspondant à des profils : **bon**, **moyen**, **critique**.
- Visualisation des séries temporelles des PM2.5 pour chaque cluster.

### 6. Classification Random Forest (prédiction du pic)
- Création de la variable cible : `1` si PM2.5 > 75 µg/m³ (jour critique), `0` sinon.
- Variables explicatives : température, humidité, vent, heure, jour de la semaine, mois.
- Division train/test temporelle (80%/20%).
- Entraînement d’un **Random Forest**.
- Évaluation : rapport de classification, matrice de confusion, importance des caractéristiques.

### 7. Prévision SARIMA
- Sélection du polluant principal (PM2.5) en moyenne journalière.
- Utilisation de `auto_arima` (ou paramètres fixes) pour choisir les ordres `(p,d,q)` et `(P,D,Q,s)` avec `s=7` (période hebdomadaire).
- Ajustement du modèle SARIMA.
- **Prévision à 30 jours** avec intervalles de confiance.
- Graphique combinant historique et prévision.

### 8. Livrables spécifiques
- **Carte de chaleur hebdomadaire** : moyenne des PM2.5 par heure et jour de la semaine (heatmap).
- **Graphique de décomposition SARIMA** avec prévision 30 jours.
- **Tableau de bord** : indicateurs clés (moyenne, maximum, 95e percentile, nombre de jours critiques) et recommandations.

### 9. Réponses aux questions
- Intégration dans le code des analyses répondant explicitement à **Q1, Q2, Q3, Q4**.

---

##  Résultats attendus

| Question | Réponse résumée |
|----------|----------------|
| **Q1** | Les heures de pointe sont 7‑9h et 18‑20h. Le PM2.5 et le CO sont les plus élevés. |
| **Q2** | Oui – maximum en janvier (saison sèche), minimum en juillet (saison humide). |
| **Q3** | Oui – Random Forest atteint une précision > 80%. Les variables les plus importantes sont la température et l’humidité. |
| **Q4** | Zone industrielle (ex: Bonapriso) plus exposée que les zones résidentielles (ex: Akwa). |

---

##  Exécution du projet

### Prérequis
```bash
pip install pandas numpy matplotlib seaborn scikit-learn statsmodels pmdarima
```

### Fichiers
- `generate_douala_data.py` : génère le jeu de données synthétique.
- `douala_air_quality.csv` : données d’entrée.
- `pipeline_analyse.py` ou notebook `analyse_qualite_air.ipynb` : code complet du pipeline.

### Lancer l’analyse
```bash
python generate_douala_data.py   # une seule fois
python pipeline_analyse.py
```

Ou ouvrez le notebook Jupyter et exécutez les cellules séquentiellement.

---

##  Structure du dépôt

```
air-quality-douala/
├── README.md
├── analyse.ipynb
├── douala_air_quality.csv
```

---

##  Aperçu des visualisations

### Carte de chaleur hebdomadaire
![Heatmap](figures/heatmap_hour_day.png)

### Cercle des corrélations (ACP)
![PCA](figures/pca_circle.png)

### Prévision SARIMA 30 jours
![SARIMA](figures/sarima_forecast.png)

*(Les images sont générées automatiquement lors de l’exécution)*

---

##  Recommandations finales

- **Renforcer la surveillance** aux heures de pointe (7‑9h, 18‑20h).
- **Mettre en place des jours sans voiture** pendant la saison sèche (janvier-février).
- **Développer un système d’alerte** basé sur les prévisions SARIMA (sms, radio).
- **Étendre le réseau de capteurs** aux zones industrielles et aux axes routiers denses.
