import streamlit as st

# Configuration de la page
PAGE_CONFIG = {
    "page_title": "Analyse BEF",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Étiquettes et traductions des colonnes
LABELS = {
    'mat_fr': 'Français',
    'mat_math': 'Mathématiques',
    'mat_phychi': 'Physique-Chimie',
    'mat_sc': 'Sciences',
    'mat_scterre': 'Sciences de la Terre',
    'genre': 'Genre',
    'region': 'Région',
    'type_ecole': "Type d'École",
    'etabl': 'Établissement',
    'result': 'Résultat',
    'mention': 'Mention',
    'milieu' : 'Milieu'
}

# Colonnes requises pour la validation des données
REQUIRED_COLUMNS = [
    'ID', 'date_naiss', 'genre', 'region', 'milieu', 'type_ecole', 'lieu_naiss', 
    'nationalite', 'etabl', 'class', 'control_cont', 'mat_fr', 'mat_math',
    'mat_phychi', 'mat_sc', 'mat_scterre', 'mention', 'total',
    'moy', 'result'
]

# Schémas de couleurs
COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'success': '#2ca02c',
    'warning': '#d62728',
    'background': '#ffffff',
    'text': '#333333'
}