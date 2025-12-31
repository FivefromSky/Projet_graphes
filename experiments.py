"""
Module pour l'étude statistique des algorithmes du PVC
Effectue 100 essais et analyse les performances
"""

import numpy as np
import time
from typing import Dict, List, Tuple
from graph import Graph
from ppp import PPP
from opt_ppp import OptPPP
from opt_prim import OptPrim
from hds import HDS
from visualization import plot_statistics, plot_comparison_percentages, plot_scalability


def run_single_experiment(n: int, start_point: int = 0, verbose: bool = False) -> Dict[str, Tuple[List[int], float, float]]:
    """
    Exécute tous les algorithmes sur une instance avec n points
    
    Args:
        n: Nombre de points
        start_point: Point de départ
        verbose: Afficher les détails
        
    Returns:
        Dict {nom_algo: (cycle, longueur, temps_execution)}
    """
    # Générer le graphe
    graph = Graph(n=n)
    
    results = {}
    
    # 1. PPP
    if verbose:
        print(f"  Exécution PPP...", end=" ")
    start_time = time.time()
    cycle_ppp, length_ppp = PPP(graph, start_point)
    time_ppp = time.time() - start_time
    results['PPP'] = (cycle_ppp, length_ppp, time_ppp)
    if verbose:
        print(f"✓ ({time_ppp:.4f}s)")
    
    # 2. OptPPP
    if verbose:
        print(f"  Exécution OptPPP...", end=" ")
    start_time = time.time()
    cycle_opt_ppp, length_opt_ppp = OptPPP(graph, cycle_ppp)
    time_opt_ppp = time.time() - start_time
    results['OptPPP'] = (cycle_opt_ppp, length_opt_ppp, time_opt_ppp)
    if verbose:
        print(f"✓ ({time_opt_ppp:.4f}s)")
    
    # 3. OptPrim
    if verbose:
        print(f"  Exécution OptPrim...", end=" ")
    start_time = time.time()
    cycle_prim, length_prim = OptPrim(graph, start_point)
    time_prim = time.time() - start_time
    results['OptPrim'] = (cycle_prim, length_prim, time_prim)
    if verbose:
        print(f"✓ ({time_prim:.4f}s)")
    
    # 4. HDS (seulement pour petites instances)
    if n <= 12:  # HDS est exponentiel, limiter à n ≤ 12
        if verbose:
            print(f"  Exécution HDS...", end=" ")
        start_time = time.time()
        cycle_hds, length_hds = HDS(graph, use_simple_bound=False, max_nodes=50000)
        time_hds = time.time() - start_time
        results['HDS'] = (cycle_hds, length_hds, time_hds)
        if verbose:
            print(f"✓ ({time_hds:.4f}s)")
    elif verbose:
        print(f"  HDS ignoré (n={n} trop grand)")
    
    return results


def run_multiple_experiments(n: int, num_trials: int = 100, verbose: bool = True) -> Dict[str, Dict]:
    """
    Exécute plusieurs essais et collecte les statistiques
    
    Args:
        n: Nombre de points
        num_trials: Nombre d'essais
        verbose: Afficher la progression
        
    Returns:
        Dict avec les statistiques pour chaque algorithme
    """
    if verbose:
        print(f"\n{'='*60}")
        print(f"Étude statistique: n={n}, {num_trials} essais")
        print(f"{'='*60}\n")
    
    # Structures pour collecter les résultats
    lengths = {
        'PPP': [],
        'OptPPP': [],
        'OptPrim': [],
    }
    
    if n <= 12:
        lengths['HDS'] = []
    
    times = {algo: [] for algo in lengths.keys()}
    
    # Exécuter les essais
    for trial in range(num_trials):
        if verbose and (trial + 1) % 10 == 0:
            print(f"Essai {trial + 1}/{num_trials}...")
        
        results = run_single_experiment(n, start_point=0, verbose=False)
        
        for algo, (cycle, length, exec_time) in results.items():
            lengths[algo].append(length)
            times[algo].append(exec_time)
    
    # Calculer les statistiques
    statistics = {}
    
    for algo in lengths.keys():
        stats = {
            'lengths': lengths[algo],
            'mean_length': np.mean(lengths[algo]),
            'std_length': np.std(lengths[algo]),
            'min_length': np.min(lengths[algo]),
            'max_length': np.max(lengths[algo]),
            'mean_time': np.mean(times[algo]),
            'std_time': np.std(times[algo]),
        }
        statistics[algo] = stats
    
    # Calculer les pourcentages d'amélioration
    if verbose:
        print(f"\n{'='*60}")
        print("RÉSULTATS")
        print(f"{'='*60}\n")
        
        for algo, stats in statistics.items():
            print(f"{algo}:")
            print(f"  Longueur moyenne: {stats['mean_length']:.6f} ± {stats['std_length']:.6f}")
            print(f"  Min: {stats['min_length']:.6f}, Max: {stats['max_length']:.6f}")
            print(f"  Temps moyen: {stats['mean_time']:.6f}s ± {stats['std_time']:.6f}s")
            print()
        
        # Pourcentages d'amélioration
        print(f"{'='*60}")
        print("POURCENTAGES D'AMÉLIORATION")
        print(f"{'='*60}\n")
        
        lp = statistics['PPP']['mean_length']
        lop = statistics['OptPPP']['mean_length']
        lpr = statistics['OptPrim']['mean_length']
        
        improvement_opt_vs_ppp = ((lp - lop) / lp) * 100
        print(f"OptPPP vs PPP: {improvement_opt_vs_ppp:+.2f}%")
        
        improvement_prim_vs_opt = ((lop - lpr) / lop) * 100
        print(f"OptPrim vs OptPPP: {improvement_prim_vs_opt:+.2f}%")
        
        improvement_prim_vs_ppp = ((lp - lpr) / lp) * 100
        print(f"OptPrim vs PPP: {improvement_prim_vs_ppp:+.2f}%")
        
        if 'HDS' in statistics:
            lhds = statistics['HDS']['mean_length']
            print(f"\nComparaison avec la solution optimale (HDS):")
            
            gap_ppp = ((lp - lhds) / lhds) * 100
            gap_opt = ((lop - lhds) / lhds) * 100
            gap_prim = ((lpr - lhds) / lhds) * 100
            
            print(f"  PPP:     écart = {gap_ppp:+.2f}%")
            print(f"  OptPPP:  écart = {gap_opt:+.2f}%")
            print(f"  OptPrim: écart = {gap_prim:+.2f}%")
    
    return statistics


