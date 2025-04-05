from dash import Dash, html, dcc, callback_context, no_update
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
import layout
from recommender import get_alternative_drugs, get_drug_details, get_price_range
import pandas as pd

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.layout = layout.create_layout()

@app.callback(
    [Output("output-container", "children"),
     Output("therapeutic-class", "children"),
     Output("chemical-action-class", "children"),
     Output("therapeutic-uses", "children"),
     Output("side-effects", "children"),
     Output("side-effects-checklist", "options"),
     Output("price-range-slider", "min"),
     Output("price-range-slider", "max"),
     Output("price-range-slider", "marks"),
     Output("current-drug-price", "children"),
     Output("recommended-drugs", "children")],
    [Input("drug-input", "value"),
     Input("side-effects-checklist", "value"),
     Input("price-range-slider", "value"),
     Input("price-filter-toggle", "value")],
    prevent_initial_call=True
)
def update_all(drug_name, excluded_effects, price_range, price_filter_enabled):
    # Price range setup
    price_min, price_max = get_price_range()
    price_min = int(float(price_min))
    price_max = int(float(price_max))
    step_size = max(1, (price_max - price_min) // 4)
    marks = {i: str(i) for i in range(price_min, price_max + 1, step_size)}

    if not drug_name:
        return ["Please enter a drug name.", "No data", "No data", "No data", "No data", [],
                price_min, price_max, marks, "", []]

    drug_details = get_drug_details(drug_name.lower().strip())
    if drug_details is None:
        return ["Drug not found", "No data", "No data", "No data", "No data", [],
                price_min, price_max, marks, "Price info not available", []]

    # Process drug details
    therapeutic_class = (drug_details['Therapeutic Class'] 
                         if pd.notna(drug_details['Therapeutic Class'])
                         else "N/A")
    
    chemical_class = (drug_details['Chemical Class'] 
                      if pd.notna(drug_details['Chemical Class']) 
                      else "N/A")
    action_class = (drug_details['Action Class'] 
                    if pd.notna(drug_details['Action Class']) 
                    else "N/A")
    chem_action = html.Div([
        html.P(f"Chemical: {chemical_class}"),
        html.P(f"Action: {action_class}")
    ])
    
    therapeutic_uses = (drug_details['uses_features'] 
                        if pd.notna(drug_details['uses_features']) 
                        else "N/A")
    
    side_effects = (drug_details['side_effect_features'] 
                    if pd.notna(drug_details['side_effect_features']) 
                    else "N/A")
    effects = [e.strip() for e in str(side_effects).split(',') if e.strip()]
    side_effect_options = [{'label': eff, 'value': eff} for eff in effects]
    
    # Price display with red text
    price = drug_details['Price']
    price_display = (
        "Price information not available" 
        if price == -1 
        else html.Span([
            "Price: ",
            html.Span(
                f"₱{price:,.2f}",
                style={'color': 'red', 'fontWeight': 'bolder', 'fontSize': '1.2rem'}
            )
        ])
    )

    # Recommendations using the provided filters
    active_price_range = price_range if price_filter_enabled else None
    recommendations = get_alternative_drugs(drug_name, active_price_range, excluded_effects)
    
    if not recommendations:
        # If no recommendations and price filter is enabled, suggest turning it off.
        if price_filter_enabled:
            rec_children = [html.Div("No alternatives found with these filters. Consider turning off the price filter to see more options.", className="text-center")]
        else:
            rec_children = [html.Div("No alternatives found with these filters.", className="text-center")]
    else:
        rec_children = []
        for drug, similarity in recommendations:
            if drug.lower() == drug_name.lower():
                continue
            rec_children.append(
                dbc.Button(
                    drug.capitalize(),
                    id={'type': 'recommendation-button', 'index': drug},
                    className="m-1",
                    color="primary",
                    n_clicks=0,
                )
            )
            rec_children.append(
                dbc.Tooltip(
                    f"Similarity: {similarity:.2f}",
                    target={'type': 'recommendation-button', 'index': drug},
                )
            )

    return [
        "",
        therapeutic_class,
        chem_action,
        therapeutic_uses,
        ", ".join(effects) if effects else "No side effects reported",
        side_effect_options,
        price_min,
        price_max,
        marks,
        price_display,
        rec_children
    ]

@app.callback(
    [Output("price-range-slider", "disabled"),
     Output("price-filter-col", "style")],
    [Input("price-filter-toggle", "value")]
)
def toggle_price_filter(enable_filter):
    if not enable_filter:
        return True, {'opacity': 0.5}  # Only visually dim the slider
    return False, {'opacity': 1}

@app.callback(
    Output("drug-input", "value"),
    [Input({'type': 'recommendation-button', 'index': ALL}, 'n_clicks')],
    [State({'type': 'recommendation-button', 'index': ALL}, "id")]
)
def update_input(n_clicks, button_ids):
    ctx = callback_context
    if not ctx.triggered:
        return no_update
    
    clicked_idx = next((i for i, n in enumerate(n_clicks) if n), None)
    return button_ids[clicked_idx]['index'] if clicked_idx is not None else no_update

# New callback to toggle visibility of the entire results section (suggestions, filters, drug info)
@app.callback(
    Output("results-section", "style"),
    [Input("drug-input", "value")]
)
def toggle_results_section(drug_name):
    if drug_name and (get_drug_details(drug_name.lower().strip()) is not None):
         return {"display": "block"}
    else:
         return {"display": "none"}

if __name__ == "__main__":
    app.run(debug=True)