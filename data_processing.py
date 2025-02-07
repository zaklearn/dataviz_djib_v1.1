import pandas as pd
from datetime import datetime
import streamlit as st
from config import REQUIRED_COLUMNS

def load_and_validate_data(file):
    """
    Charge et valide le fichier Excel contenant les données du BEF.
    """
    try:
        df = pd.read_excel(file)
        
        # Validation des colonnes requises
        missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)
        if missing_columns:
            st.error(f"Colonnes manquantes: {missing_columns}")
            return None
            
        return df
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier: {str(e)}")
        return None

def calculate_age(date_naiss):
    """
    Calcule l'âge à partir de la date de naissance.
    """
    if pd.isna(date_naiss) or date_naiss == '00/00/0000':
        return None
    try:
        if isinstance(date_naiss, str):
            date_naiss = pd.to_datetime(date_naiss, format='%d/%m/%Y', errors='coerce')
        elif not isinstance(date_naiss, pd.Timestamp):
            date_naiss = pd.to_datetime(date_naiss, errors='coerce')
        
        if pd.isna(date_naiss):
            return None
            
        current_year = datetime.now().year
        birth_year = date_naiss.year
        age = current_year - birth_year
        
        if age < 0 or age > 100:
            return None
            
        return age
    except Exception as e:
        return None

def preprocess_data(df):
    """
    Prétraite les données avec toutes les transformations nécessaires.
    """
    if df is None:
        return None
        
    df_processed = df.copy()
    
    # Calcul de l'âge
    df_processed['age'] = df_processed['date_naiss'].apply(calculate_age)
    median_age = df_processed['age'].median()
    df_processed['age'] = df_processed['age'].fillna(median_age)
    
    # Conversion des colonnes numériques
    numeric_columns = ['mat_fr', 'mat_math', 'mat_phychi', 'mat_sc', 'mat_scterre', 'moy', 'total']
    for col in numeric_columns:
        df_processed[col] = pd.to_numeric(df_processed[col], errors='coerce')
    
    return df_processed