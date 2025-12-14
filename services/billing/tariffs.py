def calculate_cost(start_meter, end_meter):
    # Simple fixed rate for now
    kwh = (end_meter - start_meter) / 1000.0 # Assuming meter is in Wh
    rate = 2.5 # Currency per kWh
    return kwh * rate
