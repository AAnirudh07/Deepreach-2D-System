import matplotlib.pyplot as plt
import numpy as np
import os

# Parameters
v = 1
r_o = 0.5
times = [0, 0.5, 1.0]

for T in times:
    safe_radius = v * T + r_o

    fig, ax = plt.subplots(figsize=(6, 6))

    unsafe_circle = plt.Circle((0, 0), safe_radius, color="red", alpha=0.5, label=f"Unsafe Region (r={safe_radius:.2f})")
    ax.add_artist(unsafe_circle)
    ax.plot(0, 0, "ko")

    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect("equal")
    ax.set_xlabel("$p_x$")
    ax.set_ylabel("$p_y$")
    ax.set_title(f"Safe Set for Obstacle Avoidance ($t={T}$ s)")
    ax.legend()

    filename = f"../assets/safeset_t{str(T).replace(".", "")}.png"
    plt.savefig(filename, bbox_inches="tight")
    plt.close()
