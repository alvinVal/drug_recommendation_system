import dash
from dash import html, dcc, callback_context
from dash.dependencies import Input, Output, State
import layout  # Import layout module
from recommender import get_alternative_drugs  # Import recommender function
import pandas as pd

# Load the dataset
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
    suggestions = df[df['Drug'].str.contains(input_value, case=False, na=False)]['Drug'].unique()
    return [{"label": drug, "value": drug} for drug in suggestions]

# Callback to update input field when a suggestion is selected
@app.callback(
    Output("drug-input", "value"),
    Input("suggestions-dropdown", "value")
)
def update_input(selected_suggestion):
    return selected_suggestion if selected_suggestion else ""

# Callback to update recommendations and drug details
@app.callback(
    [Output("output-container", "children"),
     Output("therapeutic-effects", "children"),
     Output("side-effects", "children")],
    Input("drug-input", "value")
)
def update_recommendations_and_details(drug_name):
    if not drug_name:
        return "Please enter a drug name.", "No details available.", "No details available."
    
    recommendations = get_alternative_drugs(drug_name, criteria="therapeutic effects")
    if recommendations and recommendations[0] == "Drug not found in database.":
        return "Drug not found in database.", "No details available.", "No details available."
    
    recommendation_links = [html.A(drug, href="#", id={"type": "rec-link", "index": drug}, style={"cursor": "pointer", "color": "blue", "textDecoration": "underline"}) for drug in recommendations]
    recommendation_list = [html.Li(link) for link in recommendation_links]
    
    drug_row = df[df["Drug"] == drug_name].iloc[0]
    therapeutic = f"Therapeutic Class: {drug_row['Therapeutic Class']}"
    side = f"Side Effects: {drug_row['Side Effects']}"
    
    return html.Ul(recommendation_list), therapeutic, side

# Callback to handle clicks on recommendation links
@app.callback(
    Output("drug-input", "value"),
    Input("output-container", "children"),
    State("drug-input", "value")
)
def on_recommendation_click(children, current_input):
    ctx = callback_context
    if not ctx.triggered:
        return current_input
    
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if "rec-link" in trigger_id:
        return trigger_id["index"]
    return current_input

if __name__ == "__main__":
    app.run_server(debug=True)
