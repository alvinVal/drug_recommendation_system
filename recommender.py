import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load and preprocess data
df = pd.read_csv("data/drugs.csv")
df['name'] = df['name'].str.lower().str.strip()
df['uses_features'] = df['uses_features'].fillna('').astype(str)
df['side_effect_features'] = df['side_effect_features'].fillna('').astype(str)

# Create TF-IDF matrix
tfidf = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
tfidf_matrix = tfidf.fit_transform(df['uses_features'] + ' ' + df['side_effect_features'])
cosine_sim = cosine_similarity(tfidf_matrix)

def get_drug_details(drug_name):
    """Get detailed information for a specific drug (exact match only)"""
    try:
        drug_name = drug_name.lower().strip()
        exact_match = df[df['name'] == drug_name]
        if not exact_match.empty:
            return exact_match.iloc[0]
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def get_alternative_drugs(drug_name, price_range=None, excluded_side_effects=None):
    """Get recommendations with dynamic filtering. If filters yield no results,
    fallback to the top 3 alternatives based solely on cosine similarity."""
    try:
        drug_name = drug_name.lower().strip()
        idx = df[df['name'] == drug_name].index[0]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get top 50 candidates (excluding self)
        top_indices = [i[0] for i in sim_scores[1:51]]
        recommendations = df.iloc[top_indices].copy()
        recommendations['similarity'] = [i[1] for i in sim_scores[1:51]]
        
        # Apply price filter if enabled
        if price_range:
            min_price, max_price = price_range
            recommendations = recommendations[
                (recommendations['Price'] >= min_price) & 
                (recommendations['Price'] <= max_price) &
                (recommendations['Price'] != -1)
            ]
        
        # Apply side effects filter if any are excluded
        if excluded_side_effects:
            mask = ~recommendations['side_effect_features'].str.contains(
                '|'.join(excluded_side_effects), case=False, na=False
            )
            recommendations = recommendations[mask]
        
        filtered_recs = recommendations[['name', 'similarity']].head(3).values.tolist()
        if not filtered_recs:
            # Fallback: return the top 3 alternatives ignoring filters
            fallback = []
            for i, sim in sim_scores[1:]:
                candidate = df.iloc[i]
                if candidate['name'] != drug_name:
                    fallback.append([candidate['name'], sim])
                if len(fallback) == 3:
                    break
            return fallback
        return filtered_recs
    except Exception as e:
        print(f"Error: {str(e)}")
        return []

def get_price_range():
    """Get min and max price from dataset (excludes -1)"""
    valid_prices = df[df['Price'] != -1]['Price']
    return (valid_prices.min(), valid_prices.max()) if not valid_prices.empty else (0, 2000)
