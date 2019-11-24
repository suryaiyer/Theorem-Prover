import copy
from CNF_converter import toCNF


# Check the resolution if the query is true or false
def PL_resolution(KB, a):
    new = []
    clauses = KB
    clauses.append(a)
    while True:
        n = len(clauses)

        pair = [(clauses[i], clauses[j]) for i in range(n) for j in range(i + 1, n)]

        for (Ci, Cj) in pair:
            resolvents = PL_Resolve(Ci, Cj)

            if set() in resolvents:
                return True

            if resolvents and len(resolvents[0]) <= max(len(Ci), len(Cj)):
                new = union(resolvents, new)

        if is_subset(clauses, new) and len(new) < len(clauses):
            return False

        for clause in new:
            if clause not in clauses:
                clauses.append(clause)
        new = []


# Resolvent function that return a list with different resolve set
def PL_Resolve(Ci, Cj):
    clause = []

    for i in Ci:
        for j in Cj:
            if (i == '!' + j) or (j == '!' + i):
                clause_set = unique(remove(i, set(Ci)), remove(j, set(Cj)))
                copy_clause_set = copy.deepcopy(clause_set)
                if len(clause_set) > 1:
                    for item1 in copy_clause_set:
                        for item2 in copy_clause_set:
                            if item1 != item2 and (item1 == '!' + item2 or item2 == '!' + item1):
                                clause_set = []

                    if clause_set:
                        clause.append(clause_set)
                else:
                    clause.append(clause_set)

    return clause


# Remove 2 items that complement i.e., A and !A
def remove(clause, item):
    item.remove(clause)
    return item


# Return the set that unique and sorted
def unique(Ci, Cj):
    unique_set = Ci
    for item in Cj:
        unique_set.add(item)
    return unique_set


# add the set to list set
def union(sets, list_set):
    list_set = list(list_set)

    for s in sets:
        check = False
        for ls in list_set:
            if ls == s:
                check = True
        if not check:
            list_set.append(s)
    return list_set


# check if set is the subset of list set
def is_subset(list_set, subsets):
    check = False

    for subset in subsets:
        if subset in list_set:
            check = True
            break
    return check
