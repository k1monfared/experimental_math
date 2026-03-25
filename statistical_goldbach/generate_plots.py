"""
Generate all Goldbach conjecture visualizations.

Computes the number of ways each even number up to N can be decomposed
as a sum of two primes, then generates 6 analysis plots.

Requirements: matplotlib, numpy, sympy

Usage:
    python generate_plots.py          # default N=10000
    python generate_plots.py 20000    # custom upper limit
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from sympy import primerange
import math
import sys
import os

# --- Configuration ---
N = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
PHI = (1 + math.sqrt(5)) / 2  # golden ratio
C2 = 0.6601618                 # twin prime constant

# --- Compute decompositions ---
print(f'Computing Goldbach decompositions for even numbers up to {N:,}...')
primes_set = set(primerange(2, N))
primes_list = sorted(primes_set)

evens = list(range(4, N + 1, 2))
counts = []
for e in evens:
    c = 0
    for p in primes_list:
        if p > e:
            break
        if (e - p) in primes_set:
            c += 1
    counts.append(c)

evens = np.array(evens)
counts = np.array(counts)
print(f'Done. {len(evens)} even numbers, max decompositions: {max(counts)}')

# --- Helper functions ---

def author_curve(x):
    """The golden ratio bounding curve: f(x) = (x / (phi * pi))^(1/phi)"""
    return (x / (PHI * math.pi)) ** (1.0 / PHI)

def hardy_littlewood(n):
    """Simplified Hardy-Littlewood prediction for the number of Goldbach representations."""
    if n < 4:
        return 0
    ln_n = math.log(n)
    if ln_n < 1:
        return 1
    base = 2 * C2 * n / (ln_n ** 2)
    prod = 1.0
    for p in primes_list:
        if p > n // 2:
            break
        if p == 2:
            continue
        if n % p == 0:
            prod *= (p - 1) / (p - 2)
    return base * prod

author_pred = np.array([author_curve(e) for e in evens])
hl_pred = np.array([hardy_littlewood(e) for e in evens])
x_smooth = np.linspace(4, N, 1000)
y_smooth = np.array([author_curve(x) for x in x_smooth])
hl_smooth = np.array([hardy_littlewood(x) for x in x_smooth])

# Change to script directory so images are saved alongside the code
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ============================================================
# PLOT 1: Goldbach's Comet
# ============================================================
print('Generating plot 1/6: Goldbach\'s Comet...')
fig, ax = plt.subplots(figsize=(14, 7))
ax.scatter(evens, counts, s=0.5, c='#2c3e50', alpha=0.6)
ax.set_xlabel('Even number n', fontsize=13)
ax.set_ylabel('Number of Goldbach decompositions', fontsize=13)
ax.set_title(f"Goldbach's Comet: Decomposition Counts for Even Numbers up to {N:,}",
             fontsize=15, fontweight='bold')
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig('goldbach_comet.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# PLOT 2: Color-coded golden ratio curve fit
# ============================================================
print('Generating plot 2/6: Golden ratio curve fit...')
fig, ax = plt.subplots(figsize=(14, 7))
above = counts > author_pred
below = counts < author_pred
on_curve = ~above & ~below
ax.scatter(evens[above], counts[above], s=1.5, c='#3498db', alpha=0.5, label='Above curve')
ax.scatter(evens[below], counts[below], s=1.5, c='#e74c3c', alpha=0.5, label='Below curve')
ax.scatter(evens[on_curve], counts[on_curve], s=3, c='#2ecc71', alpha=0.7, label='On curve')
ax.plot(x_smooth, y_smooth, 'k-', linewidth=2,
        label=r'$f(x) = (x/(\varphi\pi))^{1/\varphi}$')
ax.set_xlabel('Even number n', fontsize=13)
ax.set_ylabel('Number of decompositions', fontsize=13)
ax.set_title(r'Goldbach Decompositions vs Golden Ratio Curve $f(x) = (x/(\varphi\pi))^{1/\varphi}$',
             fontsize=15, fontweight='bold')
ax.legend(fontsize=11, markerscale=5)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig('goldbach_curve_fit.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# PLOT 3: Ratio of actual to predicted
# ============================================================
print('Generating plot 3/6: Ratio analysis...')
fig, axes = plt.subplots(2, 1, figsize=(14, 9), sharex=True)

ratio_author = counts / np.maximum(author_pred, 0.01)
axes[0].scatter(evens, ratio_author, s=0.5, c='#8e44ad', alpha=0.4)
axes[0].axhline(y=1, color='black', linewidth=1.5, linestyle='--')
axes[0].set_ylabel('Actual / Predicted', fontsize=12)
axes[0].set_title('Ratio: Actual Count / Golden Ratio Prediction', fontsize=14, fontweight='bold')
axes[0].set_ylim(0, max(ratio_author) * 1.05)
axes[0].grid(True, alpha=0.3)

ratio_hl = counts / np.maximum(hl_pred, 0.01)
axes[1].scatter(evens, ratio_hl, s=0.5, c='#e67e22', alpha=0.4)
axes[1].axhline(y=1, color='black', linewidth=1.5, linestyle='--')
axes[1].set_xlabel('Even number n', fontsize=12)
axes[1].set_ylabel('Actual / Predicted', fontsize=12)
axes[1].set_title('Ratio: Actual Count / Hardy-Littlewood Prediction', fontsize=14, fontweight='bold')
axes[1].set_ylim(0, max(ratio_hl) * 1.05)
axes[1].grid(True, alpha=0.3)

fig.tight_layout()
fig.savefig('goldbach_ratio.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# PLOT 4: Minimum decomposition growth (lower bound)
# ============================================================
print('Generating plot 4/6: Minimum growth...')
fig, ax = plt.subplots(figsize=(14, 7))

window = 50
running_min = []
for i in range(len(counts)):
    start = max(0, i - window)
    running_min.append(min(counts[start:i + 1]))
running_min = np.array(running_min)

ax.scatter(evens, counts, s=0.3, c='#bdc3c7', alpha=0.3, label='All counts')
ax.plot(evens, running_min, color='#e74c3c', linewidth=1.5,
        label=f'Running minimum (window={window})')

chunk_size = 200
chunk_evens, chunk_mins = [], []
for i in range(0, len(counts), chunk_size):
    chunk = counts[i:i + chunk_size]
    chunk_evens.append(evens[i + np.argmin(chunk)])
    chunk_mins.append(min(chunk))
ax.plot(chunk_evens, chunk_mins, 'o-', color='#c0392b', linewidth=2, markersize=5,
        label='Lower envelope')

ax.axhline(y=1, color='black', linewidth=1, linestyle=':', alpha=0.5)
ax.annotate('If this ever hits 0,\nGoldbach is false',
            xy=(N * 0.7, 1), fontsize=11, color='#c0392b',
            arrowprops=dict(arrowstyle='->', color='#c0392b'),
            xytext=(N * 0.7, max(counts) * 0.15))
ax.set_xlabel('Even number n', fontsize=13)
ax.set_ylabel('Minimum decomposition count', fontsize=13)
ax.set_title('Minimum Goldbach Decompositions: The Lower Bound Never Reaches Zero',
             fontsize=15, fontweight='bold')
ax.legend(fontsize=11, markerscale=3)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig('goldbach_minimum.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# PLOT 5: Distribution histograms by range
# ============================================================
print('Generating plot 5/6: Distribution histograms...')
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

ranges = [
    (4, N // 10),
    (N // 10, N // 2),
    (N // 2, N),
]
colors = ['#3498db', '#2ecc71', '#e74c3c']

for ax, (lo, hi), col in zip(axes, ranges, colors):
    mask = (evens >= lo) & (evens <= hi)
    ax.hist(counts[mask], bins=30, color=col, alpha=0.7, edgecolor='white')
    ax.set_xlabel('Number of decompositions', fontsize=11)
    ax.set_ylabel('Frequency', fontsize=11)
    ax.set_title(f'n in [{lo:,}, {hi:,}]', fontsize=13, fontweight='bold')
    mean_val = np.mean(counts[mask])
    ax.axvline(mean_val, color='black', linestyle='--', linewidth=1.5,
               label=f'mean={mean_val:.1f}')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

fig.suptitle('Distribution of Goldbach Decomposition Counts by Range',
             fontsize=15, fontweight='bold', y=1.02)
fig.tight_layout()
fig.savefig('goldbach_distribution.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# PLOT 6: Hardy-Littlewood vs Golden Ratio comparison
# ============================================================
print('Generating plot 6/6: Prediction comparison...')
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

ax = axes[0]
ax.scatter(evens, counts, s=0.5, c='#bdc3c7', alpha=0.3, label='Actual counts')
ax.plot(x_smooth, y_smooth, color='#e74c3c', linewidth=2,
        label=r'Golden ratio: $(x/(\varphi\pi))^{1/\varphi}$')
ax.plot(x_smooth, hl_smooth, color='#3498db', linewidth=2, label='Hardy-Littlewood')
ax.set_xlabel('Even number n', fontsize=12)
ax.set_ylabel('Decomposition count', fontsize=12)
ax.set_title('Comparing Two Predictions for Goldbach Decomposition Counts',
             fontsize=14, fontweight='bold')
ax.legend(fontsize=11, markerscale=5)
ax.grid(True, alpha=0.3)

ax = axes[1]
residual_author = counts - author_pred
residual_hl = counts - hl_pred
ax.scatter(evens, residual_author, s=0.5, c='#e74c3c', alpha=0.3,
           label='Residual (golden ratio)')
ax.scatter(evens, residual_hl, s=0.5, c='#3498db', alpha=0.3,
           label='Residual (Hardy-Littlewood)')
ax.axhline(y=0, color='black', linewidth=1, linestyle='--')
ax.set_xlabel('Even number n', fontsize=12)
ax.set_ylabel('Actual - Predicted', fontsize=12)
ax.set_title('Residuals: Golden Ratio vs Hardy-Littlewood', fontsize=14, fontweight='bold')
ax.legend(fontsize=11, markerscale=5)
ax.grid(True, alpha=0.3)

fig.tight_layout()
fig.savefig('goldbach_comparison.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print(f'All 6 plots generated in {os.getcwd()}/')
