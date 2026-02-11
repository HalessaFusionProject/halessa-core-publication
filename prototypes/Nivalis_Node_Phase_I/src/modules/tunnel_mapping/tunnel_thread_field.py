"""
Tunnel Node Threading Module

This module defines the logic for generating vector fields based on divergence pressure index 𝒟(P).
It traces potential corridor flows for tunnel node mapping across stable, compressive, and divergent zones.

Based on:
    - pcl_divergence_dynamics.md
    - QESR_divergence_trace_map.png
    - QESR_tunnel_thread_vector_map.png
"""

import numpy as np

def compute_divergence_index(X, Y, lock_integrity=None):
    R = np.sqrt(X**2 + Y**2)
    Theta = np.arctan2(Y, X)
    grad_sigma = np.abs(np.cos(6 * Theta)) * np.exp(-R**2)
    grad_sigma_t = np.abs(np.sin(3 * np.pi * R)) * np.exp(-2 * R)
    if lock_integrity is None:
        lock_integrity = np.exp(-(R / 0.7)**2)
    D_P = 1.0 * grad_sigma + 0.7 * grad_sigma_t + 0.9 * (1 - lock_integrity)
    return D_P

def classify_nodes(D_P, T_anchor=0.6, T_diverge=1.1):
    zones = np.zeros_like(D_P)
    zones[D_P < T_anchor] = 0
    zones[(D_P >= T_anchor) & (D_P < T_diverge)] = 1
    zones[D_P >= T_diverge] = 2
    return zones  # 0: lock, 1: compress, 2: diverge

def compute_threading_vectors(D_P):
    dD_dx, dD_dy = np.gradient(D_P)
    magnitude = np.sqrt(dD_dx**2 + dD_dy**2) + 1e-5
    vx = -dD_dx / magnitude
    vy = -dD_dy / magnitude
    return vx, vy

def generate_field(x_range=(-2, 2), y_range=(-2, 2), resolution=300):
    x = np.linspace(*x_range, resolution)
    y = np.linspace(*y_range, resolution)
    X, Y = np.meshgrid(x, y)
    D_P = compute_divergence_index(X, Y)
    zones = classify_nodes(D_P)
    vx, vy = compute_threading_vectors(D_P)
    return X, Y, D_P, zones, vx, vy
