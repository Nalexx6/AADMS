import regex as re


def find_regex_from_nfa(nfa):
    states = list(nfa.keys())
    num_states = len(states)

    # Initialize the matrix for storing equations
    matrix = [[None] * (num_states + 1) for _ in range(num_states)]

    for i in range(1, num_states):
        matrix[i][num_states] = 'e'

    # Create equations based on transitions
    for i in range(num_states):
        for j in range(num_states):
            if j in nfa[states[i]]:
                print(f'{j} is direct from {states[i]}')
                matrix[i][j] = nfa[states[i]][j]
            else:
                print(f'{j} is not direct from {states[i]}')
                matrix[i][j] = None  # ∅ for no transition

    print(matrix)
    # Apply Gauss method

    # Straight course
    for k in range(num_states):
        expr = f"({matrix[k][k]})*"
        for i in range(k + 1, num_states):
            matrix[k][k+1] += expr
            matrix[k+1][i] += f"({matrix[k+1][i]})" + '|' + f"({matrix[k][k+1]}" + f"{matrix[i][k]})"

        matrix[k][k] = expr

    print(matrix)

    res = {states[num_states - 1]: matrix[num_states - 1][num_states - 1]}

    # Opposite course
    for k in range(num_states - 2, -1, -1):
        expr = ""
        for i in range(k + 1, num_states):
            expr += matrix[i][i] + matrix[k][i]

        if matrix[k][num_states] is not None:
            expr += matrix[k][num_states]

        matrix[k][k] = expr
        res[states[k]] = expr

    print(matrix)

    # Extract regular expressions for each state
    regex_dict = {}
    for i in range(num_states):
        regex_dict[states[i]] = matrix[i][i]

    # Simplify the regular expressions
    for i, r in regex_dict.items():
        simplified_regex = re.sub(r'\(\(.*?\)\)\*', r'(\1)*', r)  # Remove redundant parentheses
        simplified_regex = re.sub(r'\(\?P<[^>]+>', '(', simplified_regex)  # Replace named capture groups
        regex_dict[i] = simplified_regex

    return res


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


