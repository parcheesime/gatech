from copy import deepcopy
from pprint import pprint

def generate_name():
    from string import ascii_lowercase, ascii_uppercase
    from random import randint, choices, choice
    return choice(ascii_uppercase) + ''.join(choices(ascii_lowercase, k=randint(5, 12))) + ',' + ''.join(choices(ascii_uppercase) + choices(ascii_lowercase, k=randint(0, 8)))

def generate_players(n):
    from random import choice, choices, randint
    
    names = []
    for _ in range(n):
        name = generate_name()
        rating = randint(1200, 2400)
        names.append({'player': name, 'rating': rating})
    return names

def generate_matches(players, n):
    from random import sample
    results = ['1-0', '0-1', '1/2-1/2']
    matches = []
    for _ in range(n):
        white, black = sample(players, 2)
        result = sample(results, 1)
        matches.append({'white': white, 'black': black, 'result': result[0]})
    return matches

def generate_games_dict(matches):
    output = []
    for match in matches:
        entry = {
            'white_player': match['white']['player'],
            'white_rating': match['white']['rating'],
            'black_player': match['black']['player'],
            'black_rating': match['black']['rating'],
            'result': match['result']
        }
        output.append(entry)
    return output

def generate_input_file(matches):
    from random import randint, choices, shuffle
    from string import ascii_lowercase
    input = ''
    for match in matches:
        metadata = [
            f'''[White "{match['white']['player']}"]\n''',
            f'''[Black "{match['black']['player']}"]\n''',
            f'''[WhiteElo "{match['white']['rating']}"]\n''',
            f'''[BlackElo "{match['black']['rating']}"]\n''',
            f'''[Result "{match['result']}"]\n'''
        ]
        # add junk metadata
        for _ in range(randint(0,3)):
            metadata.append(f'''[{''.join(choices(ascii_lowercase, k=5))} "{''.join(choices(ascii_lowercase, k=5))}"]\n''')
        # add metadata to input
        shuffle(metadata)
        for line in metadata:
            input += line
        input += '\n'
        input += ''.join(choices(ascii_lowercase, k=350)) + '\n\n'
    return input[:-2]

def ex0_test(n_players, n_matches, func):
    from pprint import pprint
    players = (generate_players(n_players))
    matches = generate_matches(players, n_matches)
    output = generate_games_dict(matches)
    input = generate_input_file(matches)
    test_output = func(input)
    try:
        assert test_output == output, 'Your solution doesn\'t match ours!'
        assert type(test_output) == type(output), 'Your output is not the correct type!'
        for d, d_test in zip(output, test_output):
            assert type(d) == type(d_test), f'The type of your list items is {type(d_test)} instead of {type(d)}'
            assert type(d_test['white_rating']) == type(int()), 'white_rating is not an Integer'
            assert type(d_test['black_rating']) == type(int()), 'black_rating is not an Integer'            

    except AssertionError:
        print('Input:')
        pprint(input)
        print(f'Output does not match solution.\nYour output:')
        pprint(test_output)
        print('True solution:')
        pprint(output)
        raise AssertionError

def ex1_test(n_players, n_matches, func):
    from random import choice
    from collections import defaultdict
    from pprint import pprint
    players = generate_players(n_players)
    output = defaultdict(list)
    input = []
    for i, player in enumerate(players):
        opponents = players[:i] + players[(i+1):]
        for j in range(n_matches):
            opponent = opponents[j]
            w = [True, False]
            player_white = choice(w)
            winner = choice(['w', 'b', 'd'])
            if player_white:
                white = player['player']
                black = opponent['player']
            else:
                white = opponent['player']
                black = player['player']
            input.append({'white_player': white, 'black_player': black, 'result': '1-0' if winner == 'w' else '0-1' if winner == 'b' else '1/2-1/2'})
            output[white].append((black, 1.0 if winner == 'w' else 0.0 if winner == 'b' else 0.5))
            output[black].append((white, 1.0 if winner == 'b' else 0.0 if winner == 'w' else 0.5))
    input_cp = deepcopy(input)
    output = dict(output)
    test_output = func(input)
    try:
        
        assert isinstance(test_output, type(output)), 'Your output is the incorrect type!'
        assert test_output == output, 'Your solution did not match!'
        assert input == input_cp, 'You modified the function input!'
        for k in output:
            l, l_test = output[k], test_output[k]
            for t, t_test in zip(l, l_test):
                assert type(t[0]) == type(t_test[0]), 'Incorrect type!'
                assert type(t[1]) == type(t_test[1]), 'Incorrect type!'
    except AssertionError:
        print('Input:')
        pprint(input)
        print(f'Output does not match solution.\nYour output:')
        pprint(test_output)
        print('True solution:')
        pprint(output)
        raise AssertionError

