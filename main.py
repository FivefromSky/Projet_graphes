"""
Programme principal pour le problème du voyageur de commerce
Université de Rouen - L3 INFO-SD
Projet AlgoGraphes 2025-26

Références:
- Cormen et al., Introduction à l'algorithmique, Chapitre 37
- Optimisation Pythonnienne, Chapitre 2, pages 13-15

Usage:
    python main.py --n 20                    # Génère 20 points aléatoires
    python main.py --file data/points.txt    # Charge depuis fichier
    python main.py --n 15 --visual           # Avec visualisation
"""

import argparse
import sys
import time
import numpy as np
from graph import Graph
from ppp import PPP
from opt_ppp import OptPPP
from opt_prim import OptPrim
from hds import HDS
from visualization import plot_multiple_cycles, plot_cycle


def print_header():
    """Affiche l'en-tête du programme"""
    print("\n" + "="*70)
    print(" "*15 + "PROBLÈME DU VOYAGEUR DE COMMERCE")
    print(" "*20 + "Projet AlgoGraphes 2025-26")
    print(" "*18 + "Université de Rouen - L3 INFO-SD")
    print("="*70 + "\n")


def print_cycle_info(algo_name: str, cycle: list, length: float, exec_time: float):
    """Affiche les informations sur un cycle"""
    print(f"\n{algo_name}:")
    print(f"  Cycle: {' → '.join(map(str, cycle[:10]))}{'...' if len(cycle) > 10 else ''} → {cycle[0]}")
    print(f"  Longueur: {length:.6f}")
    print(f"  Temps d'exécution: {exec_time:.4f} secondes")


def run_algorithms(graph: Graph, start_point: int = 0, use_hds: bool = True, verbose: bool = True):
    """
    Exécute tous les algorithmes sur un graphe
    
    Args:
        graph: Instance de Graph
        start_point: Point de départ
        use_hds: Si True, exécute aussi HDS (pour petites instances)
        verbose: Afficher les détails
        
    Returns:
        Dict avec les résultats de chaque algorithme
    """
    n = graph.n
    results = {}
    
    if verbose:
        print(f"Instance: {n} points")
        print(f"Point de départ: {start_point}")
        print("-" * 70)
    
    # 1. Algorithme PPP (Point le Plus Proche)
    if verbose:
        print("\n🔄 Exécution de PPP (Point le Plus Proche)...")
    start_time = time.time()
    cycle_ppp, length_ppp = PPP(graph, start_point)
    time_ppp = time.time() - start_time
    
    if verbose:
        print_cycle_info("PPP", cycle_ppp, length_ppp, time_ppp)
    
    results['PPP'] = {
        'cycle': cycle_ppp,
        'length': length_ppp,
        'time': time_ppp
    }
    
    # 2. Algorithme OptPPP (Amélioration par décroisement)
    if verbose:
        print("\n🔄 Exécution de OptPPP (Optimisation par décroisement)...")
    start_time = time.time()
    cycle_opt_ppp, length_opt_ppp = OptPPP(graph, cycle_ppp)
    time_opt_ppp = time.time() - start_time
    
    improvement_ppp = ((length_ppp - length_opt_ppp) / length_ppp) * 100
    
    if verbose:
        print_cycle_info("OptPPP", cycle_opt_ppp, length_opt_ppp, time_opt_ppp)
        print(f"  Amélioration vs PPP: {improvement_ppp:+.2f}%")
    
    results['OptPPP'] = {
        'cycle': cycle_opt_ppp,
        'length': length_opt_ppp,
        'time': time_opt_ppp,
        'improvement_vs_ppp': improvement_ppp
    }
    
    # 3. Algorithme OptPrim (Arbre couvrant + parcours préfixe)
    if verbose:
        print("\n🔄 Exécution de OptPrim (Arbre couvrant minimum)...")
    start_time = time.time()
    cycle_prim, length_prim = OptPrim(graph, start_point)
    time_prim = time.time() - start_time
    
    improvement_vs_ppp = ((length_ppp - length_prim) / length_ppp) * 100
    improvement_vs_opt = ((length_opt_ppp - length_prim) / length_opt_ppp) * 100
    
    if verbose:
        print_cycle_info("OptPrim", cycle_prim, length_prim, time_prim)
        print(f"  Amélioration vs PPP: {improvement_vs_ppp:+.2f}%")
        print(f"  Amélioration vs OptPPP: {improvement_vs_opt:+.2f}%")
    
    results['OptPrim'] = {
        'cycle': cycle_prim,
        'length': length_prim,
        'time': time_prim,
        'improvement_vs_ppp': improvement_vs_ppp,
        'improvement_vs_opt': improvement_vs_opt
    }
    
    # 4. Algorithme HDS (Branch & Bound - Solution exacte)
    if use_hds and n <= 12:
        if verbose:
            print("\n🔄 Exécution de HDS (Branch & Bound - Solution exacte)...")
            print("   ⚠️  Cet algorithme peut être lent pour n > 12")
        
        start_time = time.time()
        cycle_hds, length_hds = HDS(graph, use_simple_bound=False, max_nodes=100000)
        time_hds = time.time() - start_time
        
        if verbose:
            print_cycle_info("HDS (Optimal)", cycle_hds, length_hds, time_hds)
            
            # Écarts par rapport à l'optimal
            gap_ppp = ((length_ppp - length_hds) / length_hds) * 100
            gap_opt = ((length_opt_ppp - length_hds) / length_hds) * 100
            gap_prim = ((length_prim - length_hds) / length_hds) * 100
            
            print(f"\n📊 Écarts par rapport à la solution optimale:")
            print(f"  PPP:     {gap_ppp:+.2f}%")
            print(f"  OptPPP:  {gap_opt:+.2f}%")
            print(f"  OptPrim: {gap_prim:+.2f}%")
        
        results['HDS'] = {
            'cycle': cycle_hds,
            'length': length_hds,
            'time': time_hds
        }
    elif use_hds and verbose:
        print(f"\n⚠️  HDS ignoré: n={n} trop grand (limite: 12 points)")
    
    return results


