"""
Module de visualisation pour le problème du voyageur de commerce
Affichage des cycles, statistiques et comparaisons
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Tuple
import seaborn as sns

# Configuration de style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10


def plot_cycle(graph, cycle: List[int], title: str = "Cycle Hamiltonien", 
               length: float = None, ax=None, color: str = 'blue'):
    """
    Affiche un cycle hamiltonien sur un graphique
    
    Args:
        graph: Instance de Graph
        cycle: Liste d'indices représentant le cycle
        title: Titre du graphique
        length: Longueur du cycle (affichée dans le titre)
        ax: Axes matplotlib (None = créer nouvelle figure)
        color: Couleur du cycle
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 10))
    
    # Extraire les coordonnées
    x = graph.x
    y = graph.y
    
    # Tracer les points
    ax.scatter(x, y, c='red', s=100, zorder=5, edgecolors='black', linewidth=1.5)
    
    # Numéroter les points
    for i in range(len(x)):
        ax.annotate(f'{i}', (x[i], y[i]), xytext=(5, 5), 
                   textcoords='offset points', fontsize=9, fontweight='bold')
    
    # Tracer le cycle
    for i in range(len(cycle)):
        start = cycle[i]
        end = cycle[(i + 1) % len(cycle)]
        
        ax.plot([x[start], x[end]], [y[start], y[end]], 
               c=color, linewidth=2, alpha=0.7, zorder=1)
        
        # Ajouter une flèche pour montrer la direction
        mid_x = (x[start] + x[end]) / 2
        mid_y = (y[start] + y[end]) / 2
        dx = x[end] - x[start]
        dy = y[end] - y[start]
        ax.arrow(mid_x - dx*0.1, mid_y - dy*0.1, dx*0.15, dy*0.15,
                head_width=0.02, head_length=0.02, fc=color, ec=color, 
                alpha=0.6, zorder=2)
    
    # Titre avec longueur
    if length is not None:
        title = f"{title}\nLongueur: {length:.4f}"
    ax.set_title(title, fontsize=14, fontweight='bold')
    
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    
    return ax


def plot_multiple_cycles(graph, cycles_dict: Dict[str, Tuple[List[int], float]], 
                        filename: str = None):
    """
    Affiche plusieurs cycles côte à côte pour comparaison
    
    Args:
        graph: Instance de Graph
        cycles_dict: Dict {nom_algo: (cycle, longueur)}
        filename: Si fourni, sauvegarde la figure
    """
    n_cycles = len(cycles_dict)
    fig, axes = plt.subplots(1, n_cycles, figsize=(6*n_cycles, 6))
    
    if n_cycles == 1:
        axes = [axes]
    
    colors = ['blue', 'green', 'purple', 'orange', 'brown']
    
    for (name, (cycle, length)), ax, color in zip(cycles_dict.items(), axes, colors):
        plot_cycle(graph, cycle, title=name, length=length, ax=ax, color=color)
    
    plt.tight_layout()
    
    if filename:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"📊 Figure sauvegardée: {filename}")
    
    plt.show()