def ex2_test(n_players, n_matches, func):
    from collections import defaultdict
    from random import choice
    input = defaultdict(list)
    output = defaultdict(int)
    for _ in range(n_players):
        p = generate_name()
        for _ in range(n_matches):
            points = choice([1.0, 0.5, 0.0])
            input[p].append((generate_name(), points))
            output[p] += points
    input = dict(input)
    output = dict(output)
    input_cp = deepcopy(input)
    test_output = func(input)
    try:
        
        assert isinstance(test_output, type(output)), 'Your output is the incorrect type!'
        assert test_output == output, 'Your solution did not match!'
        assert input == input_cp, 'You modified the function input!'
    except AssertionError:
        print('Input:')
        pprint(input)
        print(f'Output does not match solution.\nYour output:')
        pprint(test_output)
        print('True solution:')
        pprint(output)
        raise AssertionError

def ex3_test(n_players, n_matches, func):
    from itertools import combinations
    from random import random, randint
    whammy = random() > 0.75
    players = generate_players(n_players)
    input = []
    output = {}
    for i, (white, black) in enumerate(combinations(players, 2)):
        input.append({'white_player': white['player'], 'white_rating': white['rating'], 'black_player': black['player'], 'black_rating': black['rating']})
        output[black['player']] = black['rating']
        output[white['player']] = white['rating']
        if i >= (n_matches-1): break
    if whammy:
        if (random() < 0.5):
            input.append({'white_player': white['player'], 'white_rating': white['rating'] + randint(1, 50), 'black_player': black['player'], 'black_rating': black['rating']})
        else:
            input.append({'white_player': white['player'], 'white_rating': white['rating'], 'black_player': black['player'], 'black_rating': black['rating'] + randint(1, 50)})
        try:
            input_cp = deepcopy(input)
            test_output = func(input)
            print('Input:')
            pprint(input)
            print('Output: ')
            pprint(test_output)
            raise AssertionError('There are conflicting ratings. Your function incorrectly did NOT raise a ValueError')
        except ValueError:
            assert input == input_cp, 'You modified the input!'
    else:
        input_cp = deepcopy(input)
        test_output = func(input)
        try:
            assert test_output == output
            assert input == input_cp, 'You modified the input!'
            for v in test_output.values():
                assert type(v) == type(int()), 'Your output has incorrect type!'
        except AssertionError:
            print('Input:')
            pprint(input)
            print(f'Output does not match solution.\nYour output:')
            pprint(test_output)
            print('True solution:')
            pprint(output)
            raise AssertionError
            
def ex4_test(func):
    from random import random, randint
    from math import log10
    E = random() * 0.5 + 0.25
    d = 400 * log10(1/E - 1)
    r_opponent = randint(1200, 1800)
    r_player = round(r_opponent - d)
    test_output = func(r_player, r_opponent)
    try:
        assert abs(test_output - E) <= 0.001
    except AssertionError:
        print('Input:')
        print((r_player, r_opponent))
        print(f'Output does not match solution.\nYour output:')
        pprint(test_output)
        print('True solution:')
        print(E)
        raise AssertionError

