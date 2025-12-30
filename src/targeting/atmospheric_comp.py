"""
Atmospheric compensation module for Project HELIOS.
Analyzes sensor data from atmospheric turbulence and generates correction profiles.
"""

import csv
import math
from typing import Dict, List, Tuple


def read_sensor_data(filepath: str) -> List[Dict[str, float]]:
    """
    Read atmospheric sensor CSV file.
    Expected columns: timestamp, temperature, pressure, humidity, wind_speed, turbulence_strength
    Returns list of dictionaries with numeric values.
    """
    data = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert numeric fields
            numeric_row = {}
            for key, value in row.items():
                if key == 'timestamp':
                    numeric_row[key] = value
                else:
                    try:
                        numeric_row[key] = float(value)
                    except ValueError:
                        numeric_row[key] = 0.0
            data.append(numeric_row)
    return data


def calculate_correction_profile(sensor_data_path: str) -> Dict[str, float]:
    """
    Analyze atmospheric sensor data and compute correction parameters.
    
    Parameters:
        sensor_data_path: Path to the CSV file containing sensor readings.
    
    Returns:
        Dictionary containing correction parameters:
            - 'turbulence_mean': average turbulence strength
            - 'turbulence_std': standard deviation of turbulence
            - 'correction_gain': gain factor for adaptive optics (based on turbulence)
            - 'zernike_coeffs': list of placeholder Zernike coefficients (as dict)
    """
    data = read_sensor_data(sensor_data_path)
    if not data:
        return {}
    
    # Extract turbulence strength values
    turb = [row['turbulence_strength'] for row in data]
    n = len(turb)
    mean_turb = sum(turb) / n
    variance = sum((x - mean_turb) ** 2 for x in turb) / n
    std_turb = math.sqrt(variance)
    
    # Compute correction gain (inverse relationship with turbulence)
    # Simple heuristic: higher turbulence requires stronger correction
    gain = 1.0 / (mean_turb + 0.1)  # avoid division by zero
    
    # Placeholder Zernike coefficients (first 5 modes)
    zernike_coeffs = {
        'tip': 0.01 * mean_turb,
        'tilt': 0.02 * mean_turb,
        'defocus': 0.005 * std_turb,
        'astigmatism_x': 0.003 * std_turb,
        'astigmatism_y': 0.003 * std_turb
    }
    
    return {
        'turbulence_mean': mean_turb,
        'turbulence_std': std_turb,
        'correction_gain': gain,
        'zernike_coeffs': zernike_coeffs
    }


# Example usage for testing
if __name__ == '__main__':
    # Test with sample data
    profile = calculate_correction_profile('../../data/test-flight-007/atmospheric_sensors.csv')
    print('Correction profile:', profile)
