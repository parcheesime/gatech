#!/usr/bin/env python3

import json
print(f"\n* JSON module version: {json.__version__}")

import pickle

def data_fn(basename, dirname="./resource/asnlib/publicdata/"):
    return f"{dirname}{basename}"

def file_exists(fn, data_fn=data_fn):
    from os.path import isfile
    return isfile(data_fn(fn))

def load_json(fn, data_fn=data_fn):
    infile = data_fn(fn)
    with open(infile, "rt") as fp:
        data = json.load(fp)
    print(f"'{infile}': {len(data)}")
    return data

def inspect_data(v):
    from json import dumps
    print(dumps(v, indent=4))

def save_json(data, fn, data_fn=data_fn):
    outfile = data_fn(fn)
    with open(outfile, "wt") as fp:
        json.dump(data, fp, indent=4)
    print(f"'{outfile}': {len(data)}")

def load_pickle(fn, data_fn=data_fn):
    infile = data_fn(fn)
    with open(infile, 'rb') as fp:
        p = pickle.load(fp)
    return p

def save_pickle(pyobj, fn, data_fn=data_fn):
    outfile = data_fn(fn)
    with open(outfile, 'wb') as fp:
        pickle.dump(pyobj, fp)

def load_freq_table(infile='english_letter_pair_frequencies.txt'):
    from collections import defaultdict
    freq_table = defaultdict(dict)
    with open(data_fn(infile), 'rt') as fp:
        header = fp.readline()[:-1].split(',') # read line and strip newline
        for line in fp.readlines():
            line = line[:-1].split(',') # remove newline
            x = line[0]
            for y, p_str in zip(header[1:], line[1:]):
                freq_table[x][y] = float(p_str)
    return freq_table

freq_2nd = load_freq_table()
freq_1st = freq_2nd[' ']

def gen_word(max_len=16, freq_1st=freq_1st, freq_2nd=freq_2nd):
    from random import randint, choices
    def select(p, spaces=True):
        from random import choices
        letters = list(p.keys())
        weights = list(p.values())
        if not spaces:
            letters = letters[:-1]
            weights = weights[:-1]
        return choices(letters, weights=weights)[0]
    s = select(freq_1st, spaces=False)
    while not s[-1].isspace():
        s += select(freq_2nd[s[-1]], spaces=(len(s) >= 2) or (s in ['a', 'i']))
    return s.strip()

def ex0__gen_random_vote_result():
    from random import random, choice, randint
    v = {gen_word(): gen_word()}
    err = False
    if random() < 0.25:
        v["vote_type"] = gen_word()
        err = True
    else:
        v["vote_type"] = choice(["1/2", "YEA-AND-NAY", "RECORDED VOTE"])
    v["total"] = {"yes": randint(1, 100),
                  "no": randint(1, 100),
                  "present": randint(1, 100),
                  "not_voting": randint(1, 100)}
    if random() < 0.25:
        key = choice(["yes", "no", "present", "not_voting"])
        del v["total"][key]
        err = True
    return v, err

def ex0__check(filter_votes, n_max=10):
    from random import randint
    n = randint(1, 10)
    V_in = []
    V_in_copy = []
    V_out = []
    for i in range(n):
        v, err = ex0__gen_random_vote_result()
        V_in.append(v)
        V_in_copy.append(v.copy())
        if not err:
            V_out.append(V_in_copy[-1])
    try:
        V = filter_votes(V_in)
        assert len(V) == len(V_out), \
               f"*** Your result has {len(V)} items whereas we expected {len(V_out)}. ***"
        assert all(a == b for a, b in zip(V, V_out)), \
               f"*** Your result does not match what we expected. ***"
    except:
        print("=== Test case ===")
        print("* Input:")
        inspect_data(V_in_copy)
        print("\n* Expected output:")
        inspect_data(V_out)
        if 'V' in locals():
            print("\n* Your output:")
            inspect_data(V)
        raise

def ex1__gen_random_vote_result():
    from random import random, randint
    v = {gen_word(): gen_word()}
    n_yes = randint(1, 100)
    if random() < 0.5: # pass
        n_no = n_yes - randint(1, n_yes)
        passed = True
    elif random() < 0.25: # fail with same vote count
        n_no = n_yes
        passed = False
    else: # fail with count that is strictly less than
        n_no = n_yes + randint(1, 5)
        passed = False
    v["total"] = {"yes": n_yes, "no": n_no, "present": randint(0, 10), "not_voting": randint(0, 10)}
    return v, passed

def ex1__check(is_passing):
    v, passed = ex1__gen_random_vote_result()
    try:
        your_result = is_passing(v)
        assert your_result == passed, \
               f"*** You returned {your_result} instead of {passed}. ***"
    except:
        print("=== Test case ===")
        print("* Input:")
        inspect_data(v)
        raise

def ex2__gen_random_vote_result():
    from random import random, randint
    def counts(n_yes, n_no, n_present, n_not_voting):
        return {"yes": n_yes, "no": n_no, "present": n_present, "not_voting": n_not_voting}
    def split(n):
        d = randint(0, n)
        r = n - d
        return d, r
    def split_counts(c, p):
        a, b = {}, {}
        na, nb = 0, 0
        for k in ["yes", "no", "present", "not_voting"]:
            a[k], b[k] = split(c[k])
            na, nb = na+a[k], nb+b[k]
        return a, a[p]/na if na > 0 else 0, b, b[p]/nb if nb > 0 else 0
    v = {gen_word(): gen_word()}
    n_yes = randint(1, 100)
    if random() < 0.5: # pass
        n_no = n_yes - randint(1, n_yes)
        passed = True
    else: # fail with count that is strictly less than
        n_no = n_yes + randint(0, 5)
        passed = False
    n_present = randint(0, 10)
    n_not_voting = randint(0, 10)
    v["total"] = counts(n_yes, n_no, n_present, n_not_voting)
    v["passed"] = passed
    v["democratic"], d, v["republican"], r = split_counts(v["total"], "yes" if passed else "no")
    return v, abs(d-r)

def ex2__check(calc_partisan_vote_gap):
    from math import isclose
    v, g = ex2__gen_random_vote_result()
    try:
        your_result = calc_partisan_vote_gap(v)
        assert isclose(your_result, g), \
               f"*** You returned {your_result} instead of {g}. ***"
    except:
        print("=== Test case ===")
        print("* Input:")
        inspect_data(v)
        raise

def ex3__gen_random_date(yyyy=None, mm=None, dd=None):
    from random import randint
    if yyyy is None:
        yyyy = randint(1992, 2020)
    if mm is None:
        mm = randint(1, 12)
    if dd is None:
        dd = randint(1, 31) if mm in {1, 3, 5, 7, 8, 10, 12} else randint(1, 28) if mm == 2 else randint(1, 30)
    return f"{yyyy:04d}-{mm:02d}-{dd:02d}"

def ex3__gen_random_vote_result(yyyy=None):
    from random import random, randint
    g = random()
    v = {gen_word(): gen_word(),
         "date": ex3__gen_random_date(yyyy=yyyy),
         "gap": g}
    return v, g

def ex3__gen_random_vote_results():
    from random import sample, randint, shuffle
    from statistics import mean
    years = sample(range(1991,2021), randint(1, 5))
    votes = []
    g_means = []
    for yyyy in years:
        n = randint(1, 5)
        g_sum = 0
        for i in range(n):
            v, g = ex3__gen_random_vote_result(yyyy)
            votes.append(v)
            g_sum += g
        g_means.append(g_sum / n)
    shuffle(votes)
    return votes, sorted(list(zip(years, g_means)), key=lambda x: x[0])

def ex3__check(tally_gaps):
    from math import isclose
    V, G = ex3__gen_random_vote_results()
    try:
        G_you = tally_gaps(V)
        assert isinstance(G_you, list), \
               f"Your function returned a {type(G_you)} instead of a `list`."
        assert all(isinstance(g, tuple) and len(g) == 2 for g in G_you), \
               f"Your function did not return a list of pairs."
        assert len(G_you) == len(G), \
               f"We expected a list of {len(G)} pairs, but yours has {len(G_you)} pairs instead."
        Y = set(x[0] for x in G)
        Y_you = set(x[0] for x in G_you)
        assert set(x[0] for x in G_you) == set(y[0] for y in G), \
               f"You returned results for years we weren't expecting."
        S_you = sorted(G_you, key=lambda x: x[0])
        for k, (s, g) in enumerate(zip(S_you, G)):
            assert (s[0] == g[0]), f"[{k}] Unexpected years: {s[0]} (you) vs. {g[0]} (us)."
            assert isclose(s[1], g[1]), f"[{k}] Means for year {g[0]} differ: {s[1]} (you) vs. {g[1]} (us)."
    except:
        print("=== Test case ===")
        print("* Input:")
        inspect_data(V)
        print("\n* Expected output:")
        print(G)
        if 'G_you' in locals():
            print("\n* Your output:")
            print(G_you)
        raise

