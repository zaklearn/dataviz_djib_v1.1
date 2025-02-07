import streamlit as st
import pandas as pd
from visualization import create_comparative_boxplot, create_performance_distribution
from config import LABELS

def create_stats_page():
    st.title('Statistiques Descriptives')
    
    df = st.session_state.data
    
    # Interactive filters in sidebar
    with st.sidebar:
        st.header("Filtres")
        selected_regions = st.multiselect(
            'Régions',
            options=df['region'].unique(),
            default=df['region'].unique()
        )
        
        selected_school_types = st.multiselect(
            'Types d\'École',
            options=df['type_ecole'].unique(),
            default=df['type_ecole'].unique()
        )
        
        # Apply filters
        mask = (
            df['region'].isin(selected_regions) &
            df['type_ecole'].isin(selected_school_types)
        )
        filtered_df = df[mask]
    
    # Main content
    tab1, tab2 = st.tabs(["Distribution des Notes", "Analyses Croisées"])
    
    with tab1:
        st.subheader("Distribution des Notes par Matière")
        selected_subject = st.selectbox(
            "Sélectionnez une matière",
            ['mat_fr', 'mat_math', 'mat_phychi', 'mat_sc', 'mat_scterre'],
            format_func=lambda x: LABELS[x]
        )
        
        dist_fig = create_performance_distribution(filtered_df, selected_subject)
        st.plotly_chart(dist_fig, use_container_width=True)
        
        # Basic statistics
        st.subheader("Statistiques Descriptives")
        stats = filtered_df[selected_subject].describe()
        st.dataframe(stats)
    
    with tab2:
        st.subheader("Analyses Croisées")
        
        # Cross-tabulation options
        variable1 = st.selectbox(
            'Variable 1',
            ['genre', 'region', 'type_ecole'],
            format_func=lambda x: LABELS[x]
        )
        
        variable2 = st.selectbox(
            'Variable 2',
            ['result', 'mention'],
            format_func=lambda x: LABELS[x]
        )
        
        # Create and display cross-tabulation
        crosstab = pd.crosstab(
            filtered_df[variable1],
            filtered_df[variable2],
            margins=True
        )
        st.write("Tableau Croisé:")
        st.dataframe(crosstab)
        
        # Add visualization
        selected_var = st.selectbox(
            "Variable de groupement pour la visualisation",
            ['genre', 'region', 'type_ecole'],
            format_func=lambda x: LABELS[x]
        )
        
        box_fig = create_comparative_boxplot(
            filtered_df,
            selected_subject,
            selected_var
        )
        st.plotly_chart(box_fig, use_container_width=True)