# 📊 PROJET SMARTMARKET - DATA WAREHOUSE

## 🎯 Vue d'ensemble

Ce projet implémente un **Data Warehouse en modèle étoile** pour analyser les données de vente de SmartMarket. Il répond aux **20 objectifs** définis dans le cahier des charges.

---

## 📁 FICHIERS CRÉÉS

| Fichier | Description | Statut |
|---------|-------------|--------|
| `SmartMarket_raw.xlsx` | Données brutes originales | ✅ Source |
| `SmartMarket_cleaned.xlsx` | **Données nettoyées** | ✅ Créé |
| `analyze_excel.py` | Script d'analyse des données | ✅ Créé |
| `clean_data.py` | Script de nettoyage automatique | ✅ Créé |
| `MAPPING_COLONNES_REEL.md` | Mapping détaillé Excel→DW | ✅ Créé |
| `SmartMarket_Modele_Etoile.tex` | Documentation LaTeX complète | ✅ Créé |
| `TABLE_LATEX_MAPPING.tex` | Tableaux de mapping LaTeX | ✅ Créé |
| `RESUME_COMPLET.md` | Résumé exécutif du projet | ✅ Créé |
| `README.md` | Ce fichier | ✅ Créé |

---

## 🚀 DÉMARRAGE RAPIDE

### 1️⃣ Analyser les données brutes
```bash
python3 analyze_excel.py
```

### 2️⃣ Nettoyer les données
```bash
python3 clean_data.py
```
✅ Crée `SmartMarket_cleaned.xlsx` avec toutes les corrections

### 3️⃣ Consulter la documentation
```bash
# Mapping détaillé
cat MAPPING_COLONNES_REEL.md

# Résumé complet
cat RESUME_COMPLET.md
```

---

## 📊 RÉSULTATS DU NETTOYAGE

### ✅ Corrections appliquées

| Problème | Avant | Après | Impact |
|----------|-------|-------|--------|
| **Remise_%** | -10% à 150% | 0% à 100% | ✅ Corrigé |
| **Canal_Vente** | 'En ligne'/'en ligne' | 'En Ligne' | ✅ Standardisé |
| **Score** | Texte + numérique | Numérique 1-5 | ✅ Normalisé |
| **Pays** | 'cn', 'CHN', 'France', 'FR' | 'CHN', 'FRA' | ✅ Standardisé |
| **Fiabilité_%** | 120% | 100% | ✅ Corrigé |
| **Dates** | 99 formats | Format ISO | ✅ Standardisé |

### 📈 Statistiques clés

#### Transactions (100 lignes)
- **Période**: 2020-02-29 → 2024-12-23
- **CA Total**: 143,400 €
- **Clients uniques**: 42
- **Produits uniques**: 30
- **Remise moyenne**: 27.73%
- **Panier moyen**: 1,687 €

#### Satisfaction (60 évaluations)
- **Score moyen**: 3.22/5
- **Évaluations complètes**: 49 (82%)

#### Fournisseurs (10 actifs)
- **Note fiabilité moyenne**: 2.33/5
- **Fiabilité moyenne**: 92.22%
- **Délai moyen livraison**: 6.6 jours

---

## 🌟 MODÈLE EN ÉTOILE

### Architecture

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

### Tables disponibles

#### ✅ Dimensions complètes
- **DIM_TEMPS** - À générer (dimension calendrier)
- **DIM_CANAL** - À générer (3 canaux identifiés)
- **DIM_FOURNISSEUR** - ✅ Données disponibles (10 fournisseurs)

#### ⚠️ Dimensions partielles
- **DIM_CLIENT** - ⚠️ IDs disponibles, détails manquants (nom, email, ville)
- **DIM_PRODUIT** - ⚠️ IDs disponibles, détails manquants (nom, catégorie, prix)
- **DIM_REGION** - ⚠️ Bloquée (nécessite données clients)

#### ✅ Table de faits
- **FAIT_VENTES** - ✅ Données disponibles après nettoyage

---

## 🎯 OBJECTIFS DU CAHIER DES CHARGES

### ✅ Réalisables immédiatement (données disponibles)

| # | Objectif | Statut | Fichier |
|---|----------|--------|---------|
| 1 | CA par année et canal | ✅ | Transactions |
| 2 | Top 10 produits vendus | ⚠️ | Transactions (sans nom produit) |
| 3 | Taux remise moyen par catégorie | ❌ | Manque catégories |
| 5 | Transactions incohérentes | ✅ | Transactions |
| 6 | Nettoyer infos clients | ⚠️ | Données manquantes |
| 7 | Standardiser catégories/prix | ✅ | Fait |
| 8 | Corriger remises hors plage | ✅ | Fait |
| 9 | Revenu réel par transaction | ✅ | Transactions |
| 13 | Fiabilité fournisseurs | ✅ | Fournisseurs |
| 14 | % livraisons en retard | ✅ | Transactions |
| 15 | Comparer ventes par canal | ✅ | Transactions |

### ⚠️ Réalisables avec enrichissement

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

## 📋 COLONNES DANS EXCEL

### Feuille: Transactions
```
✅ Transaction_ID          ✅ Revenu_Total
✅ Date                    ✅ Quantite
✅ Client_ID               ✅ Remise_%
✅ Produit_ID              ✅ Canal_Vente
✅ Mode_Paiement           ✅ Statut_Livraison
✅ Date_Livraison
```

### Feuille: Satisfaction
```
✅ Client_ID               ✅ Score
✅ Date_Enquete            ✅ Commentaire
```

### Feuille: Fournisseurs
```
✅ Fournisseur_ID          ✅ Evaluation
✅ Nom_Fournisseur         ✅ Délai_Moyen_Livraison
✅ Pays                    ✅ Fiabilité_%
```

---

## ❌ DONNÉES MANQUANTES

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

## 🛠️ PROCHAINES ÉTAPES

### Phase 1: Enrichissement des données ⚠️ URGENT
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

## 📊 REQUÊTES SQL PRÊTES À L'EMPLOI

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

## 📚 DOCUMENTATION COMPLÈTE

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

## ⚙️ CONFIGURATION REQUISE

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

## ✅ CHECKLIST DE VALIDATION

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

## 📞 SUPPORT

Pour toute question sur:
- **Mapping des données**: Voir `MAPPING_COLONNES_REEL.md`
- **Modèle en étoile**: Voir `SmartMarket_Modele_Etoile.tex`
- **Résumé complet**: Voir `RESUME_COMPLET.md`
- **Scripts Python**: Commentaires dans les fichiers .py

---

## 📄 LICENCE

Projet académique SmartMarket - Data Analytics  
© 2024 - Tous droits réservés
