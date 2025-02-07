import plotly.express as px
import plotly.graph_objects as go
from config import COLORS, LABELS

def create_gender_chart(data):
    """Create pie chart for gender distribution."""
    fig = px.pie(
        values=data.values,
        names=data.index,
        title="Répartition par Genre",
        color_discrete_sequence=[COLORS['primary'], COLORS['secondary']]
    )
    return fig

def create_region_chart(data):
    """Create bar chart for regional distribution."""
    fig = px.bar(
        x=data.index,
        y=data.values,
        title="Répartition par Région",
        labels={'x': 'Région', 'y': 'Nombre d\'étudiants'},
        color_discrete_sequence=[COLORS['primary']]
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def create_performance_distribution(df, subject):
    """Create histogram for performance distribution."""
    fig = px.histogram(
        df,
        x=subject,
        title=f"Distribution des Notes - {LABELS[subject]}",
        nbins=20,
        color_discrete_sequence=[COLORS['primary']]
    )
    fig.update_layout(
        xaxis_title="Note",
        yaxis_title="Nombre d'étudiants"
    )
    return fig

def create_comparative_boxplot(df, subject, group_by):
    """Create box plot for comparative analysis."""
    fig = px.box(
        df,
        x=group_by,
        y=subject,
        title=f"Distribution des Notes par {LABELS[group_by]} - {LABELS[subject]}",
        color=group_by,
        color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['success']]
    )
    return fig

def create_heatmap(data):
    """Create heatmap for correlation matrix."""
    fig = go.Figure(data=go.Heatmap(
        z=data.values,
        x=data.columns,
        y=data.index,
        colorscale='RdBu',
        zmin=-1,
        zmax=1
    ))
    fig.update_layout(
        title="Matrice de Corrélation entre les Matières",
        xaxis_title="Matière",
        yaxis_title="Matière"
    )
    return fig

def create_success_rate_chart(data):
    """Create bar chart for success rates."""
    fig = px.bar(
        x=data.index,
        y=data.values,
        title="Taux de Réussite par Catégorie",
        labels={'x': 'Catégorie', 'y': 'Taux de Réussite (%)'},
        color_discrete_sequence=[COLORS['success']]
    )
    fig.update_layout(yaxis_range=[0, 100])
    return fig

def create_zero_score_analysis(data):
    """Create bar chart for zero score analysis."""
    fig = px.bar(
        x=list(data.keys()),
        y=list(data.values()),
        title="Analyse des Notes Zéro par Matière",
        labels={'x': 'Matière', 'y': 'Nombre de Notes Zéro'},
        color_discrete_sequence=[COLORS['warning']]
    )
    return fig

def create_regression_plot(results):
    """Create bar chart for regression coefficients."""
    fig = px.bar(
        x=list(results['coefficients'].keys()),
        y=list(results['coefficients'].values()),
        title="Coefficients de Régression",
        labels={'x': 'Variable', 'y': 'Coefficient'},
        color_discrete_sequence=[COLORS['primary']]
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def create_result_distribution_chart(stats):
    """
    Crée un graphique en secteurs montrant la distribution des résultats
    """
    labels = ['Admis(e)', 'Ajourné(e)']
    values = [stats['admis'], stats['ajourne']]
    
    fig = px.pie(
        values=values,
        names=labels,
        title="Distribution des Résultats",
        color_discrete_sequence=[COLORS['success'], COLORS['warning']]
    )
    
    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig