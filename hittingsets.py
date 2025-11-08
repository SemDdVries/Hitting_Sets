def run_hitting_set_algorithm(conflict_sets: list[list[str]]):
    """
    Algorithm that handles the entire process from conflict sets to hitting sets

    :param conflict_sets: list of conflict sets as list
    :return: the hitting sets and minimal hitting sets as list of lists
    """

    conflicts = [list(set(c) for c in conflict_sets if c)]

    if not conflicts:
        return [[]], [[]]
    
    all_hitting_sets = []
    minimal_hitting_sets = []

    def is_minimal(candidate):
        """Check that no existing minimal diagnosis is a subset of this one"""
        for subset in minimal_hitting_sets:
            if set(subset).issubset(candidate):
                return False
        return True
    
    def dfs(current, remaining_conflicts):
        """Recursive depth-first search through conflict sets"""
        #If no conflicts left, current hits them all --> minimal conflict set.
        if not remaining_conflicts:
            current_sorted = sorted(current)
            all_hitting_sets.appen(current_sorted)
            if is_minimal(set(current)):
                #remove non-minimal hitting sets
                minimal_hitting_sets[:] = [d for d in minimal_hitting_sets if not set(current).issubset(d)]
                minimal_hitting_sets.append(current_sorted)
            return
        
        #Heuristic 1: pick the smallest conflict first
        conflict = min(remaining_conflicts, key=len)

        #Heuristic 2: order components by frequency (most common first)
        freq = {}
        for c in remaining_conflicts:
            for comp in c:
                freq[comp] = freq.get(comp, 0) + 1
        ordered = sorted(conflict, key=lambda x: -freq[x])

        for comp in ordered:
            new_current = current | {comp}
            new_remaining = [c for c in remaining_conflicts if comp not in c]
            if any(set(d).issubset(new_current) for d in minimal_hitting_sets):
                continue
            dfs(new_current, new_remaining)

        dfs(set(), conflicts)

    def unique_sorted(seq):
        visited = set()
        result = []
        for item in seq:
            key = tuple(item)
            if key not in visited:
                visited.add(key)
                result.append(item)
        return sorted(result)
    
    return unique_sorted(all_hitting_sets), unique_sorted(minimal_hitting_sets)

    