def plot_statistics(results: Dict[str, List[float]], title: str = "Statistiques"):
    """
    Affiche les statistiques de performance des algorithmes
    
    Args:
        results: Dict {nom_algo: [longueurs_des_cycles]}
        title: Titre du graphique
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Boîtes à moustaches
    ax1 = axes[0, 0]
    data = [results[algo] for algo in results.keys()]
    bp = ax1.boxplot(data, labels=list(results.keys()), patch_artist=True)
    
    # Colorer les boîtes
    colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightyellow']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    
    ax1.set_title("Distribution des longueurs", fontsize=12, fontweight='bold')
    ax1.set_ylabel("Longueur du cycle", fontsize=11)
    ax1.grid(True, alpha=0.3, axis='y')
    
    # 2. Moyennes avec barres d'erreur
    ax2 = axes[0, 1]
    means = [np.mean(results[algo]) for algo in results.keys()]
    stds = [np.std(results[algo]) for algo in results.keys()]
    
    bars = ax2.bar(list(results.keys()), means, yerr=stds, 
                   capsize=5, color=colors[:len(results)], 
                   edgecolor='black', linewidth=1.5, alpha=0.7)
    
    # Ajouter les valeurs sur les barres
    for bar, mean in zip(bars, means):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{mean:.4f}', ha='center', va='bottom', fontweight='bold')
    
    ax2.set_title("Longueurs moyennes ± écart-type", fontsize=12, fontweight='bold')
    ax2.set_ylabel("Longueur moyenne", fontsize=11)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # 3. Histogrammes superposés
    ax3 = axes[1, 0]
    for algo, color in zip(results.keys(), colors):
        ax3.hist(results[algo], bins=20, alpha=0.5, label=algo, color=color, edgecolor='black')
    
    ax3.set_title("Distribution des performances", fontsize=12, fontweight='bold')
    ax3.set_xlabel("Longueur du cycle", fontsize=11)
    ax3.set_ylabel("Fréquence", fontsize=11)
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. Tableau de statistiques
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    stats_data = []
    for algo in results.keys():
        data = results[algo]
        stats_data.append([
            algo,
            f"{np.mean(data):.4f}",
            f"{np.std(data):.4f}",
            f"{np.min(data):.4f}",
            f"{np.max(data):.4f}"
        ])
    
    table = ax4.table(cellText=stats_data,
                     colLabels=['Algorithme', 'Moyenne', 'Écart-type', 'Min', 'Max'],
                     cellLoc='center',
                     loc='center',
                     colColours=['lightgray']*5)
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    
    ax4.set_title("Statistiques détaillées", fontsize=12, fontweight='bold', pad=20)
    
    plt.suptitle(title, fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.show()


def plot_comparison_percentages(results: Dict[str, List[float]]):
    """
    Affiche les pourcentages d'amélioration entre algorithmes
    
    Args:
        results: Dict {nom_algo: [longueurs]}
    """
    algos = list(results.keys())
    
    if len(algos) < 2:
        print("Besoin d'au moins 2 algorithmes pour comparer")
        return
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Calculer les pourcentages d'amélioration
    comparisons = []
    percentages = []
    
    for i in range(len(algos)):
        for j in range(i+1, len(algos)):
            algo1, algo2 = algos[i], algos[j]
            mean1 = np.mean(results[algo1])
            mean2 = np.mean(results[algo2])
            
            improvement = ((mean1 - mean2) / mean1) * 100
            comparisons.append(f"{algo1}\nvs\n{algo2}")
            percentages.append(improvement)
    
    # Couleurs: vert si amélioration, rouge si dégradation
    colors = ['green' if p > 0 else 'red' for p in percentages]
    
    bars = ax.barh(comparisons, percentages, color=colors, alpha=0.7, edgecolor='black')
    
    # Ajouter les valeurs
    for i, (bar, pct) in enumerate(zip(bars, percentages)):
        width = bar.get_width()
        label = f"{abs(pct):.2f}%"
        ax.text(width + (1 if width > 0 else -1), bar.get_y() + bar.get_height()/2,
               label, ha='left' if width > 0 else 'right', va='center', fontweight='bold')
    
    ax.axvline(x=0, color='black', linewidth=1.5, linestyle='-')
    ax.set_xlabel("Amélioration (%)", fontsize=12, fontweight='bold')
    ax.set_title("Pourcentages d'amélioration entre algorithmes", fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    plt.show()


def plot_convergence(iterations: List[int], lengths: List[float], 
                    title: str = "Convergence de l'algorithme"):
    """
    Affiche la convergence d'un algorithme itératif (ex: OptPPP)
    
    Args:
        iterations: Liste des numéros d'itération
        lengths: Liste des longueurs correspondantes
        title: Titre du graphique
    """
    plt.figure(figsize=(10, 6))
    
    plt.plot(iterations, lengths, marker='o', linewidth=2, markersize=6)
    plt.xlabel("Itération", fontsize=12)
    plt.ylabel("Longueur du cycle", fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    # Annoter la valeur finale
    plt.annotate(f'Final: {lengths[-1]:.4f}', 
                xy=(iterations[-1], lengths[-1]),
                xytext=(10, 10), textcoords='offset points',
                fontsize=11, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    
    plt.tight_layout()
    plt.show()


def plot_scalability(sizes: List[int], times: Dict[str, List[float]]):
    """
    Affiche l'évolution du temps d'exécution en fonction de n
    
    Args:
        sizes: Liste des tailles de problème (nombre de points)
        times: Dict {nom_algo: [temps_d'exécution]}
    """
    plt.figure(figsize=(10, 6))
    
    markers = ['o', 's', '^', 'D', 'v']
    
    for (algo, algo_times), marker in zip(times.items(), markers):
        plt.plot(sizes, algo_times, marker=marker, linewidth=2, 
                markersize=8, label=algo, alpha=0.7)
    
    plt.xlabel("Nombre de points (n)", fontsize=12, fontweight='bold')
    plt.ylabel("Temps d'exécution (secondes)", fontsize=12, fontweight='bold')
    plt.title("Scalabilité des algorithmes", fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.yscale('log')  # Échelle logarithmique pour y
    
    plt.tight_layout()
    plt.show()