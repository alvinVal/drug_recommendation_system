# New callback for disabling price controls
@app.callback(
    [Output("price-range-slider", "disabled"),
     Output("price-filter-col", "style")],
    Input("price-filter-toggle", "value")
)
def toggle_price_filter(enable_filter):
    if not enable_filter:
        return True, {'opacity': 0.5, 'pointerEvents': 'none'}
    return False, {'opacity': 1, 'pointerEvents': 'all'}