def main():
    """Fonction principale"""
    # Parser les arguments
    parser = argparse.ArgumentParser(
        description="Résolution du problème du voyageur de commerce",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python main.py --n 20                    Génère 20 points aléatoires
  python main.py --file points.txt         Charge depuis fichier
  python main.py --n 15 --visual           Avec visualisation
  python main.py --n 10 --hds              Calcule la solution optimale
  python main.py --n 20 --save out.txt     Sauvegarde les points
        """
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--n', type=int, help='Nombre de points à générer aléatoirement')
    group.add_argument('--file', type=str, help='Fichier contenant les points')
    
    parser.add_argument('--start', type=int, default=0, 
                       help='Point de départ (défaut: 0)')
    parser.add_argument('--hds', action='store_true',
                       help='Calculer la solution optimale avec HDS (pour n ≤ 12)')
    parser.add_argument('--visual', action='store_true',
                       help='Afficher les visualisations')
    parser.add_argument('--save', type=str, 
                       help='Sauvegarder les points dans un fichier')
    parser.add_argument('--seed', type=int,
                       help='Graine aléatoire pour reproductibilité')
    
    args = parser.parse_args()
    
    # Afficher l'en-tête
    print_header()
    
    # Configurer la graine aléatoire si spécifiée
    if args.seed is not None:
        np.random.seed(args.seed)
        print(f"🎲 Graine aléatoire: {args.seed}\n")
    
    # Charger ou générer le graphe
    try:
        if args.file:
            print(f"📂 Chargement depuis: {args.file}")
            graph = Graph.load_from_file(args.file)
            print(f"✓ {graph.n} points chargés\n")
        else:
            print(f"🎲 Génération de {args.n} points aléatoires")
            graph = Graph(n=args.n)
            print(f"✓ Points générés\n")
            
            # Sauvegarder si demandé
            if args.save:
                graph.save_to_file(args.save)
                print(f"💾 Points sauvegardés dans: {args.save}\n")
    
    except Exception as e:
        print(f"❌ Erreur lors du chargement: {e}")
        sys.exit(1)
    
    # Vérifier le point de départ
    if args.start < 0 or args.start >= graph.n:
        print(f"❌ Erreur: point de départ {args.start} invalide (doit être entre 0 et {graph.n-1})")
        sys.exit(1)
    
    # Exécuter les algorithmes
    try:
        results = run_algorithms(
            graph, 
            start_point=args.start, 
            use_hds=args.hds,
            verbose=True
        )
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Résumé
    print("\n" + "="*70)
    print("RÉSUMÉ DES RÉSULTATS")
    print("="*70)
    
    print(f"\n{'Algorithme':<15} {'Longueur':<15} {'Temps (s)':<12} {'Amélioration'}")
    print("-" * 70)
    
    for algo in ['PPP', 'OptPPP', 'OptPrim', 'HDS']:
        if algo in results:
            r = results[algo]
            improvement = ""
            if 'improvement_vs_ppp' in r:
                improvement = f"{r['improvement_vs_ppp']:+.2f}%"
            
            print(f"{algo:<15} {r['length']:<15.6f} {r['time']:<12.4f} {improvement}")
    
    # Visualisation
    if args.visual:
        print("\n📊 Génération des visualisations...")
        
        cycles_dict = {
            algo: (results[algo]['cycle'], results[algo]['length'])
            for algo in results.keys()
        }
        
        plot_multiple_cycles(graph, cycles_dict)
    
    print("\n✓ Programme terminé avec succès!")


if __name__ == "__main__":
    main()