def ex5_test(n_players, n_matches, func):
    from collections import defaultdict
    from random import randint, choice
    player_results = defaultdict(list)
    output_1 = defaultdict(int)
    output_2 = defaultdict(int)
    player_ratings = {}
    es_1 = lambda x, y: float(x*y)
    es_2 = lambda x, y: float(x+y)
    for _ in range(n_players):
        player = generate_name()
        p_rating = randint(1200, 2000)
        player_ratings[player] = p_rating
        for _ in range(n_matches):
            opponent = generate_name()
            o_rating = randint(1200, 2000)
            result = choice([1.0, 0.5, 0.0])
            player_ratings[opponent] = o_rating
            player_results[player].append((opponent, result))
            output_1[player] += o_rating
            output_2[player] += o_rating
        output_1[player] *= p_rating
        output_2[player] += n_matches * p_rating
    player_results_cp = deepcopy(player_results)
    player_ratings_cp = deepcopy(player_ratings)
    test_output_1 = func(player_results, player_ratings, es_1)
    test_output_2 = func(player_results, player_ratings, es_2)
    player_results = dict(player_results)
    output_1 = dict(output_1)
    output_2 = dict(output_2)
    try:
        assert player_ratings == player_ratings_cp, 'You modified the input!'
        assert player_results == player_results_cp, 'You modified the input!'
        assert isinstance(test_output_1, type(output_1))
        assert isinstance(test_output_2, type(output_1))
        assert test_output_1 == output_1
        assert test_output_2 == output_2
    except AssertionError:
        print('Input:')
        print('player_results:')
        pprint(player_results)
        print('player_ratings:')
        pprint(player_ratings)
        print('es_func (for output_1):', 'lambda x, y: float(x*y)', 'es_func (for output 2):', 'lambda x, y: float(x+y)', 'expected output 1:', output_1, 'your output 1:', test_output_1, 'expected output 2:', output_2, 'your output 2:', test_output_2, sep='\n')
        raise AssertionError

def ex6_test(n_players, func):
    from random import randint
    players = generate_players(n_players)
    initial_ratings = {p['player']: p['rating'] for p in players}
    deltas = {p['player']: randint(-20, 20) for p in players}
    score_observed = {p['player']: randint(4, 6)*0.5 for p in players}
    score_expected = {}
    for name in initial_ratings:
        score_expected[name] = round(score_observed[name] - deltas[name]/10, 3) 
    post_ratings = {p['player']: p['rating'] + deltas[p['player']] for p in players}
    score_observed_cp = deepcopy(score_observed)
    score_expected_cp = deepcopy(score_expected)
    initial_ratings_cp = deepcopy(initial_ratings)
    output_test = func(score_observed, score_expected, initial_ratings)
    try:
        assert score_observed_cp == score_observed, 'You modified the input!'
        assert score_expected_cp == score_expected, 'You modified the input!'
        assert initial_ratings_cp == initial_ratings, 'You modified the input!'
        assert post_ratings == output_test
        assert isinstance(output_test, type(post_ratings)), 'Your output is the wrong type!'
        for v in output_test.values():
            assert type(v) == type(int()), 'Your output is the wrong type!'
    except AssertionError:
        print('Incorrect output!')
        print(f'player_scores:')
        pprint(score_observed)
        print(f'expected_player_scores:')
        pprint(score_expected)
        print(f'player_ratings:')
        pprint(initial_ratings)
        print(f'Your output:')
        pprint(output_test)
        print('True solution:')
        pprint(post_ratings)
        raise AssertionError

def ex7_test(n_players, func):
    from random import random, randint
    old_ratings = {}
    new_ratings = {}
    output = {}
    for _ in range(n_players):
        whammy_num = random()
        player = generate_name()
        if whammy_num < 0.1: # new player
            new = randint(1150, 1300)
            new_ratings[player] = new
            output[player] = new - 1200
        elif whammy_num > 0.9: # did not play
            old = randint(1500, 1800)
            old_ratings[player] = old
            output[player] = 0
        else:
            old = randint(1500, 1800)
            new = randint(1500, 1800)
            new_ratings[player] = new
            old_ratings[player] = old
            output[player] = new - old
    old_ratings_cp = deepcopy(old_ratings)
    new_ratings_cp = deepcopy(new_ratings)
    output_test = func(old_ratings, new_ratings)
    try:
        assert isinstance(output_test, type(output))
        assert old_ratings_cp == old_ratings, 'You modified the input!'
        assert new_ratings_cp == new_ratings, 'You modified the input!'
        assert output == output_test
        for v in output_test.values():
            assert type(v) == type(int()), 'Wrong Type!'
    except AssertionError:
        print('Incorrect output!')
        print('Inputs:')
        print(f'old_ratings:')
        pprint(old_ratings)
        print(f'new_ratings:')
        pprint(new_ratings)
        print(f'Your output:')
        pprint(output_test)
        print('True solution:')
        pprint(output)
        raise AssertionError

