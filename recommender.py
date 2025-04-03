import pandas as pd

# Load the dataset
df = pd.read_csv("data/drugs.csv")
df["Drug Name"] = df["Drug Name"].astype(str).str.lower()

def get_alternative_drugs(drug_name, criteria="therapeutic effects", selected_side_effects=None, price_range=None):
    """Returns a list of alternative drugs based on the given criteria."""
    
    drug_name = drug_name.lower()
    if drug_name not in df["Drug Name"].values:
        return ["Drug not found in database."]

    drug_row = df[df["Drug Name"] == drug_name].iloc[0]

    if criteria == "therapeutic effects":
        key = "Therapeutic Class"
    elif criteria == "side effects":
        key = "Side Effects"
    else:
        return ["Invalid criteria."]

    if pd.isna(drug_row[key]):
        return ["No alternatives found based on this criterion."]

    # Get base recommendations
    similar_drugs = df[df[key] == drug_row[key]].copy()
    
    # Filter by selected side effects if any
    if selected_side_effects:
        side_effect_cols = [col for col in df.columns if col.startswith('SideEffect')]
        mask = similar_drugs[side_effect_cols].apply(
            lambda row: not any(str(effect).lower() in [str(x).lower() for x in row.values if x] 
                        for effect in selected_side_effects), 
            axis=1
        )
        similar_drugs = similar_drugs[mask]
    
    # Filter by price range if specified
    if price_range:
        min_price, max_price = price_range
        similar_drugs = similar_drugs[
            (similar_drugs['Price'] >= min_price) & 
            (similar_drugs['Price'] <= max_price)
        ]
    
    # Remove the queried drug and format results
    similar_drugs = similar_drugs[similar_drugs['Drug Name'] != drug_name]
    results = similar_drugs['Drug Name'].unique().tolist()
    
    return results if results else ["No alternatives found."]

def get_drug_side_effects(drug_name):
    """Returns a list of side effects for a given drug"""
    drug_name = drug_name.lower()
    if drug_name not in df["Drug Name"].values:
        return []
    
    drug_row = df[df["Drug Name"] == drug_name].iloc[0]
    side_effects = [str(effect) for effect in drug_row.filter(like='SideEffect').dropna().unique() 
                   if effect and str(effect) != 'nan']
    return side_effects