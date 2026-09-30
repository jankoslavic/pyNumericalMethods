"""Sketch of the problem (sketch.png): ladder against a smooth wall with a person and forces."""

import numpy as np
import matplotlib.pyplot as plt

L = 4.0                       # length of the ladder [m]
theta = np.radians(65.0)      # angle of the ladder for the sketch [rad]
x_person = 2.6                # position of the person [m]

# points A (floor), B (wall), center of mass G and person P
A = np.array([L * np.cos(theta), 0.0])
B = np.array([0.0, L * np.sin(theta)])
direction = (B - A) / L
G = A + direction * L / 2
P = A + direction * x_person

fig, ax = plt.subplots(figsize=(6.4, 5.2))
ax.set_aspect("equal")
ax.axis("off")

# wall and floor with hatching
ax.plot([0, 0], [-0.2, 4.4], "k", lw=2)
ax.plot([-0.2, 3.2], [0, 0], "k", lw=2)
for y in np.arange(0.0, 4.4, 0.25):
    ax.plot([-0.25, 0], [y - 0.25, y], "k", lw=0.6)
for x in np.arange(0.0, 3.2, 0.25):
    ax.plot([x - 0.25, x], [-0.25, 0], "k", lw=0.6)

# ladder (two rails and rungs)
offset = np.array([-direction[1], direction[0]]) * 0.09
for sign in (-1, 1):
    start = A + sign * offset
    end = B + sign * offset
    ax.plot([start[0], end[0]], [start[1], end[1]], color="tab:brown", lw=3)
for s in np.linspace(0.25, L - 0.25, 9):
    middle = A + direction * s
    ax.plot([middle[0] - offset[0], middle[0] + offset[0]],
            [middle[1] - offset[1], middle[1] + offset[1]],
            color="tab:brown", lw=1.5)

# person (circle and a short "leg")
ax.plot(P[0], P[1] + 0.35, "o", ms=14, color="tab:blue")
ax.plot([P[0], P[0]], [P[1], P[1] + 0.25], color="tab:blue", lw=3)


def arrow(start, dx, dy, color="tab:red"):
    """Draws a force arrow from the point start in the direction (dx, dy)."""
    ax.annotate("", xy=(start[0] + dx, start[1] + dy), xytext=start,
                arrowprops=dict(arrowstyle="-|>", lw=1.6, color=color))


# forces: weight of the ladder and of the person, reactions at A and B
arrow(G, 0.0, -0.9)
ax.text(G[0] - 0.05, G[1] - 1.3, "$m\\,g$", color="tab:red", fontsize=12)
arrow(P, 0.0, -1.1)
ax.text(P[0] - 0.55, P[1] - 1.45, "$m_p\\,g$", color="tab:red", fontsize=12)
arrow(A, 0.0, 1.0, "tab:green")
ax.text(A[0] + 0.1, A[1] + 0.9, "$N_A$", color="tab:green", fontsize=12)
arrow(A, -0.9, 0.0, "tab:green")
ax.text(A[0] - 0.9, A[1] - 0.4, "$F_A$", color="tab:green", fontsize=12)
arrow(B, 0.8, 0.0, "tab:green")
ax.text(B[0] + 0.3, B[1] - 0.4, "$N_B$", color="tab:green", fontsize=12)

# angle theta, length L and position of the person x (dimension lines right of the ladder)
arc = np.linspace(np.pi - theta, np.pi, 30)
ax.plot(A[0] + 0.6 * np.cos(arc), A[1] + 0.6 * np.sin(arc), "k", lw=1)
ax.text(A[0] - 0.95, A[1] + 0.2, "$\\theta$", fontsize=13)
normal = np.array([np.sin(theta), np.cos(theta)])
dim_L = normal * 0.9
ax.annotate("", xy=B + dim_L, xytext=A + dim_L,
            arrowprops=dict(arrowstyle="<->", lw=1))
ax.text(G[0] + dim_L[0] + 0.1, G[1] + dim_L[1], "$L$", fontsize=13)
dim_x = normal * 0.45
ax.annotate("", xy=P + dim_x, xytext=A + dim_x,
            arrowprops=dict(arrowstyle="<->", lw=1))
middle_x = A + direction * x_person / 2 + dim_x
ax.text(middle_x[0] + 0.1, middle_x[1], "$x$", fontsize=13)

ax.text(0.15, 4.2, "smooth wall", fontsize=10)
ax.text(1.9, -0.55, "floor, $\\mu$", fontsize=10)
ax.set_xlim(-1.4, 4.0)
ax.set_ylim(-0.8, 4.6)
fig.tight_layout()
fig.savefig("sketch.png", dpi=150)
print("Saved: sketch.png")
