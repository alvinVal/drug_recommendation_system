import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import layout
from recommender import get_alternative_drugs
import pandas as pd

# Load the dataset
df = pd.read_csv("data/drugs.csv")

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server
app.layout = layout.create_layout()

# Callback to update suggestions based on user input
@app.callback(
    Output("suggestions-dropdown", "options"),
    Input("drug-input", "value"),
    State("suggestions-dropdown", "value")
)
def update_suggestions(input_value, selected_value):
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
    recommendation_links = [html.A(drug, href="#", id={'type': 'rec-link', 'index': drug}) for drug in recommendations]
    recommendation_list = [html.Li(link) for link in recommendation_links]
    drug_row = df[df["Drug"] == drug_name].iloc[0]
    therapeutic = f"Therapeutic Class: {drug_row['Therapeutic Class']}"
    side = f"Side Effects: {drug_row['Side Effects']}"
    return html.Ul(recommendation_list), therapeutic, side

# Callback to handle clicks on recommendation links
@app.callback(
    Output("drug-input", "value"),
    Input({'type': 'rec-link', 'index': dash.dependencies.ALL}, 'n_clicks'),
    State({'type': 'rec-link', 'index': dash.dependencies.ALL}, 'id')
)
def on_recommendation_click(n_clicks, ids):
    if not n_clicks or all(click is None for click in n_clicks):
        return dash.no_update
    clicked_id = [id['index'] for i, id in enumerate(ids) if n_clicks[i]]
    return clicked_id[0] if clicked_id else dash.no_update

if __name__ == "__main__":
    app.run_server(debug=True)
