# Projet SmartMarket - Analyse des Ventes

## Bienvenue

Ce projet vous aide à analyser les données de vente de SmartMarket. Nous avons créé un système de Data Warehouse (entrepôt de données) qui organise toutes vos informations de manière claire et facile à exploiter.

**Objectif** : Répondre aux 20 questions clés de votre cahier des charges pour améliorer vos ventes, comprendre vos clients et optimiser vos opérations.

---

## Structure du Projet

```
Data-Anaytic/
├── data/              # Vos données
│   ├── SmartMarket_raw.xlsx        (fichier original)
│   ├── SmartMarket_cleaned.xlsx    (données nettoyées)
│   └── Cas_Etude_SmartMarket_VF_F.pdf  (cahier des charges)
│
├── scripts/          # Outils automatiques
│   ├── analyze_excel.py            (analyser vos données)
│   └── clean_data.py               (nettoyer automatiquement)
│
├── docs/             # Documentation
│   ├── MAPPING_COLONNES_REEL.md    (guide des colonnes Excel)
│   └── RESUME_COMPLET.md           (référence complète)
│
├── latex/            # Documents techniques
│   ├── SmartMarket_Modele_Etoile.tex
│   └── TABLE_LATEX_MAPPING.tex
│
└── README.md            # Ce guide
```

---

## Comment Utiliser Ce Projet

### Etape 1 : Voir ce qui est dans vos données
```bash
cd scripts
python3 analyze_excel.py
```
Cela vous montre toutes les colonnes de votre fichier Excel, les types de données, et les éventuels problèmes.

### Etape 2 : Nettoyer automatiquement vos données
```bash
python3 clean_data.py
```
Un nouveau fichier `data/SmartMarket_cleaned.xlsx` sera créé avec toutes les corrections appliquées.

### Etape 3 : Consulter les guides
```bash
# Pour comprendre vos colonnes
cat docs/MAPPING_COLONNES_REEL.md

# Pour un résumé complet
cat docs/RESUME_COMPLET.md
```

---

## Ce Qui a Ete Nettoye Dans Vos Donnees

### Problemes corriges automatiquement

| Problème | Avant | Après | Impact |
|----------|-------|-------|--------|
| **Remise_%** | -10% à 150% | 0% à 100% | Corrige |
| **Canal_Vente** | 'En ligne'/'en ligne' | 'En Ligne' | Standardise |
| **Score** | Texte + numérique | Numérique 1-5 | Normalise |
| **Pays** | 'cn', 'CHN', 'France', 'FR' | 'CHN', 'FRA' | Standardise |
| **Fiabilite_%** | 120% | 100% | Corrige |
| **Dates** | 99 formats | Format ISO | Standardise |

### Vos Donnees en Un Coup d'Oeil

#### Vos Ventes (100 transactions)
- **Quand ?** De février 2020 à décembre 2024
- **Combien ?** 143,400 € de chiffre d'affaires total
- **Qui ?** 42 clients différents
- **Quoi ?** 30 produits différents vendus
- **Remise moyenne** que vous accordez : 27.73%
- **Panier moyen** par achat : 1,687 €

#### Satisfaction de Vos Clients (60 avis)
- **Note moyenne** : 3.22 étoiles sur 5
- **Taux de réponse** : 82% (49 avis complets sur 60)

