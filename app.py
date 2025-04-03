import dash
from dash import html, callback_context, no_update
from dash.dependencies import Input, Output, State, ALL
import dash_bootstrap_components as dbc
import layout
from recommender import get_alternative_drugs
import pandas as pd
import json

df = pd.read_csv("data/drugs.csv")
df["Drug"] = df["Drug"].str.lower()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.layout = layout.create_layout()

# Callback for recommendations and details
@app.callback(
    [Output("output-container", "children"),
     Output("recommended-drugs", "children"),
     Output("therapeutic-effects", "children"),
     Output("side-effects", "children")],
    Input("drug-input", "value")
)
def update_recommendations(drug_name):
    if not drug_name:
        return "Please enter a drug name.", [], "No details available.", "No details available."
    
    drug_lower = drug_name.lower()
    recommendations = get_alternative_drugs(drug_lower, "therapeutic effects")
    
    if not recommendations or recommendations[0] == "Drug not found in database.":
        return "Drug not found in database.", [], "No details available.", "No details available."
    
    # Create buttons for recommendations
    buttons = [
        dbc.Button(
            drug,
            id={'type': 'recommendation-button', 'index': drug},
            className="m-1",
            color="primary"
        ) for drug in recommendations
    ]
    
    # Get drug details
    drug_row = df[df["Drug"] == drug_lower]
    if drug_row.empty:
        return "Drug not found in database.", [], "No details available.", "No details available."
    
    drug_data = drug_row.iloc[0]
    therapeutic = f"Therapeutic Class: {drug_data.get('Therapeutic Class', 'N/A')}"
    side_effects = f"Side Effects: {drug_data.get('Side Effects', 'N/A')}"
    
    return "", buttons, therapeutic, side_effects

# Callback to update input when recommendation buttons are clicked
@app.callback(
    Output("drug-input", "value"),
    Input({'type': 'recommendation-button', 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True
)
def update_input(n_clicks):
    ctx = callback_context
    if not ctx.triggered:
        return no_update
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    drug_name = json.loads(button_id)['index']
    return drug_name

if __name__ == "__main__":
    app.run(debug=True)