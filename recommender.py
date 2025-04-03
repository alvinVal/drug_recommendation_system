# placeholder for recommender system
import pandas as pd

# Load drug dataset, sample file is in data/drugs.csv
df = pd.read_csv("data/drugs.csv")

def get_alternative_drugs(drug_name, criteria="therapeutic effects"):
    """
    Returns a list of alternative drugs based on the specified criteria.
    :param drug_name: Name of the drug to find alternatives for.
    :param criteria: Criteria for recommendations (e.g., 'therapeutic effects', 'side effects').
    :return: List of recommended alternative drugs.
    """
    if drug_name not in df["Drug"].values:
        return ["Drug not found in database."]
    
    # Find the therapeutic class of the given drug
    drug_row = df[df["Drug"] == drug_name]
    if criteria == "therapeutic effects":
        class_match = df[df["Therapeutic Class"] == drug_row["Therapeutic Class"].values[0]]
    elif criteria == "side effects":
        class_match = df[df["Side Effects"] == drug_row["Side Effects"].values[0]]
    else:
        class_match = df  # Default to all
    
    recommendations = class_match["Drug"].tolist()
    recommendations.remove(drug_name)  # Remove the input drug from recommendations
    
    return recommendations[:5]  # Return top 5 recommendations
