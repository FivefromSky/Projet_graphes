# Projet Voyageur de Commerce (PVC)

**Université de Rouen - L3 INFO-SD**  
**AlgoGraphes 2025-26**

## Description

Ce projet implémente quatre algorithmes pour résoudre le problème du voyageur de commerce (PVC) :

1. **PPP** - Point le Plus Proche (algorithme glouton)
2. **OptPPP** - Amélioration de PPP par décroisement d'arêtes (2-opt)
3. **OptPrim** - Approximation basée sur l'arbre couvrant minimum (algorithme de Prim)
4. **HDS** - Solution exacte par Branch & Bound avec heuristique de la demi-somme

## Références

- Cormen et al., *Introduction à l'algorithmique*, Dunod 1994, Chapitre 37
- [Optimisation Pythonnienne](https://saintlaurent.enseignementlibremarche.be/wp-content/uploads/2018/03/Optimisation-Pythonnienne.pdf), Chapitre 2, pages 13-15

## Structure du projet

```
projet_pvc/
├── graph.py              # Gestion des graphes et distances
├── ppp.py                # Algorithme Point Plus Proche
├── opt_ppp.py            # Optimisation par décroisement
├── opt_prim.py           # Algorithme de Prim
├── hds.py                # Branch & Bound
├── visualization.py      # Visualisations
├── experiments.py        # Étude statistique
├── main.py               # Programme principal
├── requirements.txt      # Dépendances
└── README.md            # Ce fichier
```

## Installation

### Prérequis

- Python 3.7 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation des dépendances

```bash
pip install -r requirements.txt
```

Ou manuellement :

```bash
pip install numpy matplotlib seaborn
```

### Vérification de l'installation

```bash
python -c "import numpy, matplotlib, seaborn; print('✓ Installation OK')"
```

## Utilisation

### Programme principal (main.py)

#### Génération de points aléatoires

```bash
# Générer 20 points aléatoires
python main.py --n 20

# Avec visualisation
python main.py --n 15 --visual

# Avec solution optimale (HDS) pour n ≤ 12
python main.py --n 10 --hds --visual

# Avec graine aléatoire pour reproductibilité
python main.py --n 20 --seed 42
```

#### Chargement depuis fichier

```bash
# Charger des points depuis un fichier
python main.py --file data/points.txt --visual
```

Format du fichier (une ligne par point) :
```
(0.234, 0.567)
(0.891, 0.123)
0.456 0.789
```

#### Sauvegarde des points

```bash
# Sauvegarder les points générés
python main.py --n 25 --save output/points.txt
```

#### Options avancées

```bash
# Choisir le point de départ
python main.py --n 20 --start 5

# Aide complète
python main.py --help
```

### Étude statistique (experiments.py)

#### Lancer l'étude complète

```bash
# Étude sur 100 essais avec n=15 points
python experiments.py
```

L'étude génère automatiquement :
- Statistiques de performance
- Graphiques comparatifs
- Pourcentages d'amélioration

#### Personnalisation dans le code

Modifier directement `experiments.py` :

```python
# Ligne 278-279
stats = compare_algorithms_visual(n=15, num_trials=100)

# Modifier n et num_trials selon vos besoins
stats = compare_algorithms_visual(n=20, num_trials=50)
```

#### Étude de scalabilité

Décommenter les lignes 282-286 dans `experiments.py` :

```python
scalability = run_scalability_study(sizes=[5, 10, 15, 20, 25], num_trials=20)
times_dict = {algo: scalability[algo]['times'] for algo in ['PPP', 'OptPPP', 'OptPrim']}
plot_scalability(scalability['sizes'], times_dict)
```

## Exemples d'utilisation

### Exemple 1 : Comparaison rapide

```bash
python main.py --n 15 --visual
```

**Sortie attendue :**
- Cycles pour chaque algorithme
- Longueurs et temps d'exécution
- Graphiques visuels des cycles

### Exemple 2 : Solution optimale

```bash
python main.py --n 10 --hds --visual
```

**Note :** HDS est limité à n ≤ 12 (complexité exponentielle)

### Exemple 3 : Étude statistique complète

```bash
python experiments.py
```

**Sortie attendue :**
- 100 essais pour n=15
- Statistiques détaillées
- 4 graphiques : distributions, moyennes, histogrammes, tableau

## Description des algorithmes

### 1. PPP (Point le Plus Proche)

**Principe :** Construction gloutonne du cycle en ajoutant à chaque étape le point le plus proche.

**Complexité :** O(n³)

**Avantages :** Rapide, simple

**Inconvénients :** Peut créer des croisements

### 2. OptPPP (Optimisation par décroisement)

**Principe :** Amélioration itérative de PPP en éliminant les croisements d'arêtes (2-opt local search).

**Complexité :** O(n² × k) où k est le nombre d'itérations

**Avantages :** Amélioration significative de PPP

### 3. OptPrim (Arbre couvrant + parcours préfixe)

**Principe :** 
1. Construire un arbre couvrant de poids minimum (Prim)
2. Parcours préfixe de l'arbre pour obtenir le cycle

**Complexité :** O(n² log n)

**Garantie théorique :** Longueur ≤ 2 × optimal (avec inégalité triangulaire)

### 4. HDS (Heuristique de la Demi-Somme)

**Principe :** Branch & Bound avec évaluation par la demi-somme des arêtes minimales.

**Complexité :** Exponentielle O(n!)

**Avantage :** Solution optimale garantie

**Limitation :** Utilisable uniquement pour n ≤ 12 en pratique

## Résultats attendus

### Pour n=15, 100 essais

| Algorithme | Longueur moyenne | Écart-type | Amélioration vs PPP |
|-----------|------------------|------------|---------------------|
| PPP       | ~2.8             | ~0.3       | -                   |
| OptPPP    | ~2.6             | ~0.3       | +7-10%             |
| OptPrim   | ~2.5             | ~0.3       | +10-15%            |

### Temps d'exécution (ordre de grandeur)

| n   | PPP    | OptPPP | OptPrim | HDS        |
|-----|--------|--------|---------|------------|
| 10  | 0.001s | 0.01s  | 0.002s  | 0.1s       |
| 15  | 0.003s | 0.05s  | 0.005s  | >10s       |
| 20  | 0.008s | 0.15s  | 0.01s   | >1h        |
| 25  | 0.015s | 0.35s  | 0.02s   | Impossible |

## Personnalisation

### Modifier les paramètres d'HDS

Dans `hds.py`, ligne 199 :

```python
# Augmenter le nombre de nœuds explorés
cycle, length = HDS(graph, max_nodes=500000)

# Utiliser la borne simplifiée (plus rapide)
cycle, length = HDS(graph, use_simple_bound=True)
```

### Modifier OptPPP

Dans `opt_ppp.py`, ligne 131 :

```python
# Limiter le nombre d'itérations
cycle, length = OptPPP_fast(graph, cycle, max_iterations=500)
```

## Debugging et Troubleshooting

### Erreur : "No module named 'numpy'"

```bash
pip install numpy matplotlib seaborn
```

### HDS trop lent

Réduire n (≤ 10) ou augmenter max_nodes :

```bash
python main.py --n 8 --hds
```

### Graphiques ne s'affichent pas

Sur certains systèmes :

```python
# Ajouter au début de visualization.py
import matplotlib
matplotlib.use('TkAgg')  # ou 'Qt5Agg'
```

### Points mal formatés dans le fichier

Format accepté :
```
(0.5, 0.3)
0.5 0.3
0.5,0.3
```

## Tests unitaires (optionnel)

Créer un fichier `test_algorithms.py` :

```python
import numpy as np
from graph import Graph
from ppp import PPP
from opt_ppp import OptPPP
from opt_prim import OptPrim

# Test basique
graph = Graph(n=5)
cycle, length = PPP(graph, 0)
assert len(cycle) == 5
assert graph.is_hamiltonian(cycle)
print("✓ Tests OK")
```

## Performance et optimisation

### Pour grandes instances (n > 25)

1. Utiliser uniquement PPP et OptPrim (éviter OptPPP qui est O(n²))
2. Utiliser `OptPPP_fast` avec limitation d'itérations
3. Ne jamais utiliser HDS

### Pour études statistiques

- Réduire le nombre d'essais (50 au lieu de 100)
- Paralléliser les essais (multiprocessing)

## Contribution

Groupe de projet :
- KSO
- AA

## Licence

Projet académique - Université de Rouen 2025-26

## Contact

Pour questions : contacter le professeur ou les assistants du cours AlgoGraphes.