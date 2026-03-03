# Prof. Bruno Iochins Grisci

import random
from collections import deque


def random_instance(n, seed=None):
    """
    Create a random Stable Roommates instance with n participants.
    Names: P1..Pn.
    """
    if n % 2 != 0:
        raise ValueError("Stable roommates needs an even number of participants.")

    rng = random.Random(seed)
    people = [f"P{i}" for i in range(1, n + 1)]
    prefs = {
        p: rng.sample([q for q in people if q != p], k=n - 1)
        for p in people
    }
    return prefs


def _validate_preferences(prefs):
    names = list(prefs.keys())
    n = len(names)

    if n == 0:
        raise ValueError("Preference table cannot be empty.")
    if n % 2 != 0:
        raise ValueError("Stable roommates needs an even number of participants.")

    all_names = set(names)
    for p, pref_list in prefs.items():
        if len(pref_list) != n - 1:
            raise ValueError(f"{p} must rank exactly {n - 1} participants.")
        if p in pref_list:
            raise ValueError(f"{p} cannot rank themselves.")
        if len(set(pref_list)) != n - 1:
            raise ValueError(f"{p} has repeated names in preference list.")
        if set(pref_list) != all_names - {p}:
            raise ValueError(f"{p} must rank every other participant exactly once.")


def irving(preferences: dict[str, list[str]], verbose=False):
    """
    Run Irving's Stable Roommates algorithm (1985) in O(n^2).

    Args:
        preferences: Mapping {person: ordered list of all other participants}.
        verbose: Print proposal/rejection progress when True.

    Returns:
        A tuple (matching, total_ops), where:
        - matching is a set of (person_a, person_b) pairs, or None if no stable
          matching exists.
        - total_ops = proposals (P) + symmetric preference deletions (D) +
          rotations found (R), aligned with the visualizer counters.
    """
    _validate_preferences(preferences)

    names = list(preferences.keys())
    n = len(names)
    name_to_idx = {name: i for i, name in enumerate(names)}
    pref = [[name_to_idx[q] for q in preferences[p]] for p in names]

    # rank[p][q] = index of q in p's original list (lower is better).
    rank = [[n] * n for _ in range(n)]
    for p in range(n):
        for pos, q in enumerate(pref[p]):
            rank[p][q] = pos

    # Reduced lists in linked-list form per participant for O(1) deletions.
    left = [[-1] * n for _ in range(n)]
    right = [[-1] * n for _ in range(n)]
    active = [[False] * n for _ in range(n)]
    first = [-1] * n
    last = [-1] * n
    size = [0] * n

    for p in range(n):
        row = pref[p]
        first[p] = row[0]
        last[p] = row[-1]
        size[p] = n - 1
        for i, q in enumerate(row):
            active[p][q] = True
            left[p][q] = row[i - 1] if i > 0 else -1
            right[p][q] = row[i + 1] if i + 1 < len(row) else -1

    proposal_count = 0
    deletion_count = 0
    rotation_count = 0

    def total_ops():
        return proposal_count + deletion_count + rotation_count

    def remove_one(p, q):
        """Remove q from p's reduced list. Returns True if deletion happened."""
        nonlocal deletion_count
        if not active[p][q]:
            return False
        a = left[p][q]
        b = right[p][q]
        if a != -1:
            right[p][a] = b
        else:
            first[p] = b
        if b != -1:
            left[p][b] = a
        else:
            last[p] = a
        active[p][q] = False
        left[p][q] = -1
        right[p][q] = -1
        size[p] -= 1
        deletion_count += 1
        return True

    def delete_pair(a, b):
        """Symmetric deletion of pair (a, b) from both reduced lists."""
        changed = remove_one(a, b)
        changed = remove_one(b, a) or changed
        return changed

    def build_matching_from_first_lists():
        """Construct matching when every reduced list is a singleton."""
        matching = set()
        for p in range(n):
            q = first[p]
            if q == -1 or first[q] != p:
                return None
            if p < q:
                matching.add((names[p], names[q]))
        return matching if len(matching) == n // 2 else None

    def build_matching_from_holds(hold):
        """Construct matching directly from hold[] when every hold is mutual."""
        matching = set()
        for p in range(n):
            q = hold[p]
            if q == -1 or hold[q] != p:
                return None
            if p < q:
                matching.add((names[p], names[q]))
        return matching if len(matching) == n // 2 else None

    def all_mutual_original_top_pairs(hold):
        """
        Early-stop condition:
        if everyone ends Phase 1 proposals in mutual first-choice pairs
        (in original lists), those pairs are already stable.
        """
        for p in range(n):
            q = hold[p]
            if q == -1:
                return False
            if hold[q] != p:
                return False
            if pref[p][0] != q or pref[q][0] != p:
                return False
        return True

    # ===================
    # Phase 1: proposals
    # ===================
    hold = [-1] * n  # hold[q] = proposer currently held by q
    next_idx = [0] * n
    free = deque(range(n))

    while free:
        p = free.popleft()

        while True:
            # Advance to p's next still-active candidate in original order.
            while next_idx[p] < n - 1 and not active[p][pref[p][next_idx[p]]]:
                next_idx[p] += 1

            if next_idx[p] >= n - 1:
                if verbose:
                    print(f"{names[p]} was rejected by everyone -> no stable matching.")
                return None, total_ops()

            q = pref[p][next_idx[p]]
            next_idx[p] += 1
            proposal_count += 1

            if verbose:
                print(f"{names[p]} proposes to {names[q]}")

            cur = hold[q]
            if cur == -1:
                hold[q] = p
                if verbose:
                    print(f"{names[q]} accepts {names[p]}")
                break

            if rank[q][p] < rank[q][cur]:
                hold[q] = p
                delete_pair(cur, q)  # q rejects previous holder
                if size[cur] == 0 or size[q] == 0:
                    return None, total_ops()
                free.append(cur)
                if verbose:
                    print(f"{names[q]} switches to {names[p]} and rejects {names[cur]}")
                break

            # q rejects p
            delete_pair(p, q)
            if size[p] == 0 or size[q] == 0:
                return None, total_ops()
            if verbose:
                print(f"{names[q]} rejects {names[p]}")

    # Optimization (theoretically safe):
    # if everyone is in mutual original top-choice pairs after Phase 1 proposals,
    # that pairing is already stable and we can skip reduction + rotations.
    if all_mutual_original_top_pairs(hold):
        if verbose:
            print("Phase 1 ended with mutual top-choice pairs; halting early.")
        early_matching = build_matching_from_holds(hold)
        return early_matching, total_ops()

    # Phase 1 reduction: trim each q's list after held proposer p.
    for q in range(n):
        p = hold[q]
        if p == -1 or not active[q][p]:
            return None, total_ops()

        x = right[q][p]
        while x != -1:
            nx = right[q][x]
            delete_pair(q, x)
            if size[q] == 0 or size[x] == 0:
                return None, total_ops()
            x = nx

    # ==================================
    # Phase 2: rotations and eliminations
    # ==================================
    while True:
        start = next((p for p in range(n) if size[p] > 1), -1)
        if start == -1:
            break

        # Build p-sequence until repeated p to expose one rotation.
        seen = {}
        p_seq = []
        p = start
        while p not in seen:
            seen[p] = len(p_seq)
            p_seq.append(p)

            y = first[p]
            z = right[p][y] if y != -1 else -1  # second on p's list
            if z == -1:
                return None, total_ops()
            p = last[z]
            if p == -1:
                return None, total_ops()

        i0 = seen[p]
        rotation_p = p_seq[i0:]
        rotation_y = [first[x] for x in rotation_p]  # y_i = first on x_i list
        rotation_count += 1

        # y_i rejects x_i
        for x, y in zip(rotation_p, rotation_y):
            delete_pair(x, y)
            if size[x] == 0 or size[y] == 0:
                return None, total_ops()

        # For each i, delete from y_i all successors of x_{i-1}.
        for i, y in enumerate(rotation_y):
            x_prev = rotation_p[i - 1]  # wraps around
            if not active[y][x_prev]:
                return None, total_ops()
            t = right[y][x_prev]
            while t != -1:
                nt = right[y][t]
                delete_pair(y, t)
                if size[y] == 0 or size[t] == 0:
                    return None, total_ops()
                t = nt

    matching = build_matching_from_first_lists()
    return matching, total_ops()


