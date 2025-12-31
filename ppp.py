"""
Algorithme du Point le Plus Proche (PPP) pour le PVC
Stratégie gloutonne d'insertion du point le plus proche

Référence: Optimisation Pythonnienne, Chapitre 2
"""

import numpy as np
from typing import List, Tuple, Set


def PPP(graph, Q_idx: int) -> Tuple[List[int], float]:
    """
    Algorithme du Point le Plus Proche (Nearest Neighbor)
    
    Principe:
    1. Démarrer avec un cycle contenant uniquement Q
    2. À chaque étape, trouver le point non visité le plus proche d'un point du cycle
    3. Insérer ce point dans le cycle à la position optimale
    4. Répéter jusqu'à ce que tous les points soient dans le cycle
    
    Args:
        graph: Instance de Graph contenant les points et la matrice de distances
        Q_idx: Indice du point de départ
        
    Returns:
        Tuple (cycle, longueur) où:
            - cycle: Liste d'indices représentant l'ordre de visite
            - longueur: Longueur totale du cycle
    """
    n = graph.n
    D = graph.D
    
    # Initialisation: cycle avec un seul point Q
    cycle = [Q_idx]
    remaining = set(range(n)) - {Q_idx}
    
    # Construction du cycle par ajouts successifs
    while remaining:
        min_distance = float('inf')
        best_point = None
        best_position = None
        
        # Trouver le point non visité le plus proche du cycle
        for point in remaining:
            for j, cycle_point in enumerate(cycle):
                dist = D[point, cycle_point]
                
                if dist < min_distance:
                    min_distance = dist
                    best_point = point
                    # Position d'insertion : après cycle_point
                    best_position = j
        
        # Insertion du point dans le cycle
        # On insère après best_position, en cherchant la meilleure position
        # entre best_position et le point suivant
        best_insert_pos = best_position + 1
        min_cost_increase = float('inf')
        
        # Tester toutes les positions d'insertion possibles
        for insert_pos in range(len(cycle) + 1):
            # Calculer le coût d'insertion à cette position
            prev_idx = cycle[insert_pos - 1] if insert_pos > 0 else cycle[-1]
            next_idx = cycle[insert_pos] if insert_pos < len(cycle) else cycle[0]
            
            # Coût avant insertion
            old_cost = D[prev_idx, next_idx]
            # Coût après insertion
            new_cost = D[prev_idx, best_point] + D[best_point, next_idx]
            cost_increase = new_cost - old_cost
            
            if cost_increase < min_cost_increase:
                min_cost_increase = cost_increase
                best_insert_pos = insert_pos
        
        # Insérer le point à la meilleure position
        cycle.insert(best_insert_pos, best_point)
        remaining.remove(best_point)
    
    # Calculer la longueur finale du cycle
    length = graph.cycle_length(cycle)
    
    return cycle, length


def PPP_simple(graph, Q_idx: int) -> Tuple[List[int], float]:
    """
    Version simplifiée de PPP : insertion toujours après le point le plus proche
    Cette version est plus rapide mais peut donner des résultats légèrement moins bons
    
    Args:
        graph: Instance de Graph
        Q_idx: Indice du point de départ
        
    Returns:
        Tuple (cycle, longueur)
    """
    n = graph.n
    D = graph.D
    
    cycle = [Q_idx]
    remaining = set(range(n)) - {Q_idx}
    
    while remaining:
        min_distance = float('inf')
        best_point = None
        insert_after = None
        
        # Trouver le point le plus proche et le point du cycle associé
        for point in remaining:
            for cycle_point in cycle:
                dist = D[point, cycle_point]
                if dist < min_distance:
                    min_distance = dist
                    best_point = point
                    insert_after = cycle_point
        
        # Insérer après le point le plus proche
        pos = cycle.index(insert_after)
        cycle.insert(pos + 1, best_point)
        remaining.remove(best_point)
    
    length = graph.cycle_length(cycle)
    return cycle, length
