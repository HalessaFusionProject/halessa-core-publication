# Create a lightweight Jupyter notebook for harmonic field sweep visualization
from pathlib import Path
from nbformat import v4 as nbf

nb = nbf.new_notebook()

# Cells: Setup, Load Field, Layer Sweep, Interactive Viewer
cells = [
    nbf.new_markdown_cell("# Harmonic Field Sweep Notebook\nVisualize 3D Harmonic Overlay Field Layers"),
    
    nbf.new_code_cell("""
import numpy as np
import matplotlib.pyplot as plt

# Load normalized harmonic overlay (fallback to Q sweep if needed)
try:
    q_overlay = np.load("Q_Harmonic_Overlay_Full.npy")
except:
    q_overlay = np.load("Q_total_field_sweep.npy")
    q_gradient = np.gradient(q_overlay)
    q_overlay = np.sqrt(sum(g**2 for g in q_gradient))
    q_overlay /= np.max(q_overlay)
print(f"Loaded shape: {q_overlay.shape}")
"""),

    nbf.new_code_cell("""
# Visualize a specific layer slice
def plot_layer(z=0):
    plt.figure(figsize=(8, 6))
    plt.imshow(q_overlay[z], cmap='plasma', origin='lower')
    plt.title(f"Harmonic Field – Layer {z}")
    plt.colorbar(label='Magnitude')
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()

plot_layer(0)  # Default layer
"""),

    nbf.new_code_cell("""
# Optional: Interactively scroll through layers
import ipywidgets as widgets
widgets.interact(plot_layer, z=widgets.IntSlider(min=0, max=q_overlay.shape[0]-1, step=1, value=0))
""")
]

nb.cells.extend(cells)

# Save to file
notebook_path = Path(__file__).with_name("Harmonic_Field_Sweep.ipynb")

with open(notebook_path, "w") as f:
    f.write(nbf.writes(nb))
