"""Render a safe conceptual animation for 'From Single Cell to Human'.

The generated animation is abstract: particles, fields, membranes and networks.
It contains no wet-lab protocol, no gene sequence, no cloning or embryo-manipulation workflow.
"""
from pathlib import Path
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "videos"
OUT.mkdir(parents=True, exist_ok=True)

stages = [
    "Single cell: boundary, information, energy and response",
    "Division: from one to many",
    "Differentiation: cells acquire identity",
    "Morphogenesis: a body plan emerges",
    "Organ formation: local functional modules appear",
    "System coupling: networks become an organism",
    "Emergence: from cells to a human outline",
    "Ethical boundary: understand life, do not manufacture life",
]

rng = np.random.default_rng(7)
fig = plt.figure(figsize=(12, 7), facecolor="#030712")
ax = fig.add_subplot(111, projection="3d", facecolor="#030712")
ax.set_axis_off()
ax.set_xlim(-5, 5)
ax.set_ylim(-3.2, 3.2)
ax.set_zlim(-3.2, 3.2)

cell_pts = rng.normal(size=(900, 3))
cell_pts /= np.linalg.norm(cell_pts, axis=1, keepdims=True)
cell_pts *= rng.random((900, 1)) ** (1 / 3) * 1.0
lineage_angles = np.linspace(0, 8 * np.pi, 90)
lineage = np.column_stack([
    np.cos(lineage_angles) * np.linspace(.4, 2.3, 90),
    np.sin(lineage_angles) * np.linspace(.4, 2.3, 90),
    np.sin(lineage_angles * .35),
])
body_y = np.linspace(-2.2, 2.4, 260)
body_r = .25 + .75 * np.exp(-((body_y - .3) / 1.2) ** 2) + .38 * np.exp(-((body_y - 2.0) / .45) ** 2)
body_theta = rng.random(260) * 2 * np.pi
body = np.column_stack([
    np.cos(body_theta) * body_r * rng.uniform(.45, 1.0, 260),
    body_y,
    np.sin(body_theta) * body_r * .35,
])

palette = np.array([
    [0.62, .84, 1.0],
    [1.0, .88, .38],
    [.75, .65, 1.0],
    [1.0, .45, .35],
    [.55, 1.0, .95],
])

def draw_sphere(center, radius, color, alpha):
    u = np.linspace(0, 2 * np.pi, 42)
    v = np.linspace(0, np.pi, 24)
    x = center[0] + radius * np.outer(np.cos(u), np.sin(v))
    y = center[1] + radius * np.outer(np.sin(u), np.sin(v))
    z = center[2] + radius * np.outer(np.ones_like(u), np.cos(v))
    ax.plot_wireframe(x, y, z, color=color, alpha=alpha, linewidth=.35)

def update(frame):
    ax.cla()
    ax.set_axis_off()
    ax.set_xlim(-5, 5)
    ax.set_ylim(-3.2, 3.2)
    ax.set_zlim(-3.2, 3.2)
    ax.view_init(elev=18 + 8 * math.sin(frame / 45), azim=frame * .7)
    p = frame / 179
    stage = min(7, int(p * 8))
    ax.text2D(.03, .92, stages[stage], color="#fef3c7", fontsize=17, transform=ax.transAxes, fontweight="bold")
    ax.text2D(.03, .86, "Abstract education visualization | self-organization, differentiation, morphogenesis, coupling", color="#c7d2fe", fontsize=10, transform=ax.transAxes)
    ax.text2D(.03, .06, "Safety boundary: no wet-lab protocol, gene editing, cloning, embryo operation, or actionable bioengineering parameters", color="#94a3b8", fontsize=9, transform=ax.transAxes)

    grow = min(1, max(0, (p - .10) / .20))
    pts = cell_pts * (1 + grow * 1.35)
    ax.scatter(pts[:, 0] - 2.6 * p, pts[:, 1], pts[:, 2], s=6, color=palette[frame % len(palette)], alpha=.28)
    draw_sphere((-2.6 * p, 0, 0), 1 + grow * 1.35, "#93c5fd", .28)
    draw_sphere((-2.6 * p, 0, 0), .34 + grow * .3, "#fde68a", .45)

    if p > .22:
        q = min(1, (p - .22) / .25)
        colors = palette[np.arange(len(lineage)) % len(palette)]
        ax.scatter(lineage[:, 0] * q - 1.0, lineage[:, 1] * q, lineage[:, 2] * q, s=28 * q, color=colors, alpha=.75 * q)
        for i in range(0, len(lineage) - 1, 3):
            ax.plot(lineage[i:i + 2, 0] * q - 1.0, lineage[i:i + 2, 1] * q, lineage[i:i + 2, 2] * q, color="#c4b5fd", alpha=.25 * q, linewidth=1)

    if p > .48:
        q = min(1, (p - .48) / .32)
        b = body * q + np.array([1.6, 0, 0])
        ax.scatter(b[:, 0], b[:, 1], b[:, 2], s=18 * q, color="#dbeafe", alpha=.48 * q)
        for k in range(22):
            y0 = 2.0 - k * .18
            ax.plot([1.6, 1.6 + math.sin(k) * .8 * q], [1.9 * q, y0 * q], [0, math.cos(k) * .25 * q], color="#60a5fa", alpha=.45 * q, linewidth=1.2)
            ax.plot([1.35, 1.6 + math.cos(k) * .9 * q], [.8 * q, y0 * q], [.1, math.sin(k) * .25 * q], color="#f97316", alpha=.38 * q, linewidth=1.2)
        ax.scatter([1.38], [.78 * q], [.12], s=180 * q, color="#fb923c", alpha=.9 * q)
        ax.scatter([1.2, 1.95], [1.05 * q, 1.05 * q], [0, 0], s=260 * q, color="#a5b4fc", alpha=.35 * q)
        ax.scatter([1.6], [-.22 * q], [0], s=260 * q, color="#fde68a", alpha=.42 * q)
    return []

ani = FuncAnimation(fig, update, frames=180, interval=1000 / 18, blit=False)
mp4_path = OUT / "cell_combination_human_concept.mp4"
gif_path = OUT / "cell_combination_human_concept.gif"
try:
    ani.save(mp4_path, writer=FFMpegWriter(fps=18, bitrate=1800))
    print(f"Wrote {mp4_path}")
except Exception as exc:
    print(f"MP4 export skipped: {exc}")
ani.save(gif_path, writer=PillowWriter(fps=12))
print(f"Wrote {gif_path}")
