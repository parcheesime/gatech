# def strcat_ba(a, b):
#     assert type(a) is str, f"Input argument `a` has `type(a)` is {type(a)} rather than `str`"
#     assert type(b) is str, f"Input argument `b` has `type(b)` is {type(b)} rather than `str`"
#     ###
#     return f'{b}{a}'
# #     ###
    
# #     # `strcat_ba_test`: Test cell

# # Workaround:  # Python 3.5.2 does not have `random.choices()` (available in 3.6+)
# def random_letter():
#     from random import choice
#     return choice('abcdefghijklmnopqrstuvwxyz')

# def random_string(n, fun=random_letter):
#     return ''.join([str(fun()) for _ in range(n)])

# # a = random_string(5)
# # b = random_string(3)
# # c = strcat_ba(a, b)
# # print('strcat_ba("{}", "{}") == "{}"'.format(a, b, c))
# # assert len(c) == len(a) + len(b), "`c` has the wrong length: {len(c)} rather than {len(a)+len(b)}"
# # assert c[:len(b)] == b
# # assert c[-len(a):] == a
# # print("\n(Passed!)")

# # exercise 3

# def strcat_list(L):
#     assert isinstance(L, list)  # Checking if L is a list

#     # Making a copy of L and reversing it
#     reversedL = L.copy()
#     reversedL.reverse()

#     # Converting all elements to strings and concatenating
#     concatL = "".join(str(item) for item in reversedL)

#     return concatL

# # `strcat_list_test`: Test cell
# n = 3
# nL = 6
# L = [random_string(n) for _ in range(nL)]
# Lc = strcat_list(L)

# print('L == {}'.format(L))
# print('strcat_list(L) == \'{}\''.format(Lc))
# assert all([Lc[i*n:(i+1)*n] == L[nL-i-1] for i, x in zip(range(nL), L)])
# print("\n(Passed!)")

def count_word_lengths(s):
    assert all([x.isalpha() or x == ' ' for x in s])
    assert type(s) is str
    ###
    words_list = s.split()
    word_count_list = [len(w) for w in words_list]
    return word_count_list
    ###
    
    # `count_word_lengths_test`: Test cell

# Test 1: Example
qbf_str = 'doggy'
qbf_lens = count_word_lengths(qbf_str)
print("Test 1: count_word_lengths('{}') == {}".format(qbf_str, qbf_lens))
# assert qbf_lens == [3, 5, 5, 3, 6, 4, 3, 4, 3]

# # Test 2: Random strings
# from random import choice # 3.5.2 does not have `choices()` (available in 3.6+)
# #return ''.join([choice('abcdefghijklmnopqrstuvwxyz') for _ in range(n)])

# def random_letter_or_space(pr_space=0.15):
#     from random import choice, random
#     is_space = (random() <= pr_space)
#     if is_space:
#         return ' '
#     return random_letter()

# S_LEN = 40
# W_SPACE = 1 / 6
# rand_str = random_string(S_LEN, fun=random_letter_or_space)
# rand_lens = count_word_lengths(rand_str)
# print("Test 2: count_word_lengths('{}') == '{}'".format(rand_str, rand_lens))
# c = 0
# while c < len(rand_str) and rand_str[c] == ' ':
#     c += 1
# for k in rand_lens:
#     print("  => '{}'".format (rand_str[c:c+k]))
#     assert (c+k) == len(rand_str) or rand_str[c+k] == ' '
#     c += k
#     while c < len(rand_str) and rand_str[c] == ' ':
#         c += 1
    
# # Test 3: Empty string
# print("Test 3: Empty strings...")
# assert count_word_lengths('') == []
# assert count_word_lengths('   ') == []
# print(count_word_lengths('the'))

# print("\n(Passed!)")