import streamlit as st
import sys
from pathlib import Path

# Add the project root directory to Python path
root_path = Path(__file__).parent
sys.path.append(str(root_path))

from config import PAGE_CONFIG
from pages.home import create_home_page
from pages.descriptive_stats import create_stats_page
from pages.performance import create_performance_page
from pages.advanced_analysis import create_advanced_analysis_page

# Configure the page
st.set_page_config(**PAGE_CONFIG)

# Create sidebar navigation
def main():


    # Titre de la navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Sélectionnez une page",
        ["Accueil", "Statistiques Descriptives", "Analyse des Performances", "Analyses Avancées"]
    )

    # Session state initialization
    if 'data' not in st.session_state:
        st.session_state.data = None

    # Page routing
    if page == "Accueil":
        create_home_page()
    elif page == "Statistiques Descriptives":
        if st.session_state.data is not None:
            create_stats_page()
        else:
            st.warning("Veuillez d'abord charger les données sur la page d'accueil.")
    elif page == "Analyse des Performances":
        if st.session_state.data is not None:
            create_performance_page()
        else:
            st.warning("Veuillez d'abord charger les données sur la page d'accueil.")
    elif page == "Analyses Avancées":
        if st.session_state.data is not None:
            create_advanced_analysis_page()
        else:
            st.warning("Veuillez d'abord charger les données sur la page d'accueil.")

# Pied de page fixe
st.sidebar.markdown(
    """
    <div style='position: fixed; bottom: 0; left: 0; width: 100%; background-color: white; padding: 10px; text-align: center; font-size: 12px;'>
        © 2025 HBNConsulting Ltd<br>All rights reserved
    </div>
    """,
    unsafe_allow_html=True
)

if __name__ == "__main__":
    main()