def capitalize(s):
    if len(s) > 0:
        s = s[0].upper() + s[1:]
    return s

def gen_new_name(existing_names=None):
    def gen_name():
        first = capitalize(gen_word())
        last = capitalize(gen_word())
        return f"{first} {last}"
    name = gen_name()
    if existing_names is not None:
        while name in existing_names:
            name = gen_name()
        assert name not in existing_names
        if isinstance(existing_names, dict):
            existing_names[name] = None
        elif isinstance(existing_names, set):
            existing_names.add(name)
        elif isinstance(existing_names, list):
            existing_names.append(name)
        else:
            assert False, f"Don't know how to add this name to an object of type {type(existing_names)}."
    return name

def ex4__gen_parties(n_max=10, all_parties=None):
    from random import randint, choices
    if all_parties is None:
        all_parties = dict()
    n = randint(1, n_max)
    for i in range(n):
        name = gen_new_name(all_parties)
        all_parties[name] = choices(["R", "D", "ID"], weights=[0.45, 0.45, 0.1], k=1)[0]
    return all_parties

def ex4__gen_random_votes(parties, cast_vote=True):
    from random import randint, sample, choice
    v = {gen_word(): gen_word(), 'positions': []}
    n = randint(1, len(parties))
    voters = sample(list(parties.keys()), n)
    for voter in voters:
        cast = {'name': voter, 'party': parties[voter]}
        if cast_vote:
            cast['vote_position'] = choice(["Yes", "No", "Not Voting"])
        v['positions'].append(cast)
    return v, set(voters)

def ex4__gen_random_vote_results(cast_vote=False):
    from random import randint
    parties = ex4__gen_parties()
    parties_who_voted = set()
    n = randint(1, 5)
    votes = []
    for i in range(n):
        V, P = ex4__gen_random_votes(parties, cast_vote=cast_vote)
        votes.append(V)
        parties_who_voted |= P
    return votes, {k: parties[k] for k in parties_who_voted}

def ex4__check(get_parties):
    V, P = ex4__gen_random_vote_results()
    K = P.keys()
    try:
        P_yours = get_parties(V)
        assert isinstance(P_yours, dict), \
               f"Your code did not return a dictionary."
        assert all(v in ["D", "R", "ID"] for v in P_yours.values()), \
               f"Some of your party affiliations are not one of 'D', 'R', or 'ID'."
        assert len(P) == len(P_yours), \
               f"Expected {len(P)} members, but your code produced {len(P_yours)}."
        K_yours = P_yours.keys()
        assert set(K) == set(K_yours), \
               f"The names in your result differ from ours."
        assert all(P_yours[k] == v for k, v in P.items()), \
               f"Your computed party affiliations don't match ours."
    except:
        print("=== Test case ===")
        print("* Input vote results:")
        inspect_data(V)
        print("\n* Expected output:")
        inspect_data(P)
        if 'P_yours' in locals():
            print("\n* Your output:")
            inspect_data(P_yours)
        raise

def ex5__gen_random_votes(parties, vvs):
    assert isinstance(vvs, dict)
    from random import randint, sample, choice, random
    v = {gen_word(): gen_word(), 'positions': []}
    n = randint(1, len(parties))
    all_voters = list(parties.keys())
    actual_voters = set()
    for voter in all_voters:
        vote = choice(["Yes", "No", "Not Voting"])
        vote_value = True if vote == "Yes" else (False if vote == "No" else None)
        cast = {'name': voter, 'party': parties[voter], 'vote_position': vote}
        if vote_value is not None or random() < 0.1: # randomly drop a non-voter
            v['positions'].append(cast)
            actual_voters.add(voter)
        vvs[voter].append(vote_value)
    return v, actual_voters

