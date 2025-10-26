#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'analyse du fichier SmartMarket_raw.xlsx
Affiche la structure des données et les colonnes disponibles
"""

import pandas as pd
import sys

def analyze_excel(file_path):
    """Analyse le fichier Excel et affiche sa structure"""
    try:
        excel_file = pd.ExcelFile(file_path)
        
        print("="*80)
        print("ANALYSE DU FICHIER SMARTMARKET_RAW.XLSX")
        print("="*80)
        
        print(f"\n📊 Nombre de feuilles: {len(excel_file.sheet_names)}")
        print(f"Noms des feuilles: {excel_file.sheet_names}\n")
        
        for sheet_name in excel_file.sheet_names:
            print("\n" + "="*80)
            print(f"FEUILLE: {sheet_name}")
            print("="*80)
            
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            print(f"\n📏 Dimensions: {df.shape[0]} lignes × {df.shape[1]} colonnes")
            
            print("\n📋 COLONNES DISPONIBLES:")
            print("-" * 80)
            for i, (col, dtype) in enumerate(zip(df.columns, df.dtypes), 1):
                non_null = df[col].notna().sum()
                null_count = df[col].isna().sum()
                print(f"{i:2d}. {col:35s} | Type: {str(dtype):15s} | Non-null: {non_null:5d} | Null: {null_count:5d}")
            
            print("\n📄 APERÇU DES DONNÉES (5 premières lignes):")
            print("-" * 80)
            print(df.head())
            
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
            if len(numeric_cols) > 0:
                print("\n📊 STATISTIQUES DESCRIPTIVES:")
                print("-" * 80)
                print(df[numeric_cols].describe())
            
            categorical_cols = df.select_dtypes(include=['object']).columns
            if len(categorical_cols) > 0:
                print("\n🏷️  VALEURS UNIQUES (colonnes catégorielles):")
                print("-" * 80)
                for col in categorical_cols:
                    unique_count = df[col].nunique()
                    print(f"{col:35s} | {unique_count:5d} valeurs uniques")
                    if unique_count <= 10:
                        print(f"   → {df[col].unique()[:10].tolist()}")
            
        print("\n" + "="*80)
        print("ANALYSE TERMINÉE")
        print("="*80)
        
    except Exception as e:
        print(f"❌ Erreur: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    file_path = "../data/SmartMarket_raw.xlsx"
    analyze_excel(file_path)
