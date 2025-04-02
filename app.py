import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import layout  # Importing the layout module
from recommender import get_alternative_drugs  # Importing recommender function

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server # Required for Render deployment

# Set layout from external module
app.layout = layout.create_layout()

# Define callback to update recommendations
@app.callback(
    Output("output-container", "children"),
    Input("drug-input", "value"),
    Input("criteria-dropdown", "value")
)
def update_recommendations(drug_name, criteria):
    if not drug_name:
        return "Please enter a drug name."
    recommendations = get_alternative_drugs(drug_name, criteria)
    return html.Ul([html.Li(drug) for drug in recommendations])

# Run the app
if __name__ == "__main__":
    app.run(debug=True)