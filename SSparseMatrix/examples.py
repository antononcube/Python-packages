from SSparseMatrix.src.SSparseMatrix import *

# Create a sparse matrix with named rows and columns (a SSparseMatrix object)
mat = [[1, 0, 0, 3], [4, 0, 0, 5], [0, 3, 0, 5], [0, 0, 1, 0], [0, 0, 0, 5]]
smat = SSparseMatrix(mat)
smat.set_row_names(["A", "B", "C", "D", "E"])
smat.set_column_names(["a", "b", "c", "d"])

# Print the sparse matrix
smat.print_matrix()

# Multiply with the transpose and print
smat2 = smat.copy().dot(smat.copy().transpose())
smat2.print_matrix()

# Multiply with a list-vector:
smat3 = smat.copy().dot([1, 2, 1, 0])
smat3.print_matrix()

# Get single element
print(smat["A", "d"])
print(smat[0, 3])

# Get subset of rows
smat[["A", "D", "B"], :].print_matrix()

# Get subset of columns
smat[:, ['a', 'c']].print_matrix()

# Row sums:
print(smat.row_sums())
print(smat.row_sums_dict())

# Column sums:
print(smat.column_sums())
print(smat.column_sums_dict())
