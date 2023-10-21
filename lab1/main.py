import regex as re


def find_regex_from_nfa(nfa):
    states = list(nfa.keys())
    num_states = len(states)

    # Initialize the matrix for storing equations
    matrix = [[None] * num_states for _ in range(num_states)]

    # Create equations based on transitions
    for i in range(num_states):
        for j in range(num_states):
            # if i == j:
            #     matrix[i][j] = "ε"  # ε for self-loop
            if j in nfa[states[i]]:
                print(f'{j} is direct from {states[i]}')
                matrix[i][j] = nfa[states[i]][j]
            else:
                print(f'{j} is not direct from {states[i]}')
                matrix[i][j] = None  # ∅ for no transition

    print(matrix)
    # Apply Arden's theorem
    for k in range(num_states):

        # expr = f"({matrix[k][k]})*(" + '|'.join([matrix[k][i] for i in range(num_states) if i != k and matrix[k][i] is not None]) + ")"

            # for j in range(num_states):
            #     if matrix[i][k] is not None and matrix[k][k] is not None and matrix[k][j] is not None:
            #         expr = matrix[i][k] + "(" + matrix[k][k] + ")*" + matrix[k][i]
            #         if matrix[i][j] is None:
            #             matrix[i][j] = expr
            #         else:
            #             matrix[i][j] += "|" + expr
            #
            #     print(matrix)

        expr = f"({matrix[k][k]})*"

        for i in range(k + 1, num_states):

            matrix[k][i] += expr

            for j in range(i, num_states):
                matrix[i][j] += f"({matrix[i][j]})" + '|' + f"({matrix[k][i]}" + f"{matrix[i][k]})"
                matrix[i][k] = None

        matrix[k][k] = expr

        print(matrix)

    # Extract regular expressions for each state
    regex_dict = {}
    for i in range(num_states):
        regex_dict[states[i]] = matrix[i][i]

    # Extract regular expressions for each pair of states
    # regex_dict = {}
    # for i in range(num_states):
    #     regex_dict[states[i]] = set(matrix[i][i].strip().split('|'))

    # Simplify the regular expressions
    # for i, regex in regex_dict.items():
    #         simplified_regex = re.sub(r'\(\(.*?\)\)\*', r'(\1)*', regex)  # Remove redundant parentheses
    #         simplified_regex = re.sub(r'\(\?P<[^>]+>', '(', simplified_regex)  # Replace named capture groups
    #         regex_dict[i] = simplified_regex

    return regex_dict


if __name__ == '__main__':

    # Example usage:
    nfa_example = {
        'q1': {0: '0', 1: '1'},
        'q2': {0: '0', 1: '1'},
    }

    result = find_regex_from_nfa(nfa_example)

    # Print the result
    for state, regex in result.items():
        print(f"Regex for state {state}: {regex}")


