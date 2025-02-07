import os
import sys
import pandas as pd
import streamlit as st

# Configuration du chemin d'accès
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from data_processing import load_and_validate_data, preprocess_data
from analysis import analyze_demographics, analyze_results
from visualization import create_gender_chart, create_region_chart, create_result_distribution_chart

def calculate_success_rates(df):
    """
    Calcule les statistiques détaillées des résultats pour les valeurs
    'Admis(e)' et 'Ajourné(e)'
    """
    total_students = len(df)
    admis_count = df['result'].eq('Admis(e)').sum()
    ajourne_count = df['result'].eq('Ajourné(e)').sum()
    
    success_rate = (admis_count / total_students) * 100 if total_students > 0 else 0
    failure_rate = (ajourne_count / total_students) * 100 if total_students > 0 else 0
    
    stats_by_gender = df.groupby('genre')['result'].apply(
        lambda x: (x == 'Admis(e)').sum() / len(x) * 100
    ).round(2)
    
    return {
        'total': total_students,
        'admis': admis_count,
        'ajourne': ajourne_count,
        'success_rate': success_rate,
        'failure_rate': failure_rate,
        'stats_by_gender': stats_by_gender
    }

def display_performance_metrics(stats, df):
    """
    Affiche les métriques de performance principales
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Étudiants",
            value=f"{stats['total']:,}",
            delta=None,
            help="Nombre total de candidats"
        )
    
    with col2:
        st.metric(
            label="Taux de Réussite",
            value=f"{stats['success_rate']:.1f}%",
            delta=None,
            help=f"Admis(e): {stats['admis']:,} sur {stats['total']:,} candidats"
        )
    
    with col3:
        st.metric(
            label="Moyenne Générale",
            value=f"{df['moy'].mean():.2f}/20",
            delta=None,
            help="Moyenne de tous les candidats"
        )
    
    with col4:
        st.metric(
            label="Établissements",
            value=f"{df['etabl'].nunique():,}",
            delta=None,
            help="Nombre total d'établissements"
        )

def display_detailed_statistics(stats):
    """
    Affiche les statistiques détaillées des résultats
    """
    st.subheader("Statistiques Détaillées des Résultats")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("Résultats Globaux :")
        st.write(f"Total des candidats : {stats['total']:,}")
        st.write(f"Admis(e) : {stats['admis']:,} ({stats['success_rate']:.1f}%)")
        st.write(f"Ajourné(e) : {stats['ajourne']:,} ({stats['failure_rate']:.1f}%)")
    
    with col2:
        if not stats['stats_by_gender'].empty:
            st.write("Taux de Réussite par Genre :")
            for genre, taux in stats['stats_by_gender'].items():
                st.write(f"{genre} : {taux:.1f}%")

def create_home_page():
    """
    Crée la page d'accueil de l'application
    """
    st.title('Analyse des Résultats du BEF')
    
    uploaded_file = st.file_uploader(
        "Charger le fichier Excel",
        type=['xlsx', 'xls'],
        help="Sélectionnez le fichier contenant les données du BEF"
    )
    
    if uploaded_file:
        df = load_and_validate_data(uploaded_file)
        if df is not None:
            df = preprocess_data(df)
            st.session_state.data = df
            
            # Calcul et affichage des statistiques
            stats = calculate_success_rates(df)
            display_performance_metrics(stats, df)
            display_detailed_statistics(stats)
            
            # Visualisations
            st.subheader("Visualisations des Données")
            
            tab1, tab2 = st.tabs(["Distribution par Genre", "Distribution des Résultats"])
            
            with tab1:
                demographics = analyze_demographics(df)
                gender_chart = create_gender_chart(demographics['by_gender'])
                st.plotly_chart(gender_chart, use_container_width=True)
            
            with tab2:
                result_chart = create_result_distribution_chart(stats)
                st.plotly_chart(result_chart, use_container_width=True)
            
            # Aperçu des données
            with st.expander("Aperçu des Données"):
                st.dataframe(
                    df.head(),
                    use_container_width=True,
                    column_config={
                        "result": st.column_config.TextColumn(
                            "Résultat",
                            help="Admis(e) ou Ajourné(e)"
                        )
                    }
                )