
import numpy as np
import matplotlib.pyplot as plt

# Try loading overlay, fallback to computing it
try:
    q_overlay = np.load("Q_Harmonic_Overlay_Full.npy")
except FileNotFoundError:
    q_field = np.load("Q_total_field_sweep.npy")
    q_gradient = np.gradient(q_field)
    q_overlay = np.sqrt(sum(g**2 for g in q_gradient))
    q_overlay /= np.max(q_overlay)
    print("[INFO] Overlay recomputed from raw field.")

def plot_layer(z=0):
    plt.figure(figsize=(8, 6))
    plt.imshow(q_overlay[z], cmap='plasma', origin='lower')
    plt.title(f"Harmonic Field – Layer {z}")
    plt.colorbar(label='Magnitude')
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()

# Default layer plot
if __name__ == "__main__":
    plot_layer(0)