def _normalize(matching):
    return {frozenset(pair) for pair in matching}


def _is_stable(preferences, matching):
    """
    Brute-force checker used only in tests.
    """
    if matching is None:
        return False

    partner = {}
    for a, b in matching:
        partner[a] = b
        partner[b] = a

    names = list(preferences.keys())
    if set(partner.keys()) != set(names):
        return False

    rank = {
        p: {q: i for i, q in enumerate(preferences[p])}
        for p in names
    }

    for x in names:
        px = partner[x]
        for y in preferences[x]:
            if y == px:
                break
            py = partner[y]
            if rank[y][x] < rank[y][py]:
                return False
    return True


def run_reference_tests():
    # Wikipedia example with stable solution:
    # expected matching = {1,6}, {2,4}, {3,5}
    wiki_case = {
        "1": ["3", "4", "2", "6", "5"],
        "2": ["6", "5", "4", "1", "3"],
        "3": ["2", "4", "5", "1", "6"],
        "4": ["5", "2", "3", "6", "1"],
        "5": ["3", "1", "2", "4", "6"],
        "6": ["5", "1", "3", "4", "2"],
    }
    wiki_expected = {
        frozenset(("1", "6")),
        frozenset(("2", "4")),
        frozenset(("3", "5")),
    }

    wiki_match, _ = irving(wiki_case)
    assert wiki_match is not None
    assert _normalize(wiki_match) == wiki_expected
    assert _is_stable(wiki_case, wiki_match)

    # Wikipedia minimal no-solution example
    wiki_no_solution = {
        "A": ["B", "C", "D"],
        "B": ["C", "A", "D"],
        "C": ["A", "B", "D"],
        "D": ["A", "B", "C"],
    }
    no_match, _ = irving(wiki_no_solution)
    assert no_match is None

    # Transcription "maniac" no-solution scenario (same structure, renamed D -> M)
    transcript_no_solution = {
        "A": ["B", "C", "M"],
        "B": ["C", "A", "M"],
        "C": ["A", "B", "M"],
        "M": ["A", "B", "C"],
    }
    no_match_m, _ = irving(transcript_no_solution)
    assert no_match_m is None

    # Early-stop case: everyone ends Phase 1 in mutual top-choice pairs.
    # The algorithm should return immediately before Phase 1 reduction.
    easy_mutual_top = {
        "A": ["B", "C", "D", "E", "F"],
        "B": ["A", "C", "D", "E", "F"],
        "C": ["D", "A", "B", "E", "F"],
        "D": ["C", "A", "B", "E", "F"],
        "E": ["F", "A", "B", "C", "D"],
        "F": ["E", "A", "B", "C", "D"],
    }
    easy_expected = {
        frozenset(("A", "B")),
        frozenset(("C", "D")),
        frozenset(("E", "F")),
    }
    easy_match, easy_ops = irving(easy_mutual_top)
    assert easy_match is not None
    assert _normalize(easy_match) == easy_expected
    assert _is_stable(easy_mutual_top, easy_match)
    assert easy_ops == 6  # 6 proposals, 0 deletions, 0 rotations.


def main():
    run_reference_tests()
    print("All Irving reference tests passed.")

    # Random demo
    demo = random_instance(8, seed=7)
    matching, ops = irving(demo)
    print("Random instance matching:", matching)
    print("Operation count:", ops)


if __name__ == "__main__":
    main()
