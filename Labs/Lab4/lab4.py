## Description
"""
The column vector 'X' will be symbolised as a list of size 1 lists, that is
X = [[x1], [x2] ,[x3], ... , [xn]]. An m by n matrix 'A' will be symbolised by a list of size
m consisting of lists of size n. The solution to task 4 in the lab will be the function
'gaussian_elimination'.
"""


def matrix_multiply(matrix1, matrix2):
    m = len(matrix1)
    n = len(matrix2)
    p = len(matrix2[0])
    element = lambda i,j: sum([matrix1[i][k] * matrix2[k][j]
                               for k in range(n)])
    row = lambda i: [element(i,j) for j in range(p)]
    return [row(i) for i in range(m)]


def create_identity(n):
    """ Creates an n by n identity matrix. """
    return [[1 if i==j else 0 for j in range(n)] for i in range(n)]


def switch(row1, row2, n):
    """ Creates an n by n matrix which switches the rows
    row1 and row2 on a matrix if this matrix returned is multiplied
    on the left. Rows are indexed such that the first row is row 0.
    """
    I = create_identity(n)
    return [I[row2] if i==row1
            else I[row1] if i==row2
            else I[i] for i in range(n)]


def add_multiple_of_row_to_other_row(multiple, row, other_row, n):
    """ Creates an 'n' by 'n' matrix which if multiplied with on the
    left of another matrix, then that other matrix will add
    'multiple' times the row 'row' to the row 'other_row'.
    rows are indexed such that the first row is row 0.
    """
    I = create_identity(n)
    new_other_row = [1 if j==other_row and other_row != row
                     else multiple if j==row
                     else 0 for j in range(n)]
    return [new_other_row if i==other_row else I[i] for i in range(n)]


def scale_row(multiple, row, n):
    """ Create an 'n' by 'n' matrix which if multiplied with on the
    left of another matrix, then that other matrix will have the
    row 'row' be mutliplied with 'multiple'.
    """
    return add_multiple_of_row_to_other_row(multiple, row, row, n)


def find_next_gaussian_elimination_task(matrix):
    """ Compares with the identity matrix, to see what element should be
    focused on next and what gaussian elimination task needs to be done for
    that element. This function always returns a coordinate in the form of a 
    tuple and a string with the operation that needs to be done. It checks
    each column from left to right. In the column fix, it first checks if
    the diagonal element (the element corresponding to the 1 in the same column 
    of the identity  matrix), is equal to one. If it is a zero this function 
    searches for the closest non-zero element below, and returns the coordinate 
    for that element and the string "swap". If it is non-zero but not 1 then the 
    diagonal coordinate is returned with the string "normalise". Next it checks 
    the rest of the column, from top to bottom, to see if the elements are zero.
    If not, then the coordinate with the string "eliminate" is returned. If the 
    matrix is the identity matrix, this function returns the tuple (-1, -1) and 
    the string 'finnished'. If the determinant of the matrix is 0 then the 
    tuple (-1,-1) and the string 'failed' is returned.
    """
    n = len(matrix)
    I = create_identity(n)
    transpose = lambda matrix: [[matrix[i][j] for i in range(n)]
                                for j in range(n)]
    matrix_of_validity_of_entries = [[matrix[i][j] == I[i][j] for j in range(n)]
                                for i in range(n)]
    list_of_validity_of_columns = list(
        map(all, transpose(matrix_of_validity_of_entries)))
    try:
        column_to_fix_index = list_of_validity_of_columns.index(False)
    except ValueError:
        return (-1,-1), "finnished"

    i = column_to_fix_index
    diagonal_element = matrix[i][i]
    column = transpose(matrix)[i]
    non_zero_elements = list(map(lambda x: x!=0, column))
    non_zero_elements_except_diagonal = [False if index==i
                                         else non_zero_elements[index]
                                         for index in range(n)]
    non_zero_elements_below_diagonal = non_zero_elements[i+1:]
    if not any(non_zero_elements_below_diagonal) and diagonal_element==0:
        return (-1,-1), "failed"
    elif diagonal_element == 0:
        x,y = non_zero_elements_below_diagonal.index(True), i
        return (x,y), "swap"
    elif diagonal_element != 0 and diagonal_element != 1:
        return (i,i), "normalise"
    else:
        x,y = non_zero_elements_except_diagonal.index(True), i
        return (x,y), "eliminate"


def gaussian_elimination(A, b):
    """ If 'A' is an n by n matrix and 'b' is an n by 1 vector,
    then this function returns the n by 1 vector 'x' which solves
    the equation 'Ax = b'. Observe that the vectors element
    must be surrounded by squarebrackets, for example:
    [[1],[2],[3]] is correct and [1,2,3] is not.
    """
    n = len(b)
    I = create_identity(n)
    mult = lambda A, B: matrix_multiply(A, B)
    E = lambda m, i, j: add_multiple_of_row_to_other_row(m, i, j, n)
    S = lambda i,j: switch(i,j,n)
    M = lambda m, r: scale_row(m, r, n)

    (x,y), task = find_next_gaussian_elimination_task(A)
    if task == "finnished":
        return b
    elif task == "failed":
        raise ValueError(
            "<gaussian_elimination: determinant of A must be non-zero.>")
    elif task == "swap":
        A_prim = mult(S(x,y), A)
        b_prim = mult(S(x,y), b)
        return gaussian_elimination(A_prim, b_prim)
    elif task == "normalise":
        inverse = 1 / A[x][y]
        A_prim = mult(M(inverse, x), A)
        b_prim = mult(M(inverse, x), b)
        return gaussian_elimination(A_prim, b_prim)
    elif task == "eliminate":
        inverse = - A[x][y]
        A_prim = mult(E(inverse, y,x), A)
        b_prim = mult(E(inverse, y,x), b)
        return gaussian_elimination(A_prim, b_prim)
    else:
        print("Something went wrong. Debug:", (x,y), task)
