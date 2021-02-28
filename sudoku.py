import pulp
import sys


def solve(input):

    debug = False


    # sets

    D = range(9)
    T = range(3)

    boxes = [
        [(3 * i + k, 3 * j + l) for k in T for l in T]
        for i in T for j in T
    ]


    # parameters



    # decision variables

    g = pulp.LpVariable.dicts("g", (D, D, D), cat=pulp.LpBinary)

    prob = pulp.LpProblem(name='Sudoku')

    
    # constraints

    for i in D:
        for j in D:
            # col constraint
            prob += pulp.lpSum(g[r][i][j] for r in D) == 1

            # row constraint
            prob += pulp.lpSum(g[i][c][j] for c in D) == 1

            # digit constraint
            prob += pulp.lpSum(g[i][j][d] for d in D) == 1

        for b in boxes:
            # box constraint
            prob += pulp.lpSum([g[r][c][i] for (r, c) in b]) == 1


    for r in D:
        for c in D:
            val = input[r][c]
            if val != 0:
                prob += g[r][c][val - 1] == 1


    # solve

    prob.solve(pulp.PULP_CBC_CMD(msg=debug))

    soln = []
    for r in D:
        row = []
        soln.append(row)
        for c in D:
            for d in D:
                if pulp.value(g[r][c][d]) == 1:
                    row.append(d + 1)
    return soln


def read_prob(filename):
    prob = []
    with open(filename, 'r') as file:
        for r, line in enumerate(file):
            if r > 9:
                continue
            row = []
            prob.append(row)
            for c in range(9):
                row.append(int(line[c]))
    return prob


def read_csv_prob(str):
    prob = []
    index = 0
    for r in range(9):
        row = []
        prob.append(row)
        for c in range(9):
            row.append(int(str[index]))
            index += 1
    return prob


if __name__ == "__main__":
    filename = sys.argv[1]
    if filename[:-4] == '.csv':
        print("not implemented")
    else:
        prob = read_prob(filename)
        soln = solve(prob)
        print(soln)

