#  MAPPING RÉEL: SmartMarket_raw.xlsx → Data Warehouse

##  Structure du Fichier Excel

Votre fichier contient **3 feuilles**:
1. **Transactions** - 100 lignes × 11 colonnes
2. **Satisfaction** - 60 lignes × 4 colonnes  
3. **Fournisseurs** - 10 lignes × 6 colonnes

---

## 🔷 FEUILLE 1: TRANSACTIONS (100 lignes)

| N° | Colonne Excel | Type | Table DW | Champ DW | Transformation |
|----|---------------|------|----------|----------|----------------|
| 1 | Transaction_ID | object | FAIT_VENTES | ID_Vente | Nettoyer doublons |
| 2 | Date | object | DIM_TEMPS | Date_Complete | Standardiser format date |
| 3 | Client_ID | object | DIM_CLIENT | ID_Client | Clé étrangère |
| 4 | Produit_ID | object | DIM_PRODUIT | ID_Produit | Clé étrangère |
| 5 | Quantite | int64 | FAIT_VENTES | Quantite | Vérifier > 0 |
| 6 | Remise_% | float64 | FAIT_VENTES | Taux_Remise | ** Corriger -10% et 150%** |
| 7 | Canal_Vente | object | DIM_CANAL | Nom_Canal | ** Standardiser: 'En ligne'/'en ligne'** |
| 8 | Mode_Paiement | object | - | - | Dimension additionnelle possible |
| 9 | Statut_Livraison | object | FAIT_VENTES | Indicateur_Retard | Mapper à 0/1 |
| 10 | Date_Livraison | object | FAIT_VENTES | Delai_Livraison_Jours | Calculer: Date_Livraison - Date |
| 11 | Revenu_Total | float64 | FAIT_VENTES | Revenu_Reel | ** 15 valeurs NULL** |

###  PROBLÈMES DÉTECTÉS - Transactions

1. **Remise_%**: Valeurs aberrantes (-10%, 150%) → Corriger à [0-100%]
2. **Canal_Vente**: Incohérence casse ('En ligne' vs 'en ligne') → Standardiser
3. **Revenu_Total**: 15 valeurs NULL → Recalculer si possible
4. **Date**: 99 formats différents → Standardiser au format ISO (YYYY-MM-DD)
5. **Statut_Livraison**: 21 valeurs NULL → Vérifier intégrité

---

## 🔷 FEUILLE 2: SATISFACTION (60 lignes)

| N° | Colonne Excel | Type | Table DW | Champ DW | Transformation |
|----|---------------|------|----------|----------|----------------|
| 1 | Client_ID | object | DIM_CLIENT | ID_Client | Jointure avec Transactions |
| 2 | Date_Enquete | object | DIM_TEMPS | Date_Complete | Standardiser format |
| 3 | Score | object | FAIT_VENTES | Note_Satisfaction | ** Convertir texte en numérique** |
| 4 | Commentaire | object | - | - | Analyse qualitative optionnelle |

###  PROBLÈMES DÉTECTÉS - Satisfaction

1. **Score**: Valeurs mixtes (1-5, 'Bon', 'Très satisfait') → Normaliser sur échelle 1-5
2. **Score**: 11 valeurs NULL → Décider comment traiter
3. **Date_Enquete**: Formats multiples → Standardiser

**Mapping suggéré pour Score**:
- 'Très satisfait' → 5
- 'Bon' → 4
- Numérique (1-5) → Garder tel quel

---

## 🔷 FEUILLE 3: FOURNISSEURS (10 lignes)

| N° | Colonne Excel | Type | Table DW | Champ DW | Transformation |
|----|---------------|------|----------|----------|----------------|
| 1 | Fournisseur_ID | object | DIM_FOURNISSEUR | ID_Fournisseur | Clé primaire |
| 2 | Nom_Fournisseur | object | DIM_FOURNISSEUR | Nom_Fournisseur | OK |
| 3 | Pays | object | DIM_FOURNISSEUR | Pays_Origine | ** Standardiser codes pays** |
| 4 | Evaluation | float64 | DIM_FOURNISSEUR | Note_Fiabilite | ** Normaliser sur 1-5** |
| 5 | Délai_Moyen_Livraison | object | DIM_FOURNISSEUR | Delai_Moyen_Livraison | ** Convertir 'non défini'** |
| 6 | Fiabilité_% | float64 | DIM_FOURNISSEUR | Taux_Retard_Pct | ** Corriger 120%** |

###  PROBLÈMES DÉTECTÉS - Fournisseurs

1. **Pays**: Incohérence ('cn', 'CHN', 'France', 'FR') → Standardiser ('CHN', 'FRA')
2. **Evaluation**: Échelle 3-10 → Normaliser sur 1-5
3. **Délai_Moyen_Livraison**: Valeur 'non défini' → Remplacer par NULL ou moyenne
4. **Fiabilité_%**: Valeur 120% (impossible) → Corriger à max 100%

---

##  CHAMPS CALCULÉS À CRÉER

