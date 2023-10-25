
def find_regex_from_nfa(nfa):
    states = list(nfa.keys())
    num_states = len(states)

    # Initialize the matrix for storing equations
    matrix = [[None] * (num_states + 1) for _ in range(num_states)]

    matrix[0][num_states] = 'e'

    # Create equations based on transitions
    for i in range(num_states):
        for j in range(num_states):
            if j in nfa[states[i]]:
                print(f'{states[j]} is direct from {states[i]}')
                matrix[i][j] = nfa[states[i]][j]
            else:
                print(f'{states[j]} is not direct from {states[i]}')
                matrix[i][j] = None  # ∅ for no transition

    # Apply Gauss method

    # Straight course
    for k in range(num_states - 1, -1, -1):
        expr = f"({matrix[k][k]})*"
        for i in range(k - 1, -1, -1):
            if matrix[k][k-1] is not None and matrix[k-1][i] is not None and matrix[i][k] is not None:
                matrix[k][k-1] += expr
                matrix[k-1][i] += f"({matrix[k-1][i]})" + '|' + f"({matrix[k][k-1]}" + f"{matrix[i][k]})"

        matrix[k][k] = expr

    res = {states[0]: matrix[0][0]}

    # Opposite course
    for k in range(1, num_states):
        expr = ""
        for i in range(0, k):
            expr += "(" + matrix[i][i] + matrix[k][i] + ")"
            if i < k - 1:
                expr += '|'

        matrix[k][k] = "(" + expr + ")" + matrix[k][k]
        res[states[k]] = matrix[k][k]

    # Extract regular expressions for each state
    regex_dict = {}
    for i in range(num_states):
        regex_dict[states[i]] = matrix[i][i]

    return res


if __name__ == '__main__':

    # Example usage:
    nfa_example = {
        'q1': {0: '0', 1: '0'},
        'q2': {0: '1', 1: '1'},
    }

    # nfa_example = {
    #     '0': {0: '[x]'},
    #     '1': {0: '[x,y]', 1: '[y]'},
    #     '2': {0: '[x,y,z]', 1: '[y]', 2: '[z]'},
    # }

    result = find_regex_from_nfa(nfa_example)

    # Print the result
    for state, regex in result.items():
        print(f"Regex for state {state}: {regex}")


