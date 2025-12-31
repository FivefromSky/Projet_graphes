"""
Algorithme exact Branch & Bound pour le PVC
Utilise l'heuristique de la demi-somme pour l'évaluation

Référence: Optimisation Pythonnienne, pages 13-15
"""

import numpy as np
import heapq
from typing import List, Tuple, Set, Optional


class Node:
    """
    Nœud dans l'arbre de recherche Branch & Bound
    Représente un état partiel de construction du cycle
    """
    
    def __init__(self, path: List[int], remaining: Set[int], cost: float, bound: float):
        """
        Args:
            path: Chemin partiel (liste ordonnée des sommets visités)
            remaining: Ensemble des sommets non encore visités
            cost: Coût réel du chemin partiel
            bound: Borne inférieure estimée du coût total
        """
        self.path = path
        self.remaining = remaining
        self.cost = cost
        self.bound = bound
    
    def __lt__(self, other):
        """Comparaison pour la file de priorité (minimum en premier)"""
        return self.bound < other.bound
    
    def __repr__(self):
        return f"Node(path={self.path}, cost={self.cost:.2f}, bound={self.bound:.2f})"


def compute_half_sum_bound(graph, path: List[int], remaining: Set[int], current_cost: float) -> float:
    """
    Calcule la borne inférieure avec l'heuristique de la demi-somme
    
    Principe:
    Pour chaque sommet non visité, on prend la moitié de la somme des deux
    arêtes les plus courtes qui le relient (une pour entrer, une pour sortir).
    
    Pour le dernier sommet du chemin et le premier, on prend également
    les arêtes de connexion minimales.
    
    Args:
        graph: Instance de Graph avec attributs n et D
        path: Chemin partiel actuel
        remaining: Sommets non encore visités
        current_cost: Coût du chemin partiel
        
    Returns:
        Borne inférieure du coût total
    """
    if not remaining:
        # Cas terminal: retour au point de départ
        return current_cost + graph.D[path[-1], path[0]]
    
    D = graph.D
    bound = current_cost
    
    # Pour chaque sommet non visité, ajouter la demi-somme
    # des deux arêtes minimales
    for v in remaining:
        # Trouver les deux distances minimales depuis v
        distances = []
        
        # Distances vers les sommets déjà dans le chemin
        for u in path:
            distances.append(D[v, u])
        
        # Distances vers les autres sommets non visités
        for u in remaining:
            if u != v:
                distances.append(D[v, u])
        
        # Trier et prendre les deux plus petites
        distances.sort()
        if len(distances) >= 2:
            bound += (distances[0] + distances[1]) / 2.0
        elif len(distances) == 1:
            bound += distances[0]
    
    # Ajouter la demi-somme pour le dernier sommet du chemin
    # (il faut encore une arête sortante)
    last_vertex = path[-1]
    min_out = float('inf')
    for v in remaining:
        if D[last_vertex, v] < min_out:
            min_out = D[last_vertex, v]
    
    # Ajouter la demi-somme pour le premier sommet
    # (il faut encore une arête entrante)
    first_vertex = path[0]
    min_in = float('inf')
    for v in remaining:
        if D[v, first_vertex] < min_in:
            min_in = D[v, first_vertex]
    
    bound += (min_out + min_in) / 2.0
    
    return bound


def compute_simple_bound(graph, path: List[int], remaining: Set[int], current_cost: float) -> float:
    """
    Borne inférieure simplifiée (plus rapide mais moins précise)
    Utilise simplement le coût actuel + arête minimale de retour
    
    Args:
        graph: Instance de Graph avec attributs n et D
        path: Chemin partiel
        remaining: Sommets restants
        current_cost: Coût actuel
        
    Returns:
        Borne inférieure simple
    """
    if not remaining:
        return current_cost + graph.D[path[-1], path[0]]
    
    # Coût actuel + estimation minimale pour visiter les sommets restants
    D = graph.D
    bound = current_cost
    
    # Distance minimale entre le dernier sommet visité et les restants
    if remaining:
        min_dist = min(D[path[-1], v] for v in remaining)
        bound += min_dist
        
        # Distance minimale entre les sommets restants
        if len(remaining) > 1:
            remaining_list = list(remaining)
            min_remaining = float('inf')
            for i, v in enumerate(remaining_list):
                for u in remaining_list[i+1:]:
                    if D[v, u] < min_remaining:
                        min_remaining = D[v, u]
            bound += min_remaining * (len(remaining) - 1)
    
    return bound


def HDS(graph, use_simple_bound: bool = False, max_nodes: int = 100000, verbose: bool = True) -> Tuple[List[int], float]:
    """
    Algorithme Branch & Bound avec Heuristique de la Demi-Somme
    Recherche exacte de la solution optimale au PVC
    
    Principe:
    1. Explorer l'arbre des possibilités de manière intelligente
    2. Utiliser une file de priorité pour traiter les nœuds les plus prometteurs
    3. Élaguer les branches dont la borne dépasse la meilleure solution trouvée
    4. Garantit de trouver la solution optimale
    
    Complexité: Exponentielle dans le pire cas, mais élagage efficace en pratique
    
    Args:
        graph: Instance de Graph avec attributs n et D
        use_simple_bound: Si True, utilise la borne simplifiée (plus rapide)
        max_nodes: Nombre maximum de nœuds à explorer (protection)
        verbose: Si True, affiche les statistiques
        
    Returns:
        Tuple (cycle_optimal, longueur_minimale)
        
    Raises:
        AttributeError: Si graph n'a pas les attributs requis
        RuntimeError: Si aucune solution n'est trouvée
    """
    # Validation des entrées
    if not hasattr(graph, 'n') or not hasattr(graph, 'D'):
        raise AttributeError("L'objet graph doit avoir les attributs 'n' et 'D'")
    
    n = graph.n
    
    # Cas particuliers
    if n == 0:
        return [], 0.0
    if n == 1:
        return [0], 0.0
    if n == 2:
        return [0, 1], graph.D[0, 1] + graph.D[1, 0]
    
    # Choix de la fonction de borne
    bound_func = compute_simple_bound if use_simple_bound else compute_half_sum_bound
    
    # Initialisation
    start = 0  # Partir du premier sommet
    initial_remaining = set(range(1, n))
    initial_bound = bound_func(graph, [start], initial_remaining, 0.0)
    
    # File de priorité: on explore les nœuds avec la plus petite borne en premier
    pq = []
    initial_node = Node([start], initial_remaining, 0.0, initial_bound)
    heapq.heappush(pq, initial_node)
    
    # Meilleure solution trouvée
    best_cost = float('inf')
    best_cycle = None
    
    # Compteurs statistiques
    nodes_explored = 0
    nodes_pruned = 0
    
    while pq and nodes_explored < max_nodes:
        # Extraire le nœud le plus prometteur
        current = heapq.heappop(pq)
        nodes_explored += 1
        
        # Élagage: si la borne de ce nœud dépasse la meilleure solution,
        # toutes ses extensions seront aussi mauvaises
        if current.bound >= best_cost:
            nodes_pruned += 1
            continue
        
        # Si le chemin est complet, c'est un cycle hamiltonien
        if not current.remaining:
            # Calculer le coût total (avec retour au départ)
            total_cost = current.cost + graph.D[current.path[-1], current.path[0]]
            
            if total_cost < best_cost:
                best_cost = total_cost
                best_cycle = current.path.copy()
            continue
        
        # Étendre le nœud: essayer d'ajouter chaque sommet restant
        last_vertex = current.path[-1]
        
        for next_vertex in current.remaining:
            # Nouveau chemin
            new_path = current.path + [next_vertex]
            new_remaining = current.remaining - {next_vertex}
            new_cost = current.cost + graph.D[last_vertex, next_vertex]
            
            # Calculer la borne pour ce nouveau nœud
            new_bound = bound_func(graph, new_path, new_remaining, new_cost)
            
            # Élagage: ne pas ajouter si la borne dépasse la meilleure solution
            if new_bound < best_cost:
                new_node = Node(new_path, new_remaining, new_cost, new_bound)
                heapq.heappush(pq, new_node)
            else:
                nodes_pruned += 1
    
    # Vérification de la solution
    if best_cycle is None:
        raise RuntimeError("Aucune solution trouvée. Augmentez max_nodes.")
    
    # Statistiques
    if verbose:
        if nodes_explored >= max_nodes:
            print(f"⚠️  Limite atteinte: {max_nodes} nœuds explorés")
            print(f"   Solution peut ne pas être optimale")
        
        print(f"📊 Statistiques Branch & Bound:")
        print(f"   - Nœuds explorés: {nodes_explored}")
        print(f"   - Nœuds élagués: {nodes_pruned}")
        total_nodes = nodes_explored + nodes_pruned
        if total_nodes > 0:
            print(f"   - Efficacité élagage: {100*nodes_pruned/total_nodes:.1f}%")
    
    return best_cycle, best_cost


def HDS_timeout(graph, timeout_seconds: float = 60.0, verbose: bool = True) -> Tuple[Optional[List[int]], Optional[float]]:
    """
    Version avec timeout pour éviter les calculs trop longs
    Compatible Windows et Unix
    
    Args:
        graph: Instance de Graph
        timeout_seconds: Temps maximum d'exécution
        verbose: Si True, affiche les informations
        
    Returns:
        Tuple (cycle, longueur) ou (None, None) si timeout
    """
    import time
    import threading
    
    result = {'cycle': None, 'length': None, 'completed': False}
    
    def run_hds():
        try:
            cycle, length = HDS(graph, verbose=verbose)
            result['cycle'] = cycle
            result['length'] = length
            result['completed'] = True
        except Exception as e:
            if verbose:
                print(f"❌ Erreur HDS: {e}")
    
    # Lancer dans un thread
    thread = threading.Thread(target=run_hds)
    thread.daemon = True
    thread.start()
    
    # Attendre le timeout
    thread.join(timeout=timeout_seconds)
    
    if result['completed']:
        return result['cycle'], result['length']
    else:
        if verbose:
            print(f"⏱️  Timeout après {timeout_seconds}s")
        return None, None


def HDS_silent(graph, use_simple_bound: bool = False, max_nodes: int = 100000) -> Tuple[List[int], float]:
    """
    Version silencieuse de HDS (sans affichage)
    Utile pour les études statistiques
    
    Args:
        graph: Instance de Graph
        use_simple_bound: Si True, utilise la borne simplifiée
        max_nodes: Nombre maximum de nœuds
        
    Returns:
        Tuple (cycle, longueur)
    """
    return HDS(graph, use_simple_bound=use_simple_bound, max_nodes=max_nodes, verbose=False)