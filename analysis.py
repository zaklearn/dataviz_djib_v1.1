import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder

def analyze_demographics(df):
    """Analyze demographic statistics."""
    stats = {
        'total': len(df),
        'by_gender': df['genre'].value_counts(),
        'by_region': df['region'].value_counts(),
        'by_milieu': df['milieu'].value_counts(),
        'by_school_type': df['type_ecole'].value_counts(),
        'age_distribution': df['age'].value_counts().sort_index()
    }
    return stats

def analyze_results(df):
    """Analyze examination results."""
    results = {
        'total_admis': df[df['result'] == 'ADMIS'].shape[0],
        'total_ajournes': df[df['result'] == 'AJOURNE'].shape[0],
        'admis_by_gender': pd.crosstab(df['genre'], df['result']),
        'admis_by_region': pd.crosstab(df['region'], df['result']),
        'admis_by_milieu': pd.crosstab(df['milieu'], df['result']),
        'success_rate': (df['result'] == 'ADMIS').mean()
    }
    return results

def analyze_subject_performance(df):
    """Analyze performance by subject."""
    subjects = ['mat_fr', 'mat_math', 'mat_phychi', 'mat_sc', 'mat_scterre']
    
    performance = {
        'stats': {subj: df[subj].describe() for subj in subjects},
        'zero_scores': {subj: (df[subj] == 0).sum() for subj in subjects},
        'pass_rates': {subj: (df[subj] >= 10).mean() for subj in subjects},
        'averages': {subj: df[subj].mean() for subj in subjects}
    }
    return performance

def calculate_performance_gaps(df, column, subject):
    """Calculate performance gaps between different groups."""
    gaps = df.groupby(column)[subject].agg(['mean', 'std', 'count'])
    gaps['ci'] = 1.96 * gaps['std'] / np.sqrt(gaps['count'])
    return gaps

def chi_square_test(df, var1, var2):
    """Perform chi-square test of independence."""
    contingency_table = pd.crosstab(df[var1], df[var2])
    chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
    return {
        'chi2': chi2,
        'p_value': p_value,
        'dof': dof,
        'contingency_table': contingency_table,
        'expected': expected
    }

def perform_regression_analysis(df, target_variable, features):
    """Perform multiple regression analysis."""
    # Prepare features
    X = pd.get_dummies(df[features], drop_first=True)
    y = df[target_variable]
    
    # Fit regression
    model = LinearRegression()
    model.fit(X, y)
    
    # Prepare results
    results = {
        'coefficients': dict(zip(X.columns, model.coef_)),
        'intercept': model.intercept_,
        'r2_score': model.score(X, y)
    }
    return results

def calculate_icc(df, subjects):
    """Calculate Intraclass Correlation Coefficient."""
    scores = df[subjects].values
    n = len(subjects)
    icc = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            if i != j:
                icc[i,j] = stats.pearsonr(scores[:,i], scores[:,j])[0]
            else:
                icc[i,j] = 1.0
                
    return pd.DataFrame(icc, index=subjects, columns=subjects)