def run_scalability_study(sizes: List[int] = [5, 10, 15, 20, 25], 
                          num_trials: int = 20) -> Dict:
    """
    Étudie la scalabilité des algorithmes pour différentes tailles
    
    Args:
        sizes: Liste des tailles de problème
        num_trials: Nombre d'essais par taille
        
    Returns:
        Dict avec les résultats de scalabilité
    """
    print(f"\n{'='*60}")
    print(f"ÉTUDE DE SCALABILITÉ")
    print(f"{'='*60}\n")
    
    results = {
        'sizes': sizes,
        'PPP': {'times': [], 'lengths': []},
        'OptPPP': {'times': [], 'lengths': []},
        'OptPrim': {'times': [], 'lengths': []},
    }
    
    for n in sizes:
        print(f"\nTaille n={n}:")
        stats = run_multiple_experiments(n, num_trials, verbose=False)
        
        for algo in ['PPP', 'OptPPP', 'OptPrim']:
            if algo in stats:
                results[algo]['times'].append(stats[algo]['mean_time'])
                results[algo]['lengths'].append(stats[algo]['mean_length'])
        
        print(f"  PPP:     {stats['PPP']['mean_time']:.4f}s, longueur: {stats['PPP']['mean_length']:.4f}")
        print(f"  OptPPP:  {stats['OptPPP']['mean_time']:.4f}s, longueur: {stats['OptPPP']['mean_length']:.4f}")
        print(f"  OptPrim: {stats['OptPrim']['mean_time']:.4f}s, longueur: {stats['OptPrim']['mean_length']:.4f}")
    
    return results


def compare_algorithms_visual(n: int = 15, num_trials: int = 100):
    """
    Lance l'étude complète avec visualisations
    
    Args:
        n: Nombre de points
        num_trials: Nombre d'essais
    """
    # Exécuter l'étude
    statistics = run_multiple_experiments(n, num_trials, verbose=True)
    
    # Préparer les données pour visualisation
    lengths_dict = {algo: stats['lengths'] for algo, stats in statistics.items()}
    
    # Afficher les statistiques
    print("\n📊 Génération des graphiques...")
    plot_statistics(lengths_dict, title=f"Statistiques pour n={n} ({num_trials} essais)")
    
    # Afficher les pourcentages
    plot_comparison_percentages(lengths_dict)
    
    return statistics


if __name__ == "__main__":
    # Exemple d'utilisation
    
    # 1. Étude pour une taille fixe
    print("="*70)
    print("ÉTUDE STATISTIQUE DU PROBLÈME DU VOYAGEUR DE COMMERCE")
    print("="*70)
    
    # Test avec n=15 points
    stats = compare_algorithms_visual(n=15, num_trials=100)
    
    # 2. Étude de scalabilité (optionnel)
    # Décommenter pour exécuter
    # scalability = run_scalability_study(sizes=[5, 10, 15, 20, 25], num_trials=20)
    # 
    # times_dict = {algo: scalability[algo]['times'] for algo in ['PPP', 'OptPPP', 'OptPrim']}
    # plot_scalability(scalability['sizes'], times_dict)