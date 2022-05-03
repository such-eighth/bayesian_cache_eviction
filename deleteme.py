import itertools
import numpy as np

# transition_matrix = np.zeros((2, 2))
# transition_matrix[0][0] = 0.1
# transition_matrix[0][1] = 0.9
# transition_matrix[1][0] = 0.4
# transition_matrix[1][1] = 0.6

# all_matrices = [transition_matrix]
# for i in range(3 - 1):
#     recent_matrix = all_matrices[-1]
#     all_matrices.append(transition_matrix @ recent_matrix)

# print(all_matrices)

# num_elem = 2

# for i in range(num_elem):
#     for j in range(num_elem):
#         total_val = 0
#         for k in range(1, 3 + 1):
#             curr_val = 0
#             for subset in itertools.combinations(range(1, num_elem+1), k):
#                 prod = 1
#                 for elem in subset:
#                     prod *= all_matrices[elem][i][j]
#                 curr_val += prod
#             total_val += (-1)**(k+1) * curr_val
#         print(total_val)

a = np.random.rand(3,3)
a = a/a.sum(axis=1)[:,None]
print(a)