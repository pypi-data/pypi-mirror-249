import modeler


def encode(clues):
    """
    Encode a sudoku puzzle as a SAT problem.

    Parameters
    ----------
    clues : list of lists of ints
        9x9 int matrix, non-zero values represent clues

    Returns
    -------
    model : eznf.Model
        A SAT model representing the sudoku puzzle.
    """
    Z = modeler.Modeler()  # modeler object from my library, always starts like this.

    # create vars
    for i in range(9):
        for j in range(9):
            for n in range(1, 10):
                Z.add_var(f"x_{i, j, n}", description=f"Cell ({i}, {j}) gets number {n}")

    # exactly one number per cell
    for i in range(9):
        for j in range(9):
            Z.exactly_one([f"x_{i, j, n}" for n in range(1, 10)])

    # respect clues
    for i in range(9):
        for j in range(9):
            if clues[i][j] != 0:
                Z.constraint(f"x_{i, j, clues[i][j]}")

    # exactly-one constraints
    for n in range(1, 10):
        # rows
        for i in range(9):
            Z.exactly_one([f"x_{i, j, n}" for j in range(9)])

        # cols 
        for j in range(9):
            Z.exactly_one([f"x_{i, j, n}" for i in range(9)])

        # sub_grids
#        sub_grids = [[[] for sj in range(3)] for si in range(3)]
 #       for i in range(9):
  #          for j in range(9):
   #             sub_grids[i//3][j//3].append((i, j))
   #     for si in range(3):
    #        for sj in range(3):
     #           Z.exactly_one([f"x_{*cell, n}" for cell in sub_grids[si][sj]])

    return Z


sudoku_example = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
                  [6, 0, 0, 1, 9, 5, 0, 0, 0],
                  [0, 9, 8, 0, 0, 0, 0, 6, 0],
                  [8, 0, 0, 0, 6, 0, 0, 0, 3],
                  [4, 0, 0, 8, 0, 3, 0, 0, 1],
                  [7, 0, 0, 0, 2, 0, 0, 0, 6],
                  [0, 6, 0, 0, 0, 0, 2, 8, 0],
                  [0, 0, 0, 4, 1, 9, 0, 0, 5],
                  [0, 0, 0, 0, 8, 0, 0, 7, 9]]

encoding = encode(sudoku_example)
# encoding.serialize("sudoku.cnf")

def sudoku_decoder(model):
    matrix = [[0 for j in range(9)] for i in range(9)]
#    print(model)
    true_vars = 0
    for i in range(9):
        for j in range(9):
            for n in range(1, 10):
                if model[f"x_{i, j, n}"]:
                    true_vars += 1
                    print(f"x_{i, j, n}")
                    matrix[i][j] = str(n)
    print("true vars: ", true_vars)
    for row in matrix:
        print(row)

encoding.solve_and_decode(sudoku_decoder)
