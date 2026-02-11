"""
tunnel_node_threading.py
-------------------------
This module extracts tunnel node threads based on Q-field gradient curls and Z-axis pressure troughs.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.ndimage import gaussian_filter
from scipy.interpolate import griddata

# Load Z-axis pressure trough data
def load_pressure_trough(file_path="data/fields/Q_Z_Pressure_Convergence_Trough.csv"):
    return pd.read_csv(file_path)

# Core processing: generate potential curl zones from trough map
def compute_pinch_zones(trough_df, threshold=0.85):
    normalized = (trough_df['pressure'].values - trough_df['pressure'].min()) / (trough_df['pressure'].max() - trough_df['pressure'].min())
    trough_df['pinch'] = normalized > threshold
    return trough_df

# Optional: visualize Z-plane convergence
def visualize_trough_pinch(trough_df):
    fig, ax = plt.subplots(figsize=(8, 6))
    scatter = ax.scatter(trough_df['x'], trough_df['y'], c=trough_df['pressure'], cmap='plasma', alpha=0.75)
    ax.set_title('Z-Pressure Field with Pinch Candidates')
    fig.colorbar(scatter, label='Pressure')
    pinch_points = trough_df[trough_df['pinch']]
    ax.scatter(pinch_points['x'], pinch_points['y'], color='cyan', label='Pinch Nodes', edgecolor='k')
    ax.legend()
    plt.show()

# Export vector intersections (placeholder logic)
def export_node_vector_map(pinch_df, output_path="data/vectors/tunnel_node_vectors.csv"):
    pinch_df[['x', 'y', 'z']].to_csv(output_path, index=False)

if __name__ == "__main__":
    df = load_pressure_trough()
    df = compute_pinch_zones(df)
    visualize_trough_pinch(df)
    export_node_vector_map(df[df['pinch']])
