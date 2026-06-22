"""
Generate all thesis figures for HinglishMSA.
Run from project root: .venv/Scripts/python.exe generate_figures.py
Saves to: Thesis_Report/Figures/generated/
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

OUT_DIR = 'Thesis_Report/Figures/generated'
os.makedirs(OUT_DIR, exist_ok=True)

plt.rcParams.update({
    'font.family': 'DejaVu Serif',
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'savefig.dpi': 200,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.2,
})

C_BLUE   = '#1565C0'
C_GREEN  = '#2E7D32'
C_RED    = '#B71C1C'
C_PURPLE = '#6A1B9A'
C_ORANGE = '#E65100'
C_TEAL   = '#00695C'
C_GRAY   = '#546E7A'
C_LIGHT  = '#ECEFF1'

EXPS  = ['E1\nBaseline', 'E2\nStandard', 'E3\nProposed\n(Full)', 'E4\nText-Only', 'E5\nHigh-Conf']
ACC2  = [0.6467, 0.6667, 0.7000, 0.4133, 0.7200]
F1S   = [0.6493, 0.6688, 0.7023, 0.2418, 0.7211]
MAE   = [1.2271, 1.1724, 1.0995, 1.3014, 1.0989]
CORR  = [0.3895, 0.4520, 0.4787, 0.2737, 0.5459]
ECOLORS = [C_BLUE, C_TEAL, C_GREEN, C_RED, C_ORANGE]


# ─────────────────────────────────────────────────────────────────
# FIG 1: Results Comparison (2x2)
# ─────────────────────────────────────────────────────────────────
def fig_results():
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    fig.suptitle('MulTHinglish — Experimental Results on HinglishMSA Test Set (150 clips)',
                 fontsize=14, fontweight='bold', y=1.01)

    x = np.arange(5)

    configs = [
        (axes[0, 0], ACC2, 'Acc-2 (higher = better)', 'Binary Accuracy', (0.25, 0.85), 0.797, 'upper left'),
        (axes[0, 1], F1S,  'F1-Score (higher = better)', 'Weighted F1-Score', (0.1, 0.85), 0.797, 'upper left'),
        (axes[1, 0], MAE,  'MAE (lower = better)', 'Mean Absolute Error', (0.8, 1.55), 0.887, 'lower right'),
        (axes[1, 1], CORR, 'Corr (higher = better)', 'Pearson Correlation', (0.1, 0.7), 0.706, 'upper left'),
    ]

    for ax, vals, ylabel, title, ylim, mosi_val, leg_loc in configs:
        bars = ax.bar(x, vals, color=ECOLORS, alpha=0.82, edgecolor='white', linewidth=1.0, width=0.55)
        ax.set_xticks(x)
        ax.set_xticklabels(EXPS, fontsize=9)
        ax.set_ylabel(ylabel, fontsize=11)
        ax.set_title(title, fontweight='bold', pad=8)
        ax.set_ylim(ylim)
        ax.axhline(mosi_val, color='#78909C', linestyle='--', linewidth=1.3,
                   label=f'CMU-MOSI English ({mosi_val})')
        ax.legend(fontsize=8.5, loc=leg_loc)
        ax.grid(axis='y', alpha=0.2, linestyle=':', color='gray')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        span = ylim[1] - ylim[0]
        for bar, val in zip(bars, vals):
            ypos = bar.get_height() + span * 0.02
            ax.text(bar.get_x() + bar.get_width() / 2, ypos,
                    f'{val:.3f}', ha='center', va='bottom', fontsize=9, fontweight='bold',
                    color='#212121')

        # bold border on best
        is_lower_better = (ylabel == 'MAE (lower = better)')
        best_idx = int(np.argmin(vals)) if is_lower_better else int(np.argmax(vals))
        bars[best_idx].set_edgecolor(C_GREEN)
        bars[best_idx].set_linewidth(2.5)
        bars[best_idx].set_alpha(1.0)

    plt.tight_layout()
    p = f'{OUT_DIR}/fig_results_comparison.png'
    plt.savefig(p)
    plt.close()
    print(f'  Saved: {p}')


# ─────────────────────────────────────────────────────────────────
# FIG 2: Dataset Construction Funnel
# ─────────────────────────────────────────────────────────────────
def fig_funnel():
    stages = [
        ('YouTube Videos\nDownloaded', 1174, C_BLUE),
        ('Clips with\nFace Detected', 43146, '#1976D2'),
        ('Clips\nTranscribed', 29500, '#42A5F5'),
        ('Hinglish Clips\nDetected', 6740, C_TEAL),
        ('Clips\nAnnotated', 4200, C_GREEN),
        ('Usable\nAnnotations', 2652, C_ORANGE),
        ('Training\nSet', 2451, '#EF6C00'),
        ('Test Set\n(Gold)', 150, C_RED),
    ]
    labels, values, colors = zip(*stages)
    max_val = max(values)

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, len(stages) + 0.5)
    ax.axis('off')

    bar_height = 0.65
    margin_scale = 0.9  # widest bar fills 90% of axes width

    for i, (label, val, col) in enumerate(reversed(stages)):
        y = i
        width = margin_scale * (val / max_val)
        x_start = (1 - width) / 2

        rect = FancyBboxPatch(
            (x_start, y + 0.08), width, bar_height,
            boxstyle='round,pad=0.01',
            facecolor=col, edgecolor='white', linewidth=1.5, alpha=0.88
        )
        ax.add_patch(rect)

        pct = val / 1174 * 100
        ax.text(0.5, y + 0.08 + bar_height / 2, f'{label}\n{val:,}  ({pct:.1f}% of videos)',
                ha='center', va='center', fontsize=9.5, fontweight='bold', color='white')

    ax.set_title('HinglishMSA — Dataset Construction Funnel', fontsize=14, fontweight='bold', pad=12)
    p = f'{OUT_DIR}/fig_dataset_funnel.png'
    plt.savefig(p)
    plt.close()
    print(f'  Saved: {p}')


# ─────────────────────────────────────────────────────────────────
# FIG 3: Sentiment Score Distribution
# ─────────────────────────────────────────────────────────────────
def fig_score_dist():
    try:
        df = pd.read_csv('data/auto_labeled.csv')
    except:
        print('  Skipping fig_score_dist: data/auto_labeled.csv not found')
        return

    scores = df['score'].dropna()

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle('HinglishMSA — Sentiment Score Distribution', fontsize=14, fontweight='bold')

    # Histogram
    ax = axes[0]
    n, bins, patches = ax.hist(scores, bins=30, edgecolor='white', linewidth=0.6, alpha=0.9)
    for patch, left in zip(patches, bins[:-1]):
        patch.set_facecolor(C_RED if left < 0 else C_GREEN)
        patch.set_alpha(0.78)
    ax.axvline(0, color='black', linewidth=1.5, linestyle='--', label='Neutral (0)')
    ax.axvline(scores.mean(), color=C_ORANGE, linewidth=1.5, linestyle='-.',
               label=f'Mean = {scores.mean():.2f}')
    ax.set_xlabel('Sentiment Score')
    ax.set_ylabel('Number of Clips')
    ax.set_title('Score Distribution')
    ax.legend(fontsize=10)
    ax.grid(axis='y', alpha=0.2, linestyle=':')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    neg_patch = mpatches.Patch(color=C_RED, alpha=0.78, label=f'Negative (s<=0): {(scores<=0).sum()}')
    pos_patch = mpatches.Patch(color=C_GREEN, alpha=0.78, label=f'Positive (s>0): {(scores>0).sum()}')
    ax.legend(handles=[neg_patch, pos_patch] + ax.get_legend_handles_labels()[0], fontsize=9.5)

    # Confidence pie
    ax2 = axes[1]
    if 'confidence' in df.columns:
        conf_counts = df['confidence'].value_counts()
        conf_labels = []
        conf_vals = []
        conf_colors = []
        for c, col in [('high', C_GREEN), ('medium', C_ORANGE), ('low', C_RED)]:
            if c in conf_counts:
                conf_labels.append(f'{c.capitalize()}\n(n={conf_counts[c]:,})')
                conf_vals.append(conf_counts[c])
                conf_colors.append(col)

        wedges, texts, autotexts = ax2.pie(
            conf_vals, labels=conf_labels, colors=conf_colors,
            autopct='%1.1f%%', startangle=90, pctdistance=0.75,
            wedgeprops={'edgecolor': 'white', 'linewidth': 2}
        )
        for at in autotexts:
            at.set_fontsize(11)
            at.set_fontweight('bold')
        ax2.set_title('Annotation Confidence Distribution\n(Total: 2,652 usable clips)',
                      fontweight='bold', pad=10)
    else:
        ax2.axis('off')

    plt.tight_layout()
    p = f'{OUT_DIR}/fig_score_distribution.png'
    plt.savefig(p)
    plt.close()
    print(f'  Saved: {p}')


# ─────────────────────────────────────────────────────────────────
# FIG 4: MulTHinglish Architecture Diagram
# ─────────────────────────────────────────────────────────────────
def draw_box(ax, x, y, w, h, text, facecolor, fontsize=10, textcolor='white', style='round,pad=0.05'):
    box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                          boxstyle=style, facecolor=facecolor,
                          edgecolor='white', linewidth=1.5, zorder=3)
    ax.add_patch(box)
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize,
            fontweight='bold', color=textcolor, zorder=4, wrap=True,
            multialignment='center')

def draw_arrow(ax, x1, y1, x2, y2, color='#455A64', lw=1.5):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw,
                                connectionstyle='arc3,rad=0.0'))

def fig_architecture():
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_facecolor('#FAFAFA')
    fig.patch.set_facecolor('#FAFAFA')

    # ── Column x positions ──
    X_INPUT    = 1.3
    X_ENCODER  = 3.6
    X_PROJ     = 5.8
    X_CROSS    = 9.0
    X_CONCAT   = 12.0
    X_MLP      = 13.8
    X_OUT      = 15.5

    # ── Row y positions ──
    Y_TEXT   = 7.8
    Y_AUDIO  = 5.0
    Y_VISUAL = 2.2

    BOX_H = 0.85
    BOX_W_IN  = 1.8
    BOX_W_ENC = 1.7
    BOX_W_PRJ = 1.5
    ARROW_COL = '#37474F'

    # ── Section headers ──
    for x, label in [(X_INPUT, 'Inputs'), (X_ENCODER, 'Encoders'),
                     (X_PROJ, 'Projection'), (X_CROSS, 'Cross-Modal\nAttention'),
                     (X_CONCAT, 'Fusion'), (X_MLP, 'Prediction')]:
        ax.text(x, 9.5, label, ha='center', va='center', fontsize=9.5,
                color='#546E7A', fontstyle='italic')

    # ── Input boxes ──
    draw_box(ax, X_INPUT, Y_TEXT,  BOX_W_IN, BOX_H, 'Text\n(Transcription)', C_BLUE)
    draw_box(ax, X_INPUT, Y_AUDIO, BOX_W_IN, BOX_H, 'Audio\n(16kHz WAV)',    C_TEAL)
    draw_box(ax, X_INPUT, Y_VISUAL,BOX_W_IN, BOX_H, 'Visual\n(5 Frames)',    C_PURPLE)

    # ── Encoder boxes ──
    draw_box(ax, X_ENCODER, Y_TEXT,  BOX_W_ENC, BOX_H, 'MuRIL\n(BERT-based)', C_BLUE)
    draw_box(ax, X_ENCODER, Y_AUDIO, BOX_W_ENC, BOX_H, 'wav2vec2\nXLSR-53',    C_TEAL)
    draw_box(ax, X_ENCODER, Y_VISUAL,BOX_W_ENC, BOX_H, 'CLIP\nViT-B/32',       C_PURPLE)

    # ── Projection boxes ──
    draw_box(ax, X_PROJ, Y_TEXT,  BOX_W_PRJ, BOX_H, '768\n →\n 128', '#1E88E5', fontsize=9)
    draw_box(ax, X_PROJ, Y_AUDIO, BOX_W_PRJ, BOX_H, '1024\n →\n 128','#26A69A', fontsize=9)
    draw_box(ax, X_PROJ, Y_VISUAL,BOX_W_PRJ, BOX_H, '512\n →\n 128', '#7B1FA2', fontsize=9)

    # dim labels after projection
    for y, dim in [(Y_TEXT, '768d'), (Y_AUDIO, '1024d'), (Y_VISUAL, '512d')]:
        ax.text(X_ENCODER + BOX_W_ENC/2 + 0.15, y, dim, fontsize=8.5, color='#546E7A', va='center')

    # ── Arrows: Input → Encoder ──
    for y in [Y_TEXT, Y_AUDIO, Y_VISUAL]:
        draw_arrow(ax, X_INPUT + BOX_W_IN/2, y, X_ENCODER - BOX_W_ENC/2, y, ARROW_COL)
        draw_arrow(ax, X_ENCODER + BOX_W_ENC/2, y, X_PROJ - BOX_W_PRJ/2, y, ARROW_COL)

    # ── Cross-Modal Attention Block ──
    cross_cx = X_CROSS
    cross_w  = 2.8
    cross_h  = 6.8
    cross_y  = (Y_TEXT + Y_VISUAL) / 2

    cross_box = FancyBboxPatch((cross_cx - cross_w/2, cross_y - cross_h/2),
                                cross_w, cross_h,
                                boxstyle='round,pad=0.1',
                                facecolor='#FFF9C4', edgecolor=C_ORANGE,
                                linewidth=2.0, zorder=2)
    ax.add_patch(cross_box)

    ax.text(cross_cx, cross_y + 2.8, 'Cross-Modal\nAttention\n(6 Directions)',
            ha='center', va='center', fontsize=10.5, fontweight='bold', color=C_ORANGE, zorder=5)

    # 6 attention direction labels inside
    attn_pairs = ['T ← A', 'T ← V', 'A ← T', 'A ← V', 'V ← T', 'V ← A']
    attn_colors = [C_TEAL, C_PURPLE, C_BLUE, C_PURPLE, C_BLUE, C_TEAL]
    for idx, (pair, col) in enumerate(zip(attn_pairs, attn_colors)):
        yy = cross_y + 1.6 - idx * 0.7
        ax.text(cross_cx, yy, pair, ha='center', va='center',
                fontsize=9.5, color=col, fontweight='bold', zorder=5)

    ax.text(cross_cx, cross_y - 2.2, f'L=4 layers\nH=8 heads\nd_model=128',
            ha='center', va='center', fontsize=8.5, color='#5D4037', zorder=5,
            style='italic')

    # Arrows: Projection → Cross-Modal
    for y in [Y_TEXT, Y_AUDIO, Y_VISUAL]:
        draw_arrow(ax, X_PROJ + BOX_W_PRJ/2, y, cross_cx - cross_w/2, y, ARROW_COL)

    # ── Concat box ──
    draw_box(ax, X_CONCAT, cross_y, 1.5, 1.6, 'Concat\n6×128\n= 768d', C_GRAY, fontsize=9)
    draw_arrow(ax, cross_cx + cross_w/2, cross_y, X_CONCAT - 0.75, cross_y, ARROW_COL, lw=2.0)

    # ── MLP box ──
    draw_box(ax, X_MLP, cross_y, 1.5, 2.2,
             'MLP\n768→256\n→128→1', '#4E342E', fontsize=9)
    draw_arrow(ax, X_CONCAT + 0.75, cross_y, X_MLP - 0.75, cross_y, ARROW_COL, lw=2.0)

    # ── Output ──
    draw_box(ax, X_OUT, cross_y, 1.2, 0.85, 'Score\nϵ [-3, +3]', C_GREEN, fontsize=10)
    draw_arrow(ax, X_MLP + 0.75, cross_y, X_OUT - 0.6, cross_y, ARROW_COL, lw=2.0)

    # ── Title ──
    ax.set_title('MulTHinglish Architecture — 5,283,713 Parameters',
                 fontsize=14, fontweight='bold', pad=15)

    # ── Legend ──
    legend_items = [
        mpatches.Patch(facecolor=C_BLUE,   label='Text Pathway (MuRIL)'),
        mpatches.Patch(facecolor=C_TEAL,   label='Audio Pathway (wav2vec2-XLSR-53)'),
        mpatches.Patch(facecolor=C_PURPLE, label='Visual Pathway (CLIP ViT-B/32)'),
        mpatches.Patch(facecolor='#FFF9C4', edgecolor=C_ORANGE, linewidth=1.5,
                       label='Cross-Modal Attention (6 directions, L=4 layers each)'),
    ]
    ax.legend(handles=legend_items, loc='lower left', fontsize=9.5,
              framealpha=0.9, edgecolor='#90A4AE')

    p = f'{OUT_DIR}/fig_multhilnglish_arch.png'
    plt.savefig(p)
    plt.close()
    print(f'  Saved: {p}')


# ─────────────────────────────────────────────────────────────────
# FIG 5: Cross-Modal Attention Directions
# ─────────────────────────────────────────────────────────────────
def fig_crossmodal():
    fig, ax = plt.subplots(figsize=(8, 7))
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 8)
    ax.axis('off')
    fig.patch.set_facecolor('#FAFAFA')

    # 3 modality nodes in triangle
    nodes = {'T': (4.0, 6.5), 'A': (1.5, 2.0), 'V': (6.5, 2.0)}
    node_labels = {'T': 'Text\n(MuRIL)', 'A': 'Audio\n(XLSR)', 'V': 'Visual\n(CLIP)'}
    node_colors = {'T': C_BLUE, 'A': C_TEAL, 'V': C_PURPLE}
    node_r = 0.72

    # Draw 6 directed arrows (all pairs both directions)
    import matplotlib.patheffects as pe

    pairs = [
        ('T', 'A', C_BLUE,   0.25, 'T←A'),
        ('A', 'T', C_TEAL,   0.25, 'A←T'),
        ('T', 'V', C_BLUE,   0.25, 'T←V'),
        ('V', 'T', C_PURPLE, 0.25, 'V←T'),
        ('A', 'V', C_TEAL,   0.25, 'A←V'),
        ('V', 'A', C_PURPLE, 0.25, 'V←A'),
    ]

    drawn_pairs = set()
    for src, tgt, col, rad, label in pairs:
        x1, y1 = nodes[src]
        x2, y2 = nodes[tgt]
        key = tuple(sorted([src, tgt]))
        rad_sign = rad if key not in drawn_pairs else -rad
        drawn_pairs.add(key)

        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(
                        arrowstyle='->', color=col, lw=2.0,
                        connectionstyle=f'arc3,rad={rad_sign}',
                        shrinkA=node_r * 72, shrinkB=node_r * 72
                    ))

        # label at midpoint
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        # offset perpendicular
        dx = x2 - x1
        dy = y2 - y1
        length = (dx**2 + dy**2)**0.5
        perp_x = -dy / length * 0.55 * np.sign(rad_sign)
        perp_y =  dx / length * 0.55 * np.sign(rad_sign)
        ax.text(mx + perp_x, my + perp_y, label, ha='center', va='center',
                fontsize=9.5, fontweight='bold', color=col,
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.75, pad=1.5))

    # Draw nodes on top
    for name, (cx, cy) in nodes.items():
        circle = plt.Circle((cx, cy), node_r, facecolor=node_colors[name],
                             edgecolor='white', linewidth=2.5, zorder=5)
        ax.add_patch(circle)
        ax.text(cx, cy, node_labels[name], ha='center', va='center',
                fontsize=11, fontweight='bold', color='white', zorder=6,
                multialignment='center')

    ax.set_title('Cross-Modal Attention — 6 Directed Attention Streams\n'
                 '(Each stream: L=4 stacked transformer layers, H=8 heads)',
                 fontsize=13, fontweight='bold', pad=10)

    legend_items = [
        mpatches.Patch(facecolor=C_BLUE,   label='Query from Text'),
        mpatches.Patch(facecolor=C_TEAL,   label='Query from Audio'),
        mpatches.Patch(facecolor=C_PURPLE, label='Query from Visual'),
    ]
    ax.legend(handles=legend_items, loc='upper left', fontsize=10, framealpha=0.9)

    p = f'{OUT_DIR}/fig_crossmodal_attention.png'
    plt.savefig(p)
    plt.close()
    print(f'  Saved: {p}')


# ─────────────────────────────────────────────────────────────────
# FIG 6: Pipeline Flowchart
# ─────────────────────────────────────────────────────────────────
def fig_pipeline():
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 5)
    ax.axis('off')
    fig.patch.set_facecolor('#FAFAFA')

    steps = [
        ('YouTube\nAPI v3', '1,179\nvideos', C_BLUE),
        ('pytubefix\n+ ffmpeg', '1,174 WAV\n+ frames', '#1976D2'),
        ('Silence\nDetect', '50,695\nclips', '#42A5F5'),
        ('Face\nDetection', '43,146\nclips', C_TEAL),
        ('Whisper\nlarge-v3', '29,500\ntranscripts', C_GREEN),
        ('Hinglish\nDetect', '6,740\nclips', C_ORANGE),
        ('Groq\nLLM', '2,652\nlabels', C_RED),
        ('MuRIL\nXLSR\nCLIP', '3x\nfeature\narrays', C_PURPLE),
        ('MulTHinglish\nTraining', 'Acc-2\n70.0%', '#4E342E'),
    ]

    box_w = 1.3
    box_h = 3.2
    gap   = 0.22
    total_w = len(steps) * box_w + (len(steps) - 1) * gap
    x_start = (14 - total_w) / 2

    for i, (title, detail, col) in enumerate(steps):
        x = x_start + i * (box_w + gap)
        y_center = 2.5

        rect = FancyBboxPatch((x, y_center - box_h/2), box_w, box_h,
                               boxstyle='round,pad=0.06',
                               facecolor=col, edgecolor='white', linewidth=1.5,
                               alpha=0.88, zorder=3)
        ax.add_patch(rect)

        ax.text(x + box_w/2, y_center + 0.55, title,
                ha='center', va='center', fontsize=8.5, fontweight='bold',
                color='white', zorder=4, multialignment='center')
        ax.text(x + box_w/2, y_center - 0.65, detail,
                ha='center', va='center', fontsize=8.0, color='white',
                zorder=4, multialignment='center')

        # Arrow to next
        if i < len(steps) - 1:
            ax.annotate('', xy=(x + box_w + gap, y_center),
                        xytext=(x + box_w, y_center),
                        arrowprops=dict(arrowstyle='->', color='#546E7A',
                                        lw=1.5, mutation_scale=14))

        # Phase label below
        ax.text(x + box_w/2, y_center - box_h/2 - 0.25, f'Phase {i+1}',
                ha='center', va='top', fontsize=7.5, color='#78909C', style='italic')

    ax.set_title('HinglishMSA — End-to-End Pipeline',
                 fontsize=14, fontweight='bold', pad=10)

    p = f'{OUT_DIR}/fig_pipeline_overview.png'
    plt.savefig(p)
    plt.close()
    print(f'  Saved: {p}')


# ─────────────────────────────────────────────────────────────────
# FIG 7: Modality Ablation Bar Chart (focused)
# ─────────────────────────────────────────────────────────────────
def fig_ablation():
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle('MulTHinglish — Ablation Study: Effect of Modalities and Label Quality',
                 fontsize=13, fontweight='bold')

    # Left: Multimodal vs Text-Only
    ax = axes[0]
    categories = ['Text-Only\n(E4)', 'Full Multimodal\n(E3 Proposed)', 'High-Conf Only\n(E5)']
    acc_vals  = [0.4133, 0.7000, 0.7200]
    bar_cols  = [C_RED, C_GREEN, C_ORANGE]

    bars = ax.bar(range(3), acc_vals, color=bar_cols, alpha=0.85, edgecolor='white', linewidth=1.2, width=0.55)
    ax.set_xticks(range(3))
    ax.set_xticklabels(categories, fontsize=10)
    ax.set_ylabel('Binary Accuracy (Acc-2)', fontsize=11)
    ax.set_title('Unimodal vs. Multimodal vs. Label Quality', fontweight='bold')
    ax.set_ylim(0.25, 0.85)
    ax.axhline(0.797, color='gray', linestyle='--', linewidth=1.2, label='CMU-MOSI English (0.797)')
    ax.legend(fontsize=9)
    ax.grid(axis='y', alpha=0.2, linestyle=':')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    for bar, val in zip(bars, acc_vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.015,
                f'{val:.1%}', ha='center', va='bottom', fontsize=12, fontweight='bold')

    # Annotate improvement
    ax.annotate('', xy=(1, 0.700), xytext=(0, 0.4133),
                arrowprops=dict(arrowstyle='->', color=C_GREEN, lw=2.0))
    ax.text(0.5, 0.58, '+28.7 pp', ha='center', fontsize=10, color=C_GREEN, fontweight='bold')

    # Right: radar/spider-like comparison - just a grouped bar for 4 metrics
    ax2 = axes[1]
    x = np.arange(4)
    metrics = ['Acc-2', 'F1', '1-MAE\n(normalized)', 'Corr']

    # Normalize MAE: 1 - MAE/max_MAE so higher=better
    max_mae = 1.5
    e3_vals = [0.7000, 0.7023, 1 - 1.0995/max_mae, 0.4787]
    e4_vals = [0.4133, 0.2418, 1 - 1.3014/max_mae, 0.2737]
    e5_vals = [0.7200, 0.7211, 1 - 1.0989/max_mae, 0.5459]

    w = 0.22
    b1 = ax2.bar(x - w, e3_vals, w, label='E3 Proposed (Full)', color=C_GREEN, alpha=0.82)
    b2 = ax2.bar(x,     e4_vals, w, label='E4 Text-Only',        color=C_RED,   alpha=0.82)
    b3 = ax2.bar(x + w, e5_vals, w, label='E5 High-Conf',        color=C_ORANGE,alpha=0.82)

    ax2.set_xticks(x)
    ax2.set_xticklabels(metrics, fontsize=10)
    ax2.set_ylabel('Score (higher = better)')
    ax2.set_title('All Metrics Comparison\n(MAE inverted for uniformity)', fontweight='bold')
    ax2.set_ylim(0, 0.95)
    ax2.legend(fontsize=9)
    ax2.grid(axis='y', alpha=0.2, linestyle=':')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    plt.tight_layout()
    p = f'{OUT_DIR}/fig_ablation_study.png'
    plt.savefig(p)
    plt.close()
    print(f'  Saved: {p}')


# ─────────────────────────────────────────────────────────────────
# FIG 8: Hinglish Detection Comparison
# ─────────────────────────────────────────────────────────────────
def fig_detection():
    fig, ax = plt.subplots(figsize=(9, 5))

    methods = ['Naive ASR\nLanguage ID', 'Improved\n3-Stage Algorithm']
    hinglish = [1019, 6740]
    other = [29500-1019, 29500-6740]
    pct = [1019/29500*100, 6740/29500*100]

    x = np.arange(2)
    w = 0.5

    b1 = ax.bar(x, hinglish, w, label='Hinglish Detected', color=C_GREEN, alpha=0.88)
    b2 = ax.bar(x, other, w, bottom=hinglish, label='Non-Hinglish', color='#B0BEC5', alpha=0.7)

    ax.set_xticks(x)
    ax.set_xticklabels(methods, fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Clips', fontsize=12)
    ax.set_title('Hinglish Detection: Naive vs. Improved Algorithm\n(From 29,500 transcribed clips)',
                 fontsize=13, fontweight='bold')
    ax.set_ylim(0, 33000)
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.2, linestyle=':')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    for i, (h, p) in enumerate(zip(hinglish, pct)):
        ax.text(i, h/2, f'{h:,}\n({p:.1f}%)', ha='center', va='center',
                fontsize=12, fontweight='bold', color='white')

    ax.annotate('', xy=(1, 5000), xytext=(0, 5000),
                arrowprops=dict(arrowstyle='->', color=C_ORANGE, lw=2.5))
    ax.text(0.5, 5800, '6.6x\nImprovement', ha='center', fontsize=11, color=C_ORANGE, fontweight='bold')

    p = f'{OUT_DIR}/fig_hinglish_detection.png'
    plt.savefig(p)
    plt.close()
    print(f'  Saved: {p}')


# ─────────────────────────────────────────────────────────────────
# RUN ALL
# ─────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print('Generating HinglishMSA thesis figures...')
    print(f'Output directory: {OUT_DIR}\n')

    print('1/8  Results comparison chart...')
    fig_results()

    print('2/8  Dataset funnel...')
    fig_funnel()

    print('3/8  Score distribution...')
    fig_score_dist()

    print('4/8  MulTHinglish architecture...')
    fig_architecture()

    print('5/8  Cross-modal attention diagram...')
    fig_crossmodal()

    print('6/8  Pipeline flowchart...')
    fig_pipeline()

    print('7/8  Ablation study chart...')
    fig_ablation()

    print('8/8  Hinglish detection comparison...')
    fig_detection()

    print(f'\nAll figures saved to: {OUT_DIR}/')
    import os
    files = sorted(os.listdir(OUT_DIR))
    for f in files:
        size = os.path.getsize(f'{OUT_DIR}/{f}') // 1024
        print(f'  {f}  ({size} KB)')
