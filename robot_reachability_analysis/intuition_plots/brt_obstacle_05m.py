import matplotlib.pyplot as plt
import numpy as np
import os

obstacle_center = (0, 0)
obstacle_radius = 0.5

fig, ax = plt.subplots(figsize=(6, 6))

circle = plt.Circle(obstacle_center, obstacle_radius, color="red", alpha=0.5, label="Obstacle (r=0.5)")
ax.add_artist(circle)
ax.plot(0, 0, "ko") 

ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect("equal")
ax.set_xlabel("$p_x$")
ax.set_ylabel("$p_y$")
ax.set_title("BRT for Obstacle Avoidance ($t=0,0.5,1$ s)")
ax.legend()

output_path = "../assets/brt_obstacle_05m.png"
plt.savefig(output_path, bbox_inches="tight")
plt.close()