#### Vos Fournisseurs (10 partenaires)
- **Fiabilité moyenne** : 92.22% (plutôt bon !)
- **Délai de livraison moyen** : 6.6 jours
- **Note générale** : 2.33/5 (il y a de la marge d'amélioration)

---

## Comment Sont Organisees Vos Donnees (Modele en Etoile)

### Schema Simplifie

Imaginez une étoile : au centre, vos VENTES. Autour, toutes les informations liées :

```
         DIM_TEMPS
              │
              │
DIM_CLIENT ─────── FAIT_VENTES ─────── DIM_PRODUIT
              │
              │
         DIM_CANAL
              │
              │
         DIM_REGION
              │
              │
      DIM_FOURNISSEUR
```

### Ce Que Nous Avons

#### Completement Pret
- **TEMPS** - Dates, mois, années, trimestres... (calendrier complet)
- **CANAUX** - Vos 3 moyens de vendre : En ligne, Boutique, Téléphone
- **FOURNISSEURS** - Les 10 entreprises qui vous livrent
- **VENTES** - Toutes vos transactions avec les montants, remises, etc.

#### Incomplet (Besoin de Plus d'Info)
- **CLIENTS** - On a les numéros, mais il manque : noms, emails, villes
- **PRODUITS** - On a les codes, mais il manque : noms, catégories, prix catalogue
- **RÉGIONS** - Impossible à créer sans les villes des clients

---

## Les 20 Questions de Votre Cahier des Charges

### Ce Qu'On Peut Faire Tout de Suite

| # | Objectif | Statut | Fichier |
|---|----------|--------|---------|
| 1 | CA par année et canal | OK | Transactions |
| 2 | Top 10 produits vendus | Partiel | Transactions (sans nom produit) |
| 3 | Taux remise moyen par catégorie | Non | Manque catégories |
| 5 | Transactions incohérentes | OK | Transactions |
| 6 | Nettoyer infos clients | Partiel | Données manquantes |
| 7 | Standardiser catégories/prix | OK | Fait |
| 8 | Corriger remises hors plage | OK | Fait |
| 9 | Revenu réel par transaction | OK | Transactions |
| 13 | Fiabilité fournisseurs | OK | Fournisseurs |
| 14 | % livraisons en retard | OK | Transactions |
| 15 | Comparer ventes par canal | OK | Transactions |

### Realisables avec enrichissement

| # | Objectif | Manque | Action requise |
|---|----------|--------|----------------|
| 4 | Performance par région | Ville clients | Créer feuille Clients |
| 10 | Clients inactifs > 12 mois | Date inscription | Créer feuille Clients |
| 11 | Satisfaction par ville/année | Ville clients | Créer feuille Clients |
| 12 | Produits satisfaction basse | Nom produits | Créer feuille Produits |
| 16 | Corrélation remise-satisfaction | Jointure | Lier Satisfaction↔Transactions |
| 17 | Panier moyen par client | Détails clients | Créer feuille Clients |
| 18 | Segmentation RFM clients | Données complètes | Créer feuille Clients |

---

## Colonnes Dans Excel

### Feuille: Transactions
```
Transaction_ID, Date, Client_ID, Produit_ID, Quantite,
Remise_%, Canal_Vente, Mode_Paiement, Statut_Livraison,
Date_Livraison, Revenu_Total
```

### Feuille: Satisfaction
```
Client_ID, Date_Enquete, Score, Commentaire
```

### Feuille: Fournisseurs
```
Fournisseur_ID, Nom_Fournisseur, Pays, Evaluation,
Delai_Moyen_Livraison, Fiabilite_%
```

---

## Donnees Manquantes

### Feuille "Clients" à créer (42 lignes)
```
- ID_Client (déjà dans Transactions)
- Nom_Client
- Prenom_Client
- Email
- Telephone
- Ville
- Code_Postal
- Date_Inscription
```

### Feuille "Produits" à créer (30 lignes)
```
- ID_Produit (déjà dans Transactions)
- Nom_Produit
- Categorie
- Sous_Categorie
- Prix_Catalogue
- Marque
```

### Lien manquant
```
- Fournisseur_ID dans Transactions
  (Quel fournisseur pour chaque transaction?)
```

---

## Prochaines Etapes

### Phase 1: Enrichissement des donnees (URGENT)
```bash
1. Créer feuille "Clients" dans Excel
   - Exporter les IDs: python3 export_client_ids.py
   - Remplir manuellement les détails
   
2. Créer feuille "Produits" dans Excel
   - Exporter les IDs: python3 export_product_ids.py
   - Remplir manuellement les détails
   
3. Ajouter colonne Fournisseur_ID dans Transactions
```

### Phase 2: Créer le Data Warehouse
```sql
-- Créer la base de données
CREATE DATABASE smartmarket_dw;

-- Exécuter les scripts SQL
source create_tables.sql
source load_dimensions.sql
source load_facts.sql
```

### Phase 3: Analyses et dashboards
```bash
# Power BI / Tableau / Python
- Importer depuis smartmarket_dw
- Créer les 20 analyses
- Publier les dashboards
```

---

## REQUÊTES SQL PRÊTES À L'EMPLOI

### Top 10 produits les plus vendus
```sql
SELECT 
    p.Nom_Produit,
    SUM(v.Quantite) AS Total_Vendus,
    SUM(v.Revenu_Reel) AS CA_Total
FROM FAIT_VENTES v
JOIN DIM_PRODUIT p ON v.ID_Produit = p.ID_Produit
GROUP BY p.Nom_Produit
ORDER BY Total_Vendus DESC
LIMIT 10;
```

### CA par canal et année
```sql
SELECT 
    t.Annee,
    c.Nom_Canal,
    SUM(v.Revenu_Reel) AS CA_Total,
    COUNT(*) AS Nb_Transactions
FROM FAIT_VENTES v
JOIN DIM_TEMPS t ON v.ID_Date = t.ID_Date
JOIN DIM_CANAL c ON v.ID_Canal = c.ID_Canal
GROUP BY t.Annee, c.Nom_Canal
ORDER BY t.Annee, CA_Total DESC;
```

### % Livraisons en retard par fournisseur
```sql
SELECT 
    f.Nom_Fournisseur,
    COUNT(*) AS Total_Livraisons,
    SUM(v.Indicateur_Retard) AS Nb_Retards,
    ROUND(AVG(v.Indicateur_Retard) * 100, 2) AS Pct_Retard
FROM FAIT_VENTES v
JOIN DIM_FOURNISSEUR f ON v.ID_Fournisseur = f.ID_Fournisseur
GROUP BY f.Nom_Fournisseur
ORDER BY Pct_Retard DESC;
```

### Panier moyen par client
```sql
SELECT 
    c.ID_Client,
    COUNT(*) AS Nb_Achats,
    SUM(v.Revenu_Reel) AS CA_Total,
    ROUND(AVG(v.Revenu_Reel), 2) AS Panier_Moyen
FROM FAIT_VENTES v
JOIN DIM_CLIENT c ON v.ID_Client = c.ID_Client
GROUP BY c.ID_Client
ORDER BY Panier_Moyen DESC;
```

---

##  DOCUMENTATION COMPLÈTE

### Pour le mapping détaillé
```bash
cat MAPPING_COLONNES_REEL.md
```

### Pour le modèle en étoile complet
```bash
# Compiler le LaTeX (nécessite texlive)
pdflatex SmartMarket_Modele_Etoile.tex
pdflatex TABLE_LATEX_MAPPING.tex

# Ou consulter en texte
cat RESUME_COMPLET.md
```

---

## ⚙ CONFIGURATION REQUISE

### Python
```bash
python3 --version  # >= 3.8
pip3 install pandas openpyxl
```

### Base de données (optionnel)
```bash
# PostgreSQL
sudo apt install postgresql

# MySQL
sudo apt install mysql-server

# SQLite (inclus avec Python)
```

### LaTeX (pour générer PDFs)
```bash
sudo apt install texlive-latex-base texlive-latex-extra
```

---

## 🐛 PROBLÈMES CONNUS

### 1. Données clients incomplètes
**Impact**: Impossible d'analyser par région, segmentation RFM limitée  
**Solution**: Créer feuille "Clients" avec 42 lignes

### 2. Données produits incomplètes
**Impact**: Impossible d'analyser par catégorie, top produits sans nom  
**Solution**: Créer feuille "Produits" avec 30 lignes

### 3. Lien Transactions-Fournisseurs manquant
**Impact**: Impossible de lier performance fournisseur aux ventes  
**Solution**: Ajouter colonne Fournisseur_ID dans Transactions

### 4. 15 valeurs NULL dans Revenu_Total
**Impact**: Calculs de CA incomplets  
**Solution**: Recalculer à partir de Prix_Unitaire × Quantité × (1-Remise%)

---

##  CHECKLIST DE VALIDATION

- [x] Données brutes analysées
- [x] Script de nettoyage créé et testé
- [x] Fichier nettoyé généré (SmartMarket_cleaned.xlsx)
- [x] Remises corrigées (0-100%)
- [x] Canaux standardisés
- [x] Scores satisfaction normalisés
- [x] Pays standardisés
- [x] Dates converties
- [x] Champs calculés créés
- [ ] Feuille "Clients" créée
- [ ] Feuille "Produits" créée
- [ ] Lien Fournisseurs établi
- [ ] Base de données créée
- [ ] Dimensions chargées
- [ ] Faits chargés
- [ ] Requêtes testées
- [ ] Dashboards créés

---

##  SUPPORT

Pour toute question sur:
- **Mapping des données**: Voir `MAPPING_COLONNES_REEL.md`
- **Modèle en étoile**: Voir `SmartMarket_Modele_Etoile.tex`
- **Résumé complet**: Voir `RESUME_COMPLET.md`
- **Scripts Python**: Commentaires dans les fichiers .py

---

##  LICENCE

Projet académique SmartMarket - Data Analytics  
© 2024 - Tous droits réservés
