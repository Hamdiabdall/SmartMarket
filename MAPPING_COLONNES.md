# 📊 MAPPING DES COLONNES EXCEL → DATA WAREHOUSE

## Colonnes Attendues dans SmartMarket_raw.xlsx

Ce document liste les colonnes attendues dans le fichier Excel source et leur correspondance avec les tables du Data Warehouse.

---

## 📋 LISTE DES COLONNES EXCEL ATTENDUES

### 🔹 TRANSACTIONS
1. **ID_Transaction** → FAIT_VENTES.ID_Vente
2. **Date_Transaction** → DIM_TEMPS.Date_Complete
3. **Quantite** → FAIT_VENTES.Quantite
4. **Prix_Unitaire** → FAIT_VENTES.Prix_Unitaire
5. **Taux_Remise** (ou Remise) → FAIT_VENTES.Taux_Remise
6. **Montant_Total** → FAIT_VENTES.Montant_Brut
7. **Canal_Vente** (ou Canal) → DIM_CANAL.Nom_Canal
8. **Note_Satisfaction** → FAIT_VENTES.Note_Satisfaction

### 🔹 CLIENTS
9. **ID_Client** → DIM_CLIENT.ID_Client
10. **Nom_Client** (ou Nom) → DIM_CLIENT.Nom_Client
11. **Prenom_Client** (ou Prenom) → DIM_CLIENT.Prenom_Client
12. **Email_Client** (ou Email) → DIM_CLIENT.Email
13. **Telephone_Client** (ou Tel) → DIM_CLIENT.Telephone
14. **Ville_Client** (ou Ville) → DIM_REGION.Ville
15. **Code_Postal** → DIM_REGION.Code_Postal
16. **Date_Inscription** → DIM_CLIENT.Date_Inscription

### 🔹 PRODUITS
17. **ID_Produit** → DIM_PRODUIT.ID_Produit
18. **Nom_Produit** (ou Produit) → DIM_PRODUIT.Nom_Produit
19. **Categorie_Produit** (ou Categorie) → DIM_PRODUIT.Categorie
20. **Sous_Categorie** → DIM_PRODUIT.Sous_Categorie
21. **Prix_Catalogue** → DIM_PRODUIT.Prix_Catalogue
22. **Marque** → DIM_PRODUIT.Marque

### 🔹 LIVRAISON & FOURNISSEURS
23. **ID_Fournisseur** → DIM_FOURNISSEUR.ID_Fournisseur
24. **Nom_Fournisseur** (ou Fournisseur) → DIM_FOURNISSEUR.Nom_Fournisseur
25. **Date_Livraison** → (calcul: Delai_Livraison_Jours)
26. **Date_Prevue_Livraison** → (calcul: Indicateur_Retard)
27. **Delai_Livraison** → FAIT_VENTES.Delai_Livraison_Jours
28. **Statut_Livraison** → FAIT_VENTES.Indicateur_Retard

---

## 🧮 CHAMPS CALCULÉS

Ces champs sont calculés lors du processus ETL:

| Champ | Formule |
|-------|---------|
| **Montant_Brut** | `Prix_Unitaire × Quantite` |
| **Montant_Remise** | `Montant_Brut × (Taux_Remise / 100)` |
| **Revenu_Reel** | `Montant_Brut - Montant_Remise` |
| **Delai_Livraison_Jours** | `Date_Livraison - Date_Transaction` (en jours) |
| **Indicateur_Retard** | `IF(Date_Livraison > Date_Prevue_Livraison, 1, 0)` |
| **Segment_RFM** | Basé sur Récence, Fréquence, Montant |
| **Statut_Activite** | `IF(Derniere_Transaction < Aujourdhui - 365j, 'Inactif', 'Actif')` |

---

## 📊 INSTRUCTIONS D'UTILISATION

1. **Exécuter le script d'analyse**:
   ```bash
   python3 analyze_excel.py
   ```

2. **Vérifier les colonnes**: Comparez la sortie du script avec la liste ci-dessus

3. **Adapter le mapping**: Si les noms de colonnes diffèrent, ajustez le processus ETL en conséquence

4. **Nettoyer les données**: Appliquez les règles de nettoyage avant l'import dans le DW
