"""
Module de gestion des graphes pour le problème du voyageur de commerce
Références: Cormen et al., Introduction à l'algorithmique, Chapitre 37
"""

import numpy as np
import numpy.random as rd
from typing import List, Tuple

class Graph:
    """
    Classe représentant un graphe complet valué pour le PVC
    """
    
    def __init__(self, points: np.ndarray = None, n: int = None):
        """
        Initialise le graphe avec des points aléatoires ou fournis
        
        Args:
            points: Tableau numpy de forme (n, 2) avec coordonnées des points
            n: Nombre de points à générer aléatoirement si points=None
        """
        if points is not None:
            self.points = points
            self.n = len(points)
        elif n is not None:
            self.points = self._generate_random_points(n)
            self.n = n
        else:
            raise ValueError("Fournir soit points soit n")
        
        # Coordonnées x et y séparées
        self.x = self.points[:, 0]
        self.y = self.points[:, 1]
        
        # Matrice des distances euclidiennes
        self.D = self._compute_distance_matrix()
    
    def _generate_random_points(self, n: int) -> np.ndarray:
        """
        Génère n points aléatoires dans [0, 1] × [0, 1]
        
        Args:
            n: Nombre de points
            
        Returns:
            Tableau numpy de forme (n, 2)
        """
        return rd.random((n, 2))
    
    def _compute_distance_matrix(self) -> np.ndarray:
        """
        Calcule la matrice de distances euclidiennes entre tous les points
        D[i,j] = distance euclidienne entre Pi et Pj
        
        Returns:
            Matrice numpy de forme (n, n)
        """
        # Utilisation de broadcasting pour calcul vectorisé
        diff_x = self.x[:, np.newaxis] - self.x[np.newaxis, :]
        diff_y = self.y[:, np.newaxis] - self.y[np.newaxis, :]
        D = np.sqrt(diff_x**2 + diff_y**2)
        return D
    
    def cycle_length(self, cycle: List[int]) -> float:
        """
        Calcule la longueur totale d'un cycle hamiltonien
        
        Args:
            cycle: Liste d'indices des points dans l'ordre de visite
            
        Returns:
            Longueur totale du cycle
        """
        length = 0.0
        for i in range(len(cycle)):
            j = (i + 1) % len(cycle)
            length += self.D[cycle[i], cycle[j]]
        return length
    
    def is_hamiltonian(self, cycle: List[int]) -> bool:
        """
        Vérifie si un cycle est hamiltonien
        
        Args:
            cycle: Liste d'indices
            
        Returns:
            True si le cycle visite chaque sommet exactement une fois
        """
        return len(cycle) == self.n and len(set(cycle)) == self.n
    
    def get_point_coords(self, idx: int) -> Tuple[float, float]:
        """
        Retourne les coordonnées d'un point
        
        Args:
            idx: Indice du point
            
        Returns:
            Tuple (x, y)
        """
        return self.x[idx], self.y[idx]
    
    @staticmethod
    def load_from_file(filename: str) -> 'Graph':
        """
        Charge des points depuis un fichier texte
        Format: une ligne par point "(x, y)" ou "x y"
        
        Args:
            filename: Chemin du fichier
            
        Returns:
            Instance de Graph
        """
        points = []
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # Supprimer parenthèses et espaces
                line = line.replace('(', '').replace(')', '').replace(',', ' ')
                coords = line.split()
                if len(coords) >= 2:
                    x, y = float(coords[0]), float(coords[1])
                    points.append([x, y])
        
        return Graph(points=np.array(points))
    
    def save_to_file(self, filename: str):
        """
        Sauvegarde les points dans un fichier texte
        
        Args:
            filename: Chemin du fichier
        """
        with open(filename, 'w') as f:
            for i in range(self.n):
                f.write(f"({self.x[i]}, {self.y[i]})\n")
