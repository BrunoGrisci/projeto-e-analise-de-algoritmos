# Prof. Bruno Iochins Grisci

import random
from collections import deque
import matplotlib.pyplot as plt

def plot_curves(i_rand, i_hard, i_easy):
    # Build aligned x/y arrays
    xs = sorted(i_rand.keys())
    y_rand = [i_rand[n] for n in xs]
    y_hard = [i_hard[n] for n in xs]
    y_easy = [i_easy[n] for n in xs]

    # (Optional) theoretical references
    y_linear = xs                              # ~ n      (easy)
    y_quadratic_half = [n*(n+1)//2 for n in xs]     # ~ n^2/2  (hard-ish)
    y_quadratic = [n*n for n in xs]     # ~ n^2 (hard-ish)

    plt.figure(figsize=(8, 5))
    plt.plot(xs, y_rand, marker='o', label='Random')
    plt.plot(xs, y_hard, marker='s', label='Hard-ish (identical men)')
    plt.plot(xs, y_easy, marker='^', label='Easy (unique top choices)')

    # (Optional) add theory lines
    plt.plot(xs, y_linear, linestyle='--', label='~ n (theory)')
    plt.plot(xs, y_quadratic_half, linestyle='--', label='~ n(n+1)/2 (theory)')
    plt.plot(xs, y_quadratic, linestyle='--', label='~ n*n (theory)')

    plt.title('Gale–Shapley: iterations vs problem size n')
    plt.xlabel('n (|M| = |W|)')
    plt.ylabel('Number of loop iterations')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    #plt.yscale('log')
    plt.show()

def random_instance(n, seed=None):
    """
    Create a random one-to-one instance with n 'men' and n 'women'.
    Names: M1..Mn and W1..Wn.
    """
    rng = random.Random(seed)
    men = [f"M{i}" for i in range(1, n+1)]
    women = [f"W{i}" for i in range(1, n+1)]

    m_prefs = {m: rng.sample(women, k=n) for m in men}
    w_prefs = {w: rng.sample(men, k=n) for w in women}
    return m_prefs, w_prefs

def worstish_instance(n):
    """
    Identical men, reversed women (tends to increase proposals).
    """
    men = [f"M{i}" for i in range(1, n+1)]
    women = [f"W{i}" for i in range(1, n+1)]
    # All men rank W1 > W2 > ... > Wn
    m_prefs = {m: women[:] for m in men}
    # Each woman ranks men in reverse (Mn > ... > M1)
    rev_men = men[::-1]
    w_prefs = {w: rev_men[:] for w in women}
    return m_prefs, w_prefs    

def easy_instance(n):
    """
    Each man’s top choice is unique and each woman ranks her designated man first. Then everyone gets engaged on their first proposal.
    """
    men   = [f"M{i}" for i in range(1, n+1)]
    women = [f"W{i}" for i in range(1, n+1)]
    # Mi's top choice is Wi; each woman Wi ranks Mi first
    m_prefs = {
        men[i]: [women[i]] + [w for w in women if w != women[i]] 
        for i in range(n)
    }
    w_prefs = {
        women[i]: [men[i]] + [m for m in men if m != men[i]]
        for i in range(n)
    }
    return m_prefs, w_prefs

def gale_shapley(m_prefs: dict[str, list[str]], w_prefs: dict[str, list[str]], verbose=False):
    """
    m_prefs: {man: [women in descending preference]}
    w_prefs: {woman: [men in descending preference]}
    returns: set of (man, woman) pairs
    """
    # Precompute each woman's ranking of men for comparisons
    w_rank = {w: {m: i for i, m in enumerate(pref_list)} for w, pref_list in w_prefs.items()}

    # https://www.geeksforgeeks.org/python/deque-in-python/
    free_men = deque(m_prefs.keys())        # all men start free
    next_idx = {m: 0 for m in m_prefs}      # next woman to propose to per man
    engaged_to = {}                         # woman -> man (current fiancé)

    i_loop = 0
    while free_men:
        i_loop += 1
        m = free_men.popleft()

        # If m has already proposed to every woman, skip (no match possible)
        if next_idx[m] >= len(m_prefs[m]):
            if verbose: print(f'{m} has already proposed to everyone.')
            continue

        # Highest-ranked woman m hasn't proposed to yet
        w = m_prefs[m][next_idx[m]]
        next_idx[m] += 1

        if verbose: print(f'{m} proposes to {w}.')        

        if w not in engaged_to:             # w is free
            engaged_to[w] = m               # (m, w) become engaged
            if verbose: print(f'{w} is free, {m} and {w} become engaged.')     
        else:
            m_prime = engaged_to[w]         # w is engaged to m'
            # If w prefers current fiancé m' over m
            if w_rank[w][m_prime] < w_rank[w][m]:
                # m remains free; try next woman later
                free_men.append(m)
                if verbose: print(f'{m} remains free.')   
            else:
                # w prefers m to m'
                engaged_to[w] = m           # (m, w) become engaged
                free_men.append(m_prime)    # m' becomes free
                if verbose: print(f'{m} and {w} become engaged, {m_prime} becomes free.')   

        # If m still hasn't proposed to everyone and is free, he'll re-enter loop via queue
        # Loop continues while there exists a free man who hasn't proposed to all women

        if verbose: print(engaged_to)

    # Build result set S of engaged pairs
    return {(m, w) for w, m in engaged_to.items()}, i_loop

def main():

    # Demo: https://www.cs.princeton.edu/~wayne/kleinberg-tardos/pdf/01DemoGaleShapley.pdf
    # hospitals’ preference lists
    HPL = {           #1st      2nd       3rd         4th       5th 
        'Atlanta': ['Wayne',  'Val',     'Yolanda', 'Zeus',   'Xavier'],
        'Boston':  ['Yolanda','Wayne',   'Val',     'Xavier', 'Zeus'],
        'Chicago': ['Wayne',  'Zeus',    'Xavier',  'Yolanda','Val'],
        'Detroit': ['Val',    'Yolanda', 'Xavier',  'Wayne',  'Zeus'],
        'El Paso': ['Wayne',  'Yolanda', 'Val',     'Zeus',   'Xavier'],
    }

    # students’ preference lists
    SPL = {           #1st      2nd       3rd         4th       5th 
    'Val':     ['El Paso', 'Atlanta', 'Boston',  'Detroit', 'Chicago'],
    'Wayne':   ['Chicago', 'Boston',  'Detroit', 'Atlanta', 'El Paso'],
    'Xavier':  ['Boston',  'Chicago', 'Detroit', 'El Paso', 'Atlanta'],
    'Yolanda': ['Atlanta', 'El Paso', 'Detroit', 'Chicago', 'Boston'],
    'Zeus':    ['Detroit', 'Boston',  'El Paso', 'Chicago', 'Atlanta'],
    }

    # Pior caso dos slides de aula
    HOMENS = {
        'V': ['A', 'B', 'C', 'D', 'E'],
        'W': ['B', 'C', 'D', 'A', 'E'],
        'X': ['C', 'D', 'A', 'B', 'E'],
        'Y': ['D', 'A', 'B', 'C', 'E'],
        'Z': ['A', 'B', 'C', 'D', 'E'],
    }

    MULHERES = {
       'A': ['W', 'X', 'Y', 'Z', 'V'],
       'B': ['X', 'Y', 'Z', 'V', 'W'],
       'C': ['Y', 'Z', 'V', 'W', 'X'],
       'D': ['Z', 'V', 'W', 'X', 'Y'],
       'E': ['V', 'W', 'X', 'Y', 'Z'],
    }

    # Demo:
    print(gale_shapley(HPL, SPL, True))

    # Worst case:
    print(gale_shapley(HOMENS, MULHERES, True))

    # Analysis:    
    i_rand = {}
    i_hard = {}
    i_easy = {}

    for n in range(10, 1000, 100):
        mp, wm = random_instance(n)
        i_rand[n] = gale_shapley(mp, wm)[1]
    
    for n in range(10, 1000, 100):
        mp, wm = worstish_instance(n)
        i_hard[n] = gale_shapley(mp, wm)[1]     

    for n in range(10, 1000, 100):
        mp, wm = easy_instance(n)
        i_easy[n] = gale_shapley(mp, wm)[1] 

    print('RANDOM')
    print(i_rand)
    print('WORST')
    print(i_hard)
    print('EASY')
    print(i_easy)

    plot_curves(i_rand, i_hard, i_easy)
    

if __name__ == '__main__': 
    main()