# recommender.py
import pandas as pd

# Load the dataset
df = pd.read_csv("data/drugs.csv")
df["Drug"] = df["Drug"].astype(str).str.lower()  # Normalize for case-insensitive matching

def get_alternative_drugs(drug_name, criteria="therapeutic effects"):
    """Returns a list of alternative drugs based on the given criteria."""
    
    # Ensure lowercase for consistent comparison
    drug_name = drug_name.lower()

    if drug_name not in df["Drug"].values:
        return ["Drug not found in database."]

    # Get the row for the input drug
    drug_row = df[df["Drug"] == drug_name].iloc[0]

    # Select the correct column for recommendations
    if criteria == "therapeutic effects":
        key = "Therapeutic Class"
    elif criteria == "side effects":
        key = "Side Effects"
    else:
        return ["Invalid criteria."]

    # Get similar drugs based on the selected criterion
    if pd.isna(drug_row[key]):
        return ["No alternatives found based on this criterion."]

    similar_drugs = df[df[key] == drug_row[key]]["Drug"].unique().tolist()

    # Remove the queried drug from recommendations
    similar_drugs = [drug for drug in similar_drugs if drug != drug_name]

    return similar_drugs if similar_drugs else ["No alternatives found."]
