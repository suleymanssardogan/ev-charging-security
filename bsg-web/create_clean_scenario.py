import pandas as pd
import numpy as np
import os

def generate_clean_scenario():
    if not os.path.exists('scenarios'):
        os.makedirs('scenarios')

    # Define columns based on prep_scenarios.py
    # 0: latency_ms
    # 1: integrity_flag
    # 2: token_visible
    # 3: voltage_v
    # 4: current_a
    # 5: temperature_c
    # 6: meter_kwh
    # 7: cost
    # 8: ip_changed
    # 9: command_code (Default 1)
    # 10: user_role_code (Default 1)
    # 11: status_code (Default 1)

    # Number of rows
    n_idle = 30
    n_charging = 30
    
    # Idle State (Safe)
    # Modeled after 'mapped_normal' in prep_scenarios.py
    idle_df = pd.DataFrame()
    idle_df['latency_ms'] = [10] * n_idle
    idle_df['integrity_flag'] = [0] * n_idle
    idle_df['token_visible'] = [0] * n_idle
    idle_df['voltage_v'] = np.random.normal(230.0, 0.1, n_idle) # Slight noise for realism
    idle_df['current_a'] = [0.0] * n_idle
    idle_df['temperature_c'] = np.random.normal(25.0, 0.1, n_idle)
    idle_df['meter_kwh'] = [0.0] * n_idle
    idle_df['cost'] = [0.0] * n_idle
    idle_df['ip_changed'] = [0] * n_idle
    # Metadata
    idle_df['command_code'] = 1
    idle_df['user_role_code'] = 1
    idle_df['status_code'] = 1

    # Charging State (Normal Operation)
    # Values based on map_price but kept "clean" (no cost mismatch)
    charging_df = pd.DataFrame()
    charging_df['latency_ms'] = [20] * n_charging
    charging_df['integrity_flag'] = [0] * n_charging # Keeping 0 as it was 'Tweaked to 0' for normal in prep_scenarios
    charging_df['token_visible'] = [0] * n_charging
    charging_df['voltage_v'] = np.random.normal(230.0, 0.5, n_charging) # Normal fluctuations
    charging_df['current_a'] = np.random.normal(16.0, 0.1, n_charging) # ~16A charging
    charging_df['temperature_c'] = np.linspace(25.0, 35.0, n_charging) # Warming up slightly
    charging_df['meter_kwh'] = np.linspace(0.0, 5.0, n_charging) # Energy increasing
    charging_df['cost'] = charging_df['meter_kwh'] * 0.5 # Consistent cost (e.g. 0.5 per kWh)
    charging_df['ip_changed'] = [0] * n_charging
    # Metadata
    charging_df['command_code'] = 1
    charging_df['user_role_code'] = 1
    charging_df['status_code'] = 1

    # Combine: Idle -> Charging -> Idle
    final_df = pd.concat([idle_df, charging_df, idle_df], ignore_index=True)
    
    output_path = 'scenarios/Scenario_Clean.csv'
    final_df.to_csv(output_path, index=False, header=False)
    print(f"Generated {output_path} with {len(final_df)} rows.")

if __name__ == "__main__":
    generate_clean_scenario()