def get_mem_usage():
    """Return current memory usage (bytes) of the running Python process"""
    import os, psutil
    process = psutil.Process(os.getpid())
    return process.memory_info().rss  # in bytes 

def get_mem_usage_str():
    bytes = get_mem_usage()
    result = f"{bytes:,} B"
    units = [(10, "Ki"), (20, "Mi"), (30, "Gi"), (40, "Ti"), (50, "Pi"), (60, "Ei")]
    for e, p in reversed(units):
        if bytes >= 2**e:
            bytes /= 2**e
            result = f"{bytes:.1f} {p}B"
            break
    return result

data_root = 'resource/asnlib/publicdata/'         
def read_raw_data(filename):
    with open(data_root + filename, 'r') as f:
        return f.read()
    
def write_pickle(var, var_name):
    import pickle
    import json
    with open(data_root+'settings.json', 'r') as f:
        settings = json.load(f)
    with open(data_root+var_name+'.pkl', 'wb') as f:
        if settings['write_results']:
            pickle.dump(var, f)

def read_pickle(var_name):
    import pickle
    with open(data_root+var_name+'.pkl', 'rb') as f:
        return pickle.load(f)
            

# tests_to_run = {
#     'q0': False,
#     'q1': False,
#     'q2': False,
#     'q3': False,
#     'q4': False,
#     'q5': False,
#     'q6': False,
#     'q7': True
# }

if __name__ == '__main__':
    from shutil import copyfile
    from os import getcwd
    print(getcwd())
    copyfile('./run_tests.py', '../../../run_tests.py')
    # import json
    # with open('test_to_run.json', 'r') as f:
    #     tests_to_run = json.load(f)
    # n_runs = 1000
    # n_players = 25
    # n_matches = 15
    # if tests_to_run.get('q0', False):
    #     from Q0.q0 import extract_games
    #     for _ in range(n_runs):
    #         ex0_test(n_players, n_matches, extract_games)
    #     print('Q0 Passed!')

    # if tests_to_run.get('q1', False):
    #     from Q1.q1 import extract_player_results
    #     for _ in range(n_runs):
    #         ex1_test(n_players, n_matches, extract_player_results)
    #     print('Q1 Passed!')

    # if tests_to_run.get('q2', False):
    #     from Q2.q2 import calculate_score
    #     for _ in range(n_runs):
    #         ex2_test(n_players, n_matches, calculate_score)
    #     print('Q2 Passed!')

    # if tests_to_run.get('q3', False):
    #     from Q3.q3 import extract_ratings
    #     for _ in range(n_runs):
    #         ex3_test(n_players, n_matches, extract_ratings)
    #     print('Q3 Passed!')

    # if tests_to_run.get('q4', False):
    #     from Q4.q4 import expected_match_score
    #     for _ in range(n_runs):
    #         ex4_test(expected_match_score)
    #     print('Q4 Passed!')

    # if tests_to_run.get('q5', False):
    #     from Q5.q5 import expected_tournament_score
    #     for _ in range(n_runs):
    #         ex5_test(1, 2, expected_tournament_score)
    #     print('Q5 Passed!')

    # if tests_to_run.get('q6', False):
    #     from Q6.q6 import compute_final_ratings
    #     for _ in range(n_runs):
    #         ex6_test(n_players, compute_final_ratings)
    #     print('Q6 Passed!')

    # if tests_to_run.get('q7', False):
    #     from Q7.q7 import compute_deltas
    #     for _ in range(n_runs):
    #         ex7_test(n_players, compute_deltas)
    #     print('Q7 Passed!')