| Champ Calculé | Formule | Source |
|---------------|---------|--------|
| **Prix_Unitaire** | `Revenu_Total / (Quantite × (1 - Remise_%/100))` | Transactions |
| **Montant_Brut** | `Prix_Unitaire × Quantite` | Transactions |
| **Montant_Remise** | `Montant_Brut × Remise_%/100` | Transactions |
| **Delai_Livraison_Jours** | `Date_Livraison - Date` | Transactions |
| **Indicateur_Retard** | `IF(Statut_Livraison = 'En attente', 1, 0)` | Transactions |

---

##  RÈGLES DE NETTOYAGE PAR COLONNE

### Remise_% (CRITIQUE)
```python
# Corriger les valeurs hors plage
df.loc[df['Remise_%'] < 0, 'Remise_%'] = 0
df.loc[df['Remise_%'] > 100, 'Remise_%'] = 100
```

### Canal_Vente (CRITIQUE)
```python
# Standardiser les valeurs
df['Canal_Vente'] = df['Canal_Vente'].str.strip().str.title()
# 'En ligne'/'en ligne' → 'En Ligne'
# 'Telephone' → 'Téléphone'
```

### Pays (Fournisseurs)
```python
# Dictionnaire de mapping
pays_mapping = {
    'cn': 'CHN', 'CHN': 'CHN',
    'France': 'FRA', 'FR': 'FRA'
}
df['Pays'] = df['Pays'].map(pays_mapping)
```

### Score (Satisfaction)
```python
# Convertir texte en numérique
score_mapping = {
    'Très satisfait': 5,
    'Bon': 4
}
df['Score'] = df['Score'].replace(score_mapping)
df['Score'] = pd.to_numeric(df['Score'], errors='coerce')
```

### Evaluation (Fournisseurs)
```python
# Normaliser de [3-10] à [1-5]
df['Evaluation'] = ((df['Evaluation'] - 3) / 7) * 4 + 1
df['Evaluation'] = df['Evaluation'].clip(1, 5)
```

---

##  COLONNES MANQUANTES (à créer ou obtenir)

Les colonnes suivantes sont attendues dans le modèle mais absentes du fichier Excel:

### DIM_CLIENT
-  Nom_Client
-  Prenom_Client  
-  Email
-  Telephone
-  Date_Inscription
-  Ville
-  Code_Postal

**Solution**: Créer une feuille "Clients" ou obtenir ces données d'une autre source

### DIM_PRODUIT
-  Nom_Produit
-  Categorie
-  Sous_Categorie
-  Prix_Catalogue
-  Marque

**Solution**: Créer une feuille "Produits" ou obtenir ces données d'une autre source

---

##  PLAN D'ACTION ETL

### Phase 1: Nettoyage
1.  Corriger Remise_% (valeurs hors [0-100])
2.  Standardiser Canal_Vente (casse incohérente)
3.  Normaliser Score satisfaction (texte → numérique)
4.  Standardiser codes Pays
5.  Corriger Fiabilité_% > 100%
6.  Convertir dates au format ISO

### Phase 2: Transformation
1.  Calculer Prix_Unitaire (rétro-calculé depuis Revenu_Total)
2.  Calculer Delai_Livraison_Jours
3.  Créer Indicateur_Retard
4.  Normaliser Evaluation fournisseurs (1-5)
5.  Gérer valeurs NULL dans Revenu_Total

### Phase 3: Enrichissement
1.  Obtenir données clients (nom, email, ville, etc.)
2.  Obtenir données produits (nom, catégorie, prix, etc.)
3.  Créer dimension DIM_TEMPS
4.  Créer dimension DIM_CANAL
5.  Créer dimension DIM_REGION (depuis données clients)

### Phase 4: Chargement
1.  Charger dimensions (CLIENTS, PRODUITS, TEMPS, etc.)
2.  Charger table de faits (FAIT_VENTES)
3.  Vérifier intégrité référentielle
4.  Créer index et clés étrangères

---

##  STATISTIQUES DESCRIPTIVES

### Transactions
- **Quantité moyenne**: 4.65 unités
- **Remise moyenne**: 35.45% (après nettoyage sera réduit)
- **Revenu moyen**: 1,687 €
- **Problèmes qualité**: 
  - 12 valeurs NULL dans Remise_%
  - 18 valeurs NULL dans Canal_Vente
  - 15 valeurs NULL dans Revenu_Total

### Satisfaction
- **Clients uniques**: 39
- **Score moyen**: À calculer après nettoyage
- **Taux de réponse commentaires**: 68.3% (41/60)

### Fournisseurs
- **Nombre total**: 10 fournisseurs
- **Évaluation moyenne**: 5.33/10 (à normaliser)
- **Fiabilité moyenne**: 96.67% (après correction)
- **Pays représentés**: 2 (Chine, France)

---

##  PROCHAINES ÉTAPES

1. **Exécuter le script de nettoyage** (à créer)
2. **Obtenir les données manquantes** (clients, produits)
3. **Valider les transformations** avec les parties prenantes
4. **Créer le schéma du Data Warehouse**
5. **Développer les scripts ETL**
6. **Tester et valider**
