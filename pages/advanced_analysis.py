import streamlit as st
from analysis import chi_square_test, perform_regression_analysis
from visualization import create_regression_plot
from config import LABELS
import pandas as pd

def create_advanced_analysis_page():
    st.title('Analyses Avancées')
    
    df = st.session_state.data
    
    # Create tabs for different analyses
    tab1, tab2 = st.tabs(["Tests Statistiques", "Analyse de Régression"])
    
    with tab1:
        st.subheader("Tests d'Indépendance (Khi-deux)")
        
        # Select variables for chi-square test
        col1, col2 = st.columns(2)
        with col1:
            var1 = st.selectbox(
                'Variable 1',
                ['genre', 'type_ecole'],#, 'milieu'
                format_func=lambda x: LABELS[x]
            )
        with col2:
            var2 = st.selectbox(
                'Variable 2',
                ['result', 'mention'],
                format_func=lambda x: LABELS[x]
            )
        
        # Perform chi-square test
        chi2_results = chi_square_test(df, var1, var2)
        
        # Display results
        st.write("Résultats du Test Khi-deux")
        st.write(f"Statistique χ²: {chi2_results['chi2']:.2f}")
        st.write(f"p-value: {chi2_results['p_value']:.4f}")
        st.write(f"Degrés de liberté: {chi2_results['dof']}")
        
        # Display contingency table
        st.write("Tableau de Contingence")
        st.dataframe(chi2_results['contingency_table'])
        
        # Interpretation
        if chi2_results['p_value'] < 0.05:
            st.info("Il existe une relation significative entre les variables (p < 0.05)")
        else:
            st.info("Pas de relation significative entre les variables (p >= 0.05)")
    
    with tab2:
        st.subheader("Analyse de Régression Multiple")
        
        # Select target variable and features
        target_var = st.selectbox(
            "Variable Dépendante",
            ['mat_fr', 'mat_math', 'mat_phychi', 'mat_sc', 'mat_scterre'],
            format_func=lambda x: LABELS[x]
        )
        
        features = st.multiselect(
            "Variables Indépendantes",
            ['genre', 'age', 'type_ecole'],#, 'region', 'milieu'
            default=['genre', 'age', 'type_ecole'],
            format_func=lambda x: LABELS.get(x, x)
        )
        
        if features:
            # Perform regression analysis
            regression_results = perform_regression_analysis(df, target_var, features)
            
            # Display results
            st.write("Résultats de la Régression")
            st.write(f"R² Score: {regression_results['r2_score']:.4f}")
            
            # Display coefficients
            coef_fig = create_regression_plot(regression_results)
            st.plotly_chart(coef_fig, use_container_width=True)
            
            # Detailed coefficients table
            st.write("Coefficients de Régression")
            coef_df = pd.DataFrame({
                'Variable': list(regression_results['coefficients'].keys()),
                'Coefficient': list(regression_results['coefficients'].values())
            })
            st.dataframe(coef_df)
        else:
            st.warning("Veuillez sélectionner au moins une variable indépendante")