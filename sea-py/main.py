"""
main.py
-------
Visualização interativa de dados musicais do Spotify.
Uso: python3 main.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns

# ── Configurações visuais ─────────────────────────────────────────────────────

BG     = "#0a0e0f"
PANEL  = "#0f1517"
GREEN  = "#00ff41"
CYAN   = "#00e5ff"
GRID   = "#1a2e2f"
WHITE  = "#e0ffe8"

GENRE_PALETTE = {
    "pop":        "#00e5ff",
    "hip-hop":    "#ff00a0",
    "rock":       "#ff6e00",
    "indie-rock": "#ffe600",
    "dance":      "#00ff41",
    "soul":       "#7b61ff",
    "k-pop":      "#ff4444",
}

plt.rcParams.update({
    "font.family":       "monospace",
    "figure.facecolor":  BG,
    "axes.facecolor":    PANEL,
    "axes.edgecolor":    GREEN,
    "axes.labelcolor":   GREEN,
    "axes.titlecolor":   GREEN,
    "axes.grid":         True,
    "grid.color":        GRID,
    "grid.linewidth":    0.5,
    "xtick.color":       GREEN,
    "ytick.color":       GREEN,
    "text.color":        GREEN,
    "legend.facecolor":  PANEL,
    "legend.edgecolor":  GREEN,
    "legend.labelcolor": WHITE,
})

# ── Carrega dados ─────────────────────────────────────────────────────────────

df = pd.read_csv("data/spotify_sample.csv")
df["year"] = df["year"].astype(int)
df["decade"] = (df["year"] // 10) * 10

# ── Dashboard ─────────────────────────────────────────────────────────────────

fig = plt.figure(figsize=(22, 14))
fig.suptitle(
    "[ SPOTIFY MUSIC DB ]  //  Genre & Year Intelligence Report",
    fontsize=15, color=GREEN, fontweight="bold", y=0.98
)

gs = gridspec.GridSpec(2, 3, figure=fig,
                       hspace=0.50, wspace=0.35,
                       left=0.06, right=0.97, top=0.91, bottom=0.07)

# ── Gráfico 1: tracks por ano ─────────────────────────────────────────────────

ax1 = fig.add_subplot(gs[0, 0])
counts = df.groupby("year")["track_name"].count()
ax1.bar(counts.index, counts.values, color=CYAN, edgecolor=BG, width=0.8)
ax1.set_title("▶  TRACKS POR ANO")
ax1.set_xlabel("ANO")
ax1.set_ylabel("TRACKS")

# ── Gráfico 2: tracks por gênero ──────────────────────────────────────────────

ax2 = fig.add_subplot(gs[0, 1])
genre_counts = df["genre"].value_counts()
colors = [GENRE_PALETTE.get(g, WHITE) for g in genre_counts.index]
bars = ax2.barh(genre_counts.index, genre_counts.values, color=colors, edgecolor=BG)
for bar, val in zip(bars, genre_counts.values):
    ax2.text(val + 0.2, bar.get_y() + bar.get_height() / 2,
             str(val), va="center", color=WHITE, fontsize=8)
ax2.set_title("◈  TRACKS POR GÊNERO")
ax2.set_xlabel("TOTAL")
ax2.invert_yaxis()

# ── Gráfico 3: evolução por década ────────────────────────────────────────────

ax3 = fig.add_subplot(gs[0, 2])
pivot = df.groupby(["decade", "genre"])["track_name"].count().unstack(fill_value=0)
genres_order = [g for g in GENRE_PALETTE if g in pivot.columns]
pivot[genres_order].plot.area(
    ax=ax3,
    color=[GENRE_PALETTE[g] for g in genres_order],
    alpha=0.8, linewidth=0
)
ax3.set_title("⚡  GÊNERO POR DÉCADA")
ax3.set_xlabel("DÉCADA")
ax3.set_ylabel("TRACKS")
ax3.legend(fontsize=7, framealpha=0.5)

# ── Gráfico 4: popularidade por gênero ───────────────────────────────────────

ax4 = fig.add_subplot(gs[1, 0])
order = df.groupby("genre")["popularity"].median().sort_values(ascending=False).index
sns.violinplot(
    data=df, x="genre", y="popularity",
    order=order, hue="genre",
    palette=GENRE_PALETTE, inner="box",
    linewidth=0.8, ax=ax4, legend=False,
)
ax4.set_title("★  POPULARIDADE POR GÊNERO")
ax4.set_xlabel("")
ax4.set_ylabel("POPULARIDADE")
ax4.tick_params(axis="x", labelsize=8, rotation=20)

# ── Gráfico 5: energia vs dançabilidade ──────────────────────────────────────

ax5 = fig.add_subplot(gs[1, 1])
for genre, color in GENRE_PALETTE.items():
    sub = df[df["genre"] == genre]
    if sub.empty:
        continue
    ax5.scatter(sub["energy"], sub["danceability"],
                color=color, label=genre, alpha=0.7, s=35, edgecolors="none")
ax5.set_title("◉  ENERGIA  vs  DANÇABILIDADE")
ax5.set_xlabel("ENERGIA")
ax5.set_ylabel("DANÇABILIDADE")
ax5.legend(fontsize=7, framealpha=0.5)

# ── Gráfico 6: heatmap BPM ────────────────────────────────────────────────────

ax6 = fig.add_subplot(gs[1, 2])
heat = df.pivot_table(index="genre", columns="decade", values="bpm", aggfunc="mean").round(0)
sns.heatmap(
    heat, ax=ax6,
    cmap="YlOrRd",
    linewidths=0.4, linecolor=BG,
    annot=True, fmt=".0f",
    annot_kws={"size": 7, "color": BG},
    cbar_kws={"shrink": 0.8},
)
ax6.set_title("◎  BPM MÉDIO  //  GÊNERO × DÉCADA")
ax6.set_xlabel("DÉCADA")
ax6.set_ylabel("")

plt.show()