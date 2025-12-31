"""
Algorithme d'approximation du PVC basé sur l'arbre couvrant minimum (Prim)
et parcours préfixe de l'arbre

Références: 
- Cormen et al., Introduction à l'algorithmique, Chapitre 23 (Prim)
- Cormen et al., Chapitre 37 (Approximation du PVC)
"""

import numpy as np
import heapq
from typing import List, Tuple, Dict, Set


class PrimTree:
    """
    Représentation d'un arbre couvrant construit par l'algorithme de Prim
    """
    
    def __init__(self, n: int):
        """
        Initialise un arbre avec n sommets
        
        Args:
            n: Nombre de sommets
        """
        self.n = n
        # Adjacence: dict où adj[u] contient les voisins de u
        self.adj = {i: [] for i in range(n)}
        self.edges = []  # Liste des arêtes (u, v, poids)
        self.root = None
    
    def add_edge(self, u: int, v: int, weight: float):
        """
        Ajoute une arête à l'arbre
        
        Args:
            u, v: Indices des sommets
            weight: Poids de l'arête
        """
        self.adj[u].append(v)
        self.adj[v].append(u)
        self.edges.append((u, v, weight))
    
    def get_neighbors(self, u: int) -> List[int]:
        """
        Retourne les voisins d'un sommet
        
        Args:
            u: Indice du sommet
            
        Returns:
            Liste des indices des voisins
        """
        return self.adj[u]


def prim_mst(graph, start: int) -> PrimTree:
    """
    Algorithme de Prim pour construire un arbre couvrant de poids minimum
    Version efficace avec file de priorité (tas min)
    
    Complexité: O(E log V) avec tas binaire
    
    Principe:
    1. Partir d'un sommet start
    2. Maintenir un ensemble de sommets dans l'arbre
    3. À chaque étape, ajouter l'arête de poids minimum reliant l'arbre
       à un sommet hors de l'arbre
    4. Utiliser une file de priorité pour efficacité
    
    Args:
        graph: Instance de Graph avec attributs n, D, x, y
        start: Indice du sommet de départ
        
    Returns:
        PrimTree: Arbre couvrant de poids minimum
    """
    n = graph.n
    D = graph.D
    
    # Arbre résultat
    tree = PrimTree(n)
    tree.root = start
    
    # Ensemble des sommets dans l'arbre
    in_tree = set([start])
    
    # File de priorité: (poids, sommet_dans_arbre, nouveau_sommet)
    # Contient les arêtes candidates pour extension de l'arbre
    pq = []
    
    # Initialiser avec toutes les arêtes partant de start
    for v in range(n):
        if v != start:
            heapq.heappush(pq, (D[start, v], start, v))
    
    # Construction de l'arbre
    while len(in_tree) < n and pq:
        weight, u, v = heapq.heappop(pq)
        
        # Si v est déjà dans l'arbre, ignorer cette arête
        if v in in_tree:
            continue
        
        # Ajouter l'arête (u, v) à l'arbre
        tree.add_edge(u, v, weight)
        in_tree.add(v)
        
        # Ajouter toutes les arêtes de v vers les sommets hors de l'arbre
        for w in range(n):
            if w not in in_tree:
                heapq.heappush(pq, (D[v, w], v, w))
    
    return tree


def preorder_traversal(tree: PrimTree, root: int) -> List[int]:
    """
    Parcours préfixe (DFS) d'un arbre
    
    Le parcours préfixe visite:
    1. Le nœud actuel
    2. Récursivement, tous ses sous-arbres de gauche à droite
    
    Args:
        tree: PrimTree à parcourir
        root: Sommet racine du parcours
        
    Returns:
        Liste des sommets dans l'ordre de visite préfixe
    """
    visited = set()
    order = []
    
    def dfs(node: int):
        """Parcours en profondeur récursif"""
        visited.add(node)
        order.append(node)
        
        # Visiter tous les voisins non visités
        for neighbor in tree.get_neighbors(node):
            if neighbor not in visited:
                dfs(neighbor)
    
    dfs(root)
    return order


def preorder_iterative(tree: PrimTree, root: int) -> List[int]:
    """
    Version itérative du parcours préfixe (pour éviter stack overflow)
    
    Args:
        tree: PrimTree à parcourir
        root: Sommet racine
        
    Returns:
        Liste des sommets dans l'ordre préfixe
    """
    if tree.n == 0:
        return []
    
    stack = [root]
    visited = set()
    order = []
    
    while stack:
        node = stack.pop()
        
        if node in visited:
            continue
        
        visited.add(node)
        order.append(node)
        
        # Ajouter les voisins à la pile (en ordre inverse pour garder l'ordre)
        neighbors = tree.get_neighbors(node)
        for neighbor in reversed(neighbors):
            if neighbor not in visited:
                stack.append(neighbor)
    
    return order


def OptPrim(graph, start: int = None) -> Tuple[List[int], float]:
    """
    Algorithme d'approximation du PVC basé sur Prim et parcours préfixe
    
    Principe:
    1. Construire un arbre couvrant de poids minimum avec Prim
    2. Effectuer un parcours préfixe de cet arbre
    3. L'ordre du parcours donne un cycle hamiltonien
    
    Garantie théorique (avec inégalité triangulaire):
    - La longueur du cycle ≤ 2 × longueur optimale du PVC
    
    En pratique, avec l'inégalité triangulaire, on obtient souvent de bons résultats
    
    Args:
        graph: Instance de Graph avec attributs n, D, x, y
        start: Sommet de départ (None = choix du premier point)
        
    Returns:
        Tuple (cycle, longueur) où:
            - cycle: Cycle hamiltonien (liste d'indices)
            - longueur: Longueur totale du cycle
    """
    # Validation des entrées
    if not hasattr(graph, 'n') or not hasattr(graph, 'D'):
        raise AttributeError("L'objet graph doit avoir les attributs 'n' et 'D'")
    
    if graph.n == 0:
        return [], 0.0
    
    if graph.n == 1:
        return [0], 0.0
    
    # Point de départ par défaut
    if start is None:
        start = 0
    
    # Validation du point de départ
    if start < 0 or start >= graph.n:
        raise ValueError(f"Point de départ invalide: {start} (doit être entre 0 et {graph.n-1})")
    
    # Étape 1: Construire l'arbre couvrant de poids minimum
    tree = prim_mst(graph, start)
    
    # Étape 2: Parcours préfixe de l'arbre
    cycle = preorder_traversal(tree, start)
    
    # Vérification: le cycle doit contenir tous les sommets
    if len(cycle) != graph.n:
        raise RuntimeError(f"Erreur: cycle incomplet - {len(cycle)} sommets au lieu de {graph.n}")
    
    if len(set(cycle)) != graph.n:
        raise RuntimeError(f"Erreur: cycle contient des doublons")
    
    # Étape 3: Calculer la longueur du cycle
    length = graph.cycle_length(cycle)
    
    return cycle, length


def PVCPrim(graph, start: int = None) -> Tuple[List[int], float]:
    """
    Alias pour OptPrim (nom alternatif utilisé dans le sujet)
    
    Args:
        graph: Instance de Graph
        start: Sommet de départ
        
    Returns:
        Tuple (cycle, longueur)
    """
    return OptPrim(graph, start)


def compute_mst_weight(tree: PrimTree) -> float:
    """
    Calcule le poids total de l'arbre couvrant
    
    Args:
        tree: PrimTree
        
    Returns:
        Poids total de l'arbre
    """
    return sum(weight for _, _, weight in tree.edges)


def get_mst_info(graph, start: int = 0) -> Dict:
    """
    Retourne des informations détaillées sur l'arbre couvrant
    
    Args:
        graph: Instance de Graph
        start: Sommet de départ
        
    Returns:
        Dict avec informations sur l'arbre et le cycle
    """
    tree = prim_mst(graph, start)
    cycle = preorder_traversal(tree, start)
    cycle_length = graph.cycle_length(cycle)
    mst_weight = compute_mst_weight(tree)
    
    return {
        'tree': tree,
        'cycle': cycle,
        'cycle_length': cycle_length,
        'mst_weight': mst_weight,
        'approximation_ratio': cycle_length / mst_weight if mst_weight > 0 else float('inf')
    }