def ex5__gen_random_vote_positions():
    from random import randint
    from collections import defaultdict
    parties = ex4__gen_parties()
    actual_voters = set()
    n = randint(1, 5)
    votes = []
    voting_vectors = defaultdict(list)
    for i in range(n):
        V, P = ex5__gen_random_votes(parties, voting_vectors)
        votes.append(V)
        actual_voters |= P
    actual_voting_vectors = {name: vec for name, vec in voting_vectors.items() if name in actual_voters}
    actual_parties = {k: parties[k] for k in actual_voters}
    return votes, actual_voting_vectors, actual_parties

def ex5__check(build_voting_vectors):
    V, X, _ = ex5__gen_random_vote_positions()
    voters = set(X.keys())
    try:
        X_yours = build_voting_vectors(V)
        assert isinstance(X_yours, dict), \
               f"You returned a solution of type {type(X_yours)} instead of a dictionary."
        assert len(X_yours) == len(X), \
               f"Your solution produced {len(X_yours)} voting vectors, but we expected {len(X)}."
        voters_yours = set(X_yours.keys())
        assert voters == voters_yours, \
               f"Your solution does not include the same set of voters as ours."
        for v in voters:
            y = X_yours[v]
            assert isinstance(y, list), \
                   f"Your voting vector for person '{v}' is a {type(y)}, not a list."
            x = X[v]
            assert len(y) == len(x), \
                   f"Your voting vector for '{v}' has {len(y)} entries, whereas we expected {len(x)}."
            assert all(a == b for a, b in zip(y, x)), \
                   f"Your voting vector for '{v}' does not match ours."
    except:
        print("=== Test case ===")
        print("* Input vote results:")
        inspect_data(V)
        print("\n* Expected voting vector output:")
        inspect_data(X)
        if 'X_yours' in locals():
            print("\n* Your voting vector output:")
            inspect_data(X_yours)
        raise

def ex6__gen_data():
    from random import randint, choices, choice
    from collections import defaultdict
    Rs, Ds, Is = {}, {}, {}
    all_names = set()
    n = randint(1, 7) # total no. of people
    parties = {}
    for i in range(n):
        name = gen_new_name(all_names)
        party = choices(["R", "D", "ID"], weights=[0.45, 0.45, 0.1], k=1)[0]
        parties[name] = party
        if party == "R":
            Rs[name] = []
        elif party == "D":
            Ds[name] = []
        else:
            assert party == "ID"
            Is[name] = []
    m = randint(1, 5) # no. of votes per person
    pairs = defaultdict(int)
    for j in range(m):
        for r in Rs:
            Rs[r].append(choice([True, False, None]))
        for d in Ds:
            Ds[d].append(choice([True, False, None]))
        for i in Is:
            Is[i].append(choice([True, False, None]))
        for r, vr in Rs.items():
            for d, vd in Ds.items():
                pairs[(r, d)] += (vr[-1] is not None) and (vd[-1] is not None) and (vr[-1] == vd[-1])
    result = [(r, d, c) for (r, d), c in pairs.items()]
    vecs = {**Rs, **Ds, **Is}
    return parties, vecs, result

def ex6__check(opposing_pairs):
    parties, vecs, pairs = ex6__gen_data()
    try:
        pairs_yours = opposing_pairs(vecs, parties)
        assert isinstance(pairs_yours, list), \
               f"Your solution returned an object of type {type(pairs_yours)} rather than a list."
        assert all(len(p) == 3 for p in pairs_yours), \
               f"Not all elements of your result are triples (3-tuples)."
        lookup_yours = {(r, d): c for r, d, c in pairs_yours}
        for r, d, c in pairs:
            assert (d, r) not in lookup_yours, \
                   f"Your output has a Democrat-Republican pair, ('{d}', '{r}'), but the output is required to include Republican-Democrat pairs, i.e., the Republican name should appear first."
            assert (r, d) in lookup_yours, \
                   f"The Republican-Democrat pair, ('{r}', '{d}'), is not in your output."
            c_yours = lookup_yours[(r, d)]
            assert c == c_yours, \
                   f"The pair ('{r}', '{d}') should have a common-vote count of {c}, but yours produced {c_yours}."
    except:
        print("=== Test case ===")
        print("* Input parties:")
        inspect_data(parties)
        print("\n* Input voting vectors:")
        inspect_data(vecs)
        print("\n* Expected output pairs:")
        inspect_data(pairs)
        if 'pairs_yours' in locals():
            print("\n* Your output pairs:")
            inspect_data(pairs_yours)
        raise

# eof
