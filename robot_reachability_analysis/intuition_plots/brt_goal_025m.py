import matplotlib.pyplot as plt
import numpy as np
import os

# Parameters
v = 1  
r_g = 0.25  
times = [0, 0.5, 1.0]

for T in times:
    reach_radius = v * T + r_g

    fig, ax = plt.subplots(figsize=(6, 6))

    reachable_circle = plt.Circle((0, 0), reach_radius, color="red", alpha=0.5, label=f"Reachable Region (r={reach_radius:.2f})")
    ax.add_artist(reachable_circle)
    ax.plot(0, 0, "ko")

    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect("equal")
    ax.set_xlabel("$p_x$")
    ax.set_ylabel("$p_y$")
    ax.set_title(f"BRT for Goal Reachability ($t={T}$ s)")
    ax.legend()

    filename = f"../assets/goalreach_t{str(T).replace(".", "")}.png"
    plt.savefig(filename, bbox_inches="tight")
    plt.close()
