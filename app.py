import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import layout  # Import layout module
from recommender import get_alternative_drugs  # Import recommender function
import pandas as pd

# Load the dataset for suggestions and details (assumes data/drugs.csv exists)
df = pd.read_csv("data/drugs.csv")

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server  # Required for Render deployment
app.layout = layout.create_layout()

# Callback to update suggestions based on user input
@app.callback(
    Output("suggestions-dropdown", "options"),
    Input("drug-input", "value")
)
def update_suggestions(input_value):
    if not input_value:
        return []
    # Filter drugs whose names contain the input text (case-insensitive)
    suggestions = df[df['Drug'].str.contains(input_value, case=False, na=False)]['Drug'].unique()
    return [{"label": drug, "value": drug} for drug in suggestions]

# Callback to update the recommended alternative drugs.
# If a suggestion is selected, it takes precedence over the typed text.
@app.callback(
    Output("output-container", "children"),
    [Input("drug-input", "value"),
     Input("suggestions-dropdown", "value")]
)
def update_recommendations(input_value, selected_suggestion):
    drug_name = selected_suggestion if selected_suggestion else input_value
    if not drug_name:
        return "Please enter a drug name."
    recommendations = get_alternative_drugs(drug_name, criteria="therapeutic effects")
    if recommendations and recommendations[0] == "Drug not found in database.":
        return "Drug not found in database."
    return html.Div([
        html.H4("Suggested Alternative Drugs:", style={'marginBottom': '10px'}),
        html.Ul([html.Li(drug) for drug in recommendations])
    ])

# Callback to display therapeutic effects and side effects of the input/suggested drug
@app.callback(
    [Output("therapeutic-effects", "children"),
     Output("side-effects", "children")],
    Input("drug-input", "value")
)
def update_drug_details(drug_name):
    if not drug_name or drug_name not in df["Drug"].values:
        return "No details available.", "No details available."
    drug_row = df[df["Drug"] == drug_name].iloc[0]
    therapeutic = f"Therapeutic Class: {drug_row['Therapeutic Class']}"
    side = f"Side Effects: {drug_row['Side Effects']}"
    return therapeutic, side

if __name__ == "__main__":
    app.run_server(debug=True)
