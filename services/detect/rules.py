def check_rules(event, state):
    alerts = []
    action = event.get("action")
    payload = event.get("payload", {})
    charge_point_id = event.get("charge_point_id")
    
    # K1: Monotonicity
    if action == "MeterValues":
        connector_id = payload.get("connectorId")
        transaction_id = payload.get("transactionId")
        meter_values = payload.get("meterValue", [])
        
        for mv in meter_values:
            sampled_values = mv.get("sampledValue", [])
            for sv in sampled_values:
                if sv.get("measurand") == "Energy.Active.Import.Register" or sv.get("measurand") is None: # Default is Energy.Active.Import.Register
                    try:
                        value = float(sv.get("value"))
                        key = f"{charge_point_id}_{connector_id}"
                        
                        last_value = state.get(key)
                        if last_value is not None and value < last_value:
                            alerts.append({
                                "rule_id": "K1",
                                "severity": "HIGH",
                                "stationId": charge_point_id,
                                "transactionId": transaction_id,
                                "evidence": f"Value dropped from {last_value} to {value}",
                                "timestamp": mv.get("timestamp")
                            })
                        
                        state[key] = value
                    except (ValueError, TypeError):
                        pass

    return alerts
