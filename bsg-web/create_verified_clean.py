import pandas as pd
import numpy as np
import os

def create_verified_clean():
    if not os.path.exists('scenarios'):
        os.makedirs('scenarios')
        
    # Load verified normal points
    df = pd.read_csv('found_normals.csv')
    
    # Filter for Idle-like and Charging-like
    idle_rows = df[df['current'] < 2.0]
    charging_rows = df[df['current'] >= 2.0]
    
    if len(idle_rows) < 5 or len(charging_rows) < 5:
        print("Not enough diversity in verified normals, using random sampling from all normals.")
        # Fallback: just use all
        idle_sample = df.sample(30, replace=True)
        charging_sample = df.sample(30, replace=True)
        idle_sample_2 = df.sample(30, replace=True)
    else:
        # Sample with replacement to get enough rows
        idle_sample = idle_rows.sample(30, replace=True)
        charging_sample = charging_rows.sample(40, replace=True)
        idle_sample_2 = idle_rows.sample(20, replace=True)

    # Combine
    final_df = pd.concat([idle_sample, charging_sample, idle_sample_2], ignore_index=True)
    
    # Rename columns to match system expectation if needed
    # System expects: 
    # latency_ms, integrity_flag, token_visible, voltage_v, current_a, temperature_c, meter_kwh, cost, ip_changed
    # found_normals.csv has:
    # latency, integrity, token, voltage, current, temp, meter, cost, ip
    
    final_df.columns = ['latency_ms', 'integrity_flag', 'token_visible', 'voltage_v', 'current_a', 
                        'temperature_c', 'meter_kwh', 'cost', 'ip_changed']

    # Add 3 metadata columns
    final_df['command_code'] = 1
    final_df['user_role_code'] = 1
    final_df['status_code'] = 1
    
    output_path = 'scenarios/Scenario_Clean_Verified.csv'
    final_df.to_csv(output_path, index=False, header=False)
    print(f"Created {output_path} with {len(final_df)} verified green rows.")

if __name__ == "__main__":
    create_verified_clean()
