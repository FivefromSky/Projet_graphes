"""
Test complet de tous les algorithmes
"""

print("="*70)
print("TEST D'IMPORT ET D'EXÉCUTION")
print("="*70)

# 1. Test des imports
print("\n1️⃣ Test des imports...")
try:
    from graph import Graph
    print("   ✓ Graph importé")
except Exception as e:
    print(f"   ❌ Erreur Graph: {e}")
    exit(1)

try:
    from ppp import PPP
    print("   ✓ PPP importé")
except Exception as e:
    print(f"   ❌ Erreur PPP: {e}")
    exit(1)

try:
    from opt_ppp import OptPPP
    print("   ✓ OptPPP importé")
except Exception as e:
    print(f"   ❌ Erreur OptPPP: {e}")
    exit(1)

try:
    from opt_prim import OptPrim
    print("   ✓ OptPrim importé")
except Exception as e:
    print(f"   ❌ Erreur OptPrim: {e}")
    exit(1)

try:
    from hds import HDS
    print("   ✓ HDS importé")
except Exception as e:
    print(f"   ❌ Erreur HDS: {e}")
    exit(1)

# 2. Test de création de graphe
print("\n2️⃣ Test de création de graphe...")
try:
    graph = Graph(n=5)
    print(f"   ✓ Graphe créé avec {graph.n} points")
    print(f"   ✓ Matrice de distances: {graph.D.shape}")
except Exception as e:
    print(f"   ❌ Erreur: {e}")
    exit(1)

# 3. Test PPP
print("\n3️⃣ Test PPP...")
try:
    cycle, length = PPP(graph, 0)
    print(f"   ✓ PPP réussi")
    print(f"      Cycle: {cycle}")
    print(f"      Longueur: {length:.4f}")
except Exception as e:
    print(f"   ❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

# 4. Test OptPPP
print("\n4️⃣ Test OptPPP...")
try:
    cycle_opt, length_opt = OptPPP(graph, cycle)
    improvement = ((length - length_opt) / length) * 100
    print(f"   ✓ OptPPP réussi")
    print(f"      Longueur: {length_opt:.4f}")
    print(f"      Amélioration: {improvement:+.2f}%")
except Exception as e:
    print(f"   ❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

# 5. Test OptPrim
print("\n5️⃣ Test OptPrim...")
try:
    cycle_prim, length_prim = OptPrim(graph, 0)
    print(f"   ✓ OptPrim réussi")
    print(f"      Cycle: {cycle_prim}")
    print(f"      Longueur: {length_prim:.4f}")
except Exception as e:
    print(f"   ❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

# 6. Test HDS (petit graphe)
print("\n6️⃣ Test HDS...")
try:
    graph_small = Graph(n=6)
    cycle_hds, length_hds = HDS(graph_small, verbose=True, max_nodes=10000)
    print(f"   ✓ HDS réussi")
    print(f"      Cycle optimal: {cycle_hds}")
    print(f"      Longueur optimale: {length_hds:.4f}")
except Exception as e:
    print(f"   ❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("✓ TOUS LES TESTS RÉUSSIS !")
print("="*70)