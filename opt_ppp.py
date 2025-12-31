"""
Amélioration de PPP par décroisement d'arêtes (2-opt)
Optimisation locale par élimination des croisements

Référence: Optimisation Pythonnienne, Chapitre 2
"""

import numpy as np
from typing import List, Tuple


def check_crossing(graph, cycle: List[int], i: int, j: int) -> bool:
    """
    Vérifie si deux arêtes se croisent géométriquement dans le plan
    
    Args:
        graph: Instance de Graph
        cycle: Cycle hamiltonien
        i, j: Indices dans le cycle (j >= i+2)
        
    Returns:
        True si les arêtes (cycle[i], cycle[i+1]) et (cycle[j], cycle[j+1]) se croisent
    """
    n = len(cycle)
    
    # Points des deux arêtes
    p1_idx = cycle[i]
    p2_idx = cycle[(i + 1) % n]
    p3_idx = cycle[j]
    p4_idx = cycle[(j + 1) % n]
    
    # Coordonnées
    x1, y1 = graph.get_point_coords(p1_idx)
    x2, y2 = graph.get_point_coords(p2_idx)
    x3, y3 = graph.get_point_coords(p3_idx)
    x4, y4 = graph.get_point_coords(p4_idx)
    
    # Test d'intersection de segments (formule du produit vectoriel)
    def ccw(ax, ay, bx, by, cx, cy):
        return (cy - ay) * (bx - ax) > (by - ay) * (cx - ax)
    
    return (ccw(x1, y1, x3, y3, x4, y4) != ccw(x2, y2, x3, y3, x4, y4) and
            ccw(x1, y1, x2, y2, x3, y3) != ccw(x1, y1, x2, y2, x4, y4))


def two_opt_swap(cycle: List[int], i: int, j: int) -> List[int]:
    """
    Effectue une transformation 2-opt en inversant l'ordre entre i+1 et j
    
    Transformation:
    [..., cycle[i], cycle[i+1], ..., cycle[j], cycle[j+1], ...]
    devient:
    [..., cycle[i], cycle[j], ..., cycle[i+1], cycle[j+1], ...]
    
    Args:
        cycle: Cycle hamiltonien
        i, j: Indices pour le décroisement
        
    Returns:
        Nouveau cycle après transformation
    """
    new_cycle = cycle[:i+1] + cycle[i+1:j+1][::-1] + cycle[j+1:]
    return new_cycle


def is_swap_beneficial(graph, cycle: List[int], i: int, j: int) -> Tuple[bool, float]:
    """
    Vérifie si un décroisement améliore la longueur du cycle
    
    Args:
        graph: Instance de Graph
        cycle: Cycle hamiltonien
        i, j: Indices pour le décroisement
        
    Returns:
        Tuple (beneficial, improvement) où:
            - beneficial: True si le décroisement réduit la longueur
            - improvement: Amélioration de longueur (positive si bénéfique)
    """
    n = len(cycle)
    D = graph.D
    
    # Arêtes actuelles
    edge1_start = cycle[i]
    edge1_end = cycle[(i + 1) % n]
    edge2_start = cycle[j]
    edge2_end = cycle[(j + 1) % n]
    
    # Longueur actuelle des deux arêtes
    old_length = D[edge1_start, edge1_end] + D[edge2_start, edge2_end]
    
    # Nouvelles arêtes après décroisement
    new_edge1_end = cycle[j]
    new_edge2_end = cycle[(i + 1) % n]
    
    # Longueur après décroisement
    new_length = D[edge1_start, new_edge1_end] + D[edge2_start, new_edge2_end]
    
    improvement = old_length - new_length
    return improvement > 1e-10, improvement


def OptPPP(graph, initial_cycle: List[int]) -> Tuple[List[int], float]:
    """
    Amélioration d'un cycle par décroisements successifs (algorithme 2-opt)
    
    Principe:
    1. Partir du cycle fourni par PPP
    2. Tester tous les couples d'arêtes (i, j) avec j >= i+2
    3. Si le décroisement est avantageux, l'effectuer
    4. Répéter jusqu'à ce qu'aucune amélioration ne soit possible
    
    Cette méthode est aussi connue sous le nom de "2-opt local search"
    
    Args:
        graph: Instance de Graph
        initial_cycle: Cycle initial (généralement fourni par PPP)
        
    Returns:
        Tuple (cycle_optimisé, longueur) où:
            - cycle_optimisé: Cycle après optimisations
            - longueur: Longueur du cycle optimisé
    """
    cycle = initial_cycle.copy()
    n = len(cycle)
    improved = True
    iterations = 0
    
    # Boucle jusqu'à convergence (aucune amélioration possible)
    while improved:
        improved = False
        iterations += 1
        
        # Tester tous les couples (i, j) avec j >= i+2
        for i in range(n):
            for j in range(i + 2, n):
                # Éviter de tester les arêtes adjacentes au dernier sommet
                if i == 0 and j == n - 1:
                    continue
                
                # Vérifier si le décroisement est avantageux
                beneficial, improvement = is_swap_beneficial(graph, cycle, i, j)
                
                if beneficial:
                    # Effectuer le décroisement
                    cycle = two_opt_swap(cycle, i, j)
                    improved = True
                    break  # Recommencer depuis le début après chaque amélioration
            
            if improved:
                break
    
    # Calculer la longueur finale
    length = graph.cycle_length(cycle)
    
    return cycle, length


def OptPPP_fast(graph, initial_cycle: List[int], max_iterations: int = 1000) -> Tuple[List[int], float]:
    """
    Version plus rapide de OptPPP avec limitation du nombre d'itérations
    Utile pour de grandes instances
    
    Args:
        graph: Instance de Graph
        initial_cycle: Cycle initial
        max_iterations: Nombre maximum d'itérations
        
    Returns:
        Tuple (cycle_optimisé, longueur)
    """
    cycle = initial_cycle.copy()
    n = len(cycle)
    
    for iteration in range(max_iterations):
        improved = False
        best_improvement = 0
        best_i, best_j = None, None
        
        # Trouver la meilleure amélioration possible
        for i in range(n):
            for j in range(i + 2, n):
                if i == 0 and j == n - 1:
                    continue
                
                beneficial, improvement = is_swap_beneficial(graph, cycle, i, j)
                
                if beneficial and improvement > best_improvement:
                    best_improvement = improvement
                    best_i, best_j = i, j
                    improved = True
        
        # Appliquer la meilleure amélioration
        if improved:
            cycle = two_opt_swap(cycle, best_i, best_j)
        else:
            break  # Aucune amélioration trouvée, convergence
    
    length = graph.cycle_length(cycle)
    return cycle, length
