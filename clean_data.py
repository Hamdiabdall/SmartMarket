#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de nettoyage des données SmartMarket
Corrige tous les problèmes de qualité détectés
"""

import pandas as pd
import numpy as np
from datetime import datetime
import sys

def clean_transactions(df):
    """Nettoie la feuille Transactions"""
    print("\n🔧 Nettoyage TRANSACTIONS...")
    
    # 1. Corriger Remise_% hors plage [0-100]
    print(f"  - Remises avant: min={df['Remise_%'].min()}, max={df['Remise_%'].max()}")
    df['Remise_%'] = df['Remise_%'].clip(0, 100)
    print(f"  - Remises après: min={df['Remise_%'].min()}, max={df['Remise_%'].max()}")
    
    # 2. Standardiser Canal_Vente
    print(f"  - Canaux avant: {df['Canal_Vente'].unique()}")
    df['Canal_Vente'] = df['Canal_Vente'].str.strip().str.title()
    mapping_canal = {
        'En Ligne': 'En Ligne',
        'Boutique': 'Boutique', 
        'Telephone': 'Téléphone'
    }
    df['Canal_Vente'] = df['Canal_Vente'].replace(mapping_canal)
    print(f"  - Canaux après: {df['Canal_Vente'].unique()}")
    
    # 3. Standardiser dates
    print("  - Conversion des dates...")
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce', infer_datetime_format=True)
    df['Date_Livraison'] = pd.to_datetime(df['Date_Livraison'], errors='coerce', infer_datetime_format=True)
    
    # 4. Calculer Prix_Unitaire (rétro-calculé)
    print("  - Calcul Prix_Unitaire...")
    df['Prix_Unitaire'] = df['Revenu_Total'] / (
        df['Quantite'] * (1 - df['Remise_%']/100)
    )
    
    # 5. Calculer champs dérivés
    print("  - Calcul champs dérivés...")
    df['Montant_Brut'] = df['Prix_Unitaire'] * df['Quantite']
    df['Montant_Remise'] = df['Montant_Brut'] * (df['Remise_%'] / 100)
    
    # 6. Calculer délai livraison
    df['Delai_Livraison_Jours'] = (df['Date_Livraison'] - df['Date']).dt.days
    
    # 7. Créer indicateur retard
    df['Indicateur_Retard'] = (df['Statut_Livraison'] == 'En attente').astype(int)
    
    # 8. Standardiser Mode_Paiement
    df['Mode_Paiement'] = df['Mode_Paiement'].str.strip().str.title()
    df['Mode_Paiement'] = df['Mode_Paiement'].replace({'Cheque': 'Chèque', 'Cb': 'CB', 'Espece': 'Espèce'})
    
    print(f"✅ Transactions nettoyées: {len(df)} lignes")
    return df

def clean_satisfaction(df):
    """Nettoie la feuille Satisfaction"""
    print("\n🔧 Nettoyage SATISFACTION...")
    
    # 1. Mapper Score texte vers numérique
    print(f"  - Scores avant: {df['Score'].unique()}")
    score_mapping = {
        'Très satisfait': 5,
        'Bon': 4,
        'bon': 4,
        'Moyen': 3,
        'Mauvais': 2,
        'Très mauvais': 1
    }
    df['Score'] = df['Score'].replace(score_mapping)
    df['Score'] = pd.to_numeric(df['Score'], errors='coerce')
    print(f"  - Scores après conversion: min={df['Score'].min()}, max={df['Score'].max()}")
    
    # 2. Standardiser date enquête
    df['Date_Enquete'] = pd.to_datetime(df['Date_Enquete'], errors='coerce', infer_datetime_format=True)
    
    # 3. Nettoyer commentaires
    df['Commentaire'] = df['Commentaire'].str.strip()
    
    print(f"✅ Satisfaction nettoyée: {len(df)} lignes")
    return df

def clean_fournisseurs(df):
    """Nettoie la feuille Fournisseurs"""
    print("\n🔧 Nettoyage FOURNISSEURS...")
    
    # 1. Standardiser Pays
    print(f"  - Pays avant: {df['Pays'].unique()}")
    pays_mapping = {
        'cn': 'CHN',
        'CHN': 'CHN',
        'China': 'CHN',
        'France': 'FRA',
        'FR': 'FRA',
        'fr': 'FRA'
    }
    df['Pays'] = df['Pays'].map(pays_mapping)
    print(f"  - Pays après: {df['Pays'].unique()}")
    
    # 2. Normaliser Evaluation sur échelle 1-5
    print(f"  - Evaluation avant: min={df['Evaluation'].min()}, max={df['Evaluation'].max()}")
    # Formule: ((x - min) / (max - min)) * 4 + 1
    df['Note_Fiabilite'] = ((df['Evaluation'] - 3) / 7) * 4 + 1
    df['Note_Fiabilite'] = df['Note_Fiabilite'].clip(1, 5).round(2)
    print(f"  - Note_Fiabilite après: min={df['Note_Fiabilite'].min()}, max={df['Note_Fiabilite'].max()}")
    
    # 3. Corriger Fiabilité_% > 100
    print(f"  - Fiabilité_% avant: min={df['Fiabilité_%'].min()}, max={df['Fiabilité_%'].max()}")
    df['Fiabilité_%'] = df['Fiabilité_%'].clip(0, 100)
    print(f"  - Fiabilité_% après: min={df['Fiabilité_%'].min()}, max={df['Fiabilité_%'].max()}")
    
    # 4. Gérer Délai "non défini"
    df['Délai_Moyen_Livraison'] = pd.to_numeric(df['Délai_Moyen_Livraison'], errors='coerce')
    
    print(f"✅ Fournisseurs nettoyés: {len(df)} lignes")
    return df

def generate_report(df_trans, df_satisf, df_fourn):
    """Génère un rapport de nettoyage"""
    print("\n" + "="*80)
    print("📊 RAPPORT DE NETTOYAGE")
    print("="*80)
    
    print("\n🔹 TRANSACTIONS")
    print(f"  Lignes totales: {len(df_trans)}")
    print(f"  Période: {df_trans['Date'].min()} → {df_trans['Date'].max()}")
    print(f"  Clients uniques: {df_trans['Client_ID'].nunique()}")
    print(f"  Produits uniques: {df_trans['Produit_ID'].nunique()}")
    print(f"  CA Total: {df_trans['Revenu_Total'].sum():,.2f} €")
    print(f"  Remise moyenne: {df_trans['Remise_%'].mean():.2f}%")
    print(f"  Panier moyen: {df_trans['Revenu_Total'].mean():,.2f} €")
    
    print("\n🔹 SATISFACTION")
    print(f"  Évaluations totales: {len(df_satisf)}")
    print(f"  Score moyen: {df_satisf['Score'].mean():.2f}/5")
    print(f"  Scores NULL: {df_satisf['Score'].isna().sum()}")
    
    print("\n🔹 FOURNISSEURS")
    print(f"  Fournisseurs actifs: {len(df_fourn)}")
    print(f"  Note fiabilité moyenne: {df_fourn['Note_Fiabilite'].mean():.2f}/5")
    print(f"  Fiabilité moyenne: {df_fourn['Fiabilité_%'].mean():.2f}%")
    print(f"  Délai moyen: {df_fourn['Délai_Moyen_Livraison'].mean():.1f} jours")
    
    print("\n" + "="*80)

def main():
    """Fonction principale"""
    input_file = "/home/hamdi/Desktop/Data-Anaytic/SmartMarket_raw.xlsx"
    output_file = "/home/hamdi/Desktop/Data-Anaytic/SmartMarket_cleaned.xlsx"
    
    print("="*80)
    print("🚀 DÉMARRAGE DU NETTOYAGE DES DONNÉES SMARTMARKET")
    print("="*80)
    
    try:
        # Charger les données
        print(f"\n📂 Lecture du fichier: {input_file}")
        excel_file = pd.ExcelFile(input_file)
        
        df_transactions = pd.read_excel(excel_file, 'Transactions')
        df_satisfaction = pd.read_excel(excel_file, 'Satisfaction')
        df_fournisseurs = pd.read_excel(excel_file, 'Fournisseurs')
        
        print(f"✅ Données chargées:")
        print(f"   - Transactions: {len(df_transactions)} lignes")
        print(f"   - Satisfaction: {len(df_satisfaction)} lignes")
        print(f"   - Fournisseurs: {len(df_fournisseurs)} lignes")
        
        # Nettoyer chaque feuille
        df_transactions_clean = clean_transactions(df_transactions)
        df_satisfaction_clean = clean_satisfaction(df_satisfaction)
        df_fournisseurs_clean = clean_fournisseurs(df_fournisseurs)
        
        # Générer rapport
        generate_report(df_transactions_clean, df_satisfaction_clean, df_fournisseurs_clean)
        
        # Sauvegarder
        print(f"\n💾 Sauvegarde du fichier nettoyé: {output_file}")
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            df_transactions_clean.to_excel(writer, sheet_name='Transactions', index=False)
            df_satisfaction_clean.to_excel(writer, sheet_name='Satisfaction', index=False)
            df_fournisseurs_clean.to_excel(writer, sheet_name='Fournisseurs', index=False)
        
        print("\n✅ NETTOYAGE TERMINÉ AVEC SUCCÈS!")
        print(f"📁 Fichier créé: {output_file}")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
