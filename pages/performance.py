import streamlit as st
from analysis import analyze_subject_performance, calculate_performance_gaps
from visualization import create_heatmap, create_zero_score_analysis
from config import LABELS
import pandas as pd
def create_performance_page():
    st.title('Analyse des Performances')
    
    df = st.session_state.data
    
    # Create tabs for different analyses
    tab1, tab2, tab3 = st.tabs([
        "Performance par Matière",
        "Analyse des Notes Zéro",
        "Écarts de Performance"
    ])
    
    # Get subject performance analysis
    performance = analyze_subject_performance(df)
    
    with tab1:
        st.subheader("Performance par Matière")
        
        # Display average scores
        st.write("Moyennes par Matière")
        averages_df = pd.DataFrame({
            'Matière': [LABELS[subj] for subj in performance['averages'].keys()],
            'Moyenne': performance['averages'].values()
        })
        st.dataframe(averages_df)
        
        # Create correlation heatmap
        subjects = ['mat_fr', 'mat_math', 'mat_phychi', 'mat_sc', 'mat_scterre']
        correlations = df[subjects].corr()
        
        st.subheader("Corrélations entre les Matières")
        heatmap = create_heatmap(correlations)
        st.plotly_chart(heatmap, use_container_width=True)
    
    with tab2:
        st.subheader("Analyse des Notes Zéro")
        
        # Display zero score analysis
        zero_fig = create_zero_score_analysis(performance['zero_scores'])
        st.plotly_chart(zero_fig, use_container_width=True)
        
        # Detailed statistics
        st.write("Pourcentage de Notes Zéro par Matière")
        zero_stats = pd.DataFrame({
            'Matière': [LABELS[subj] for subj in performance['zero_scores'].keys()],
            'Nombre de Zéros': performance['zero_scores'].values(),
            'Pourcentage': [
                f"{(count/len(df))*100:.2f}%" 
                for count in performance['zero_scores'].values()
            ]
        })
        st.dataframe(zero_stats)
    
    with tab3:
        st.subheader("Analyse des Écarts de Performance")
        
        # Select subject and grouping variable
        col1, col2 = st.columns(2)
        with col1:
            selected_subject = st.selectbox(
                "Sélectionnez une matière",
                ['mat_fr', 'mat_math', 'mat_phychi', 'mat_sc', 'mat_scterre'],
                format_func=lambda x: LABELS[x]
            )
        
        with col2:
            group_var = st.selectbox(
                "Variable de groupement",
                ['genre', 'region', 'type_ecole'],
                format_func=lambda x: LABELS[x]
            )
        
        # Calculate and display gaps
        gaps = calculate_performance_gaps(df, group_var, selected_subject)
        st.write(f"Écarts de Performance pour {LABELS[selected_subject]}")
        st.dataframe(gaps)
        
        # Additional statistics
        st.write("Statistiques Détaillées")
        detailed_stats = df.groupby(group_var)[selected_subject].agg([
            'count', 'mean', 'std', 'min', 'max'
        ]).round(2)
        st.dataframe(detailed_stats)