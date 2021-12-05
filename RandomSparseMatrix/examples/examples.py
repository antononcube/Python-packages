import random

from RandomDataGenerators import *
from RandomSparseMatrix import *

random.seed(324)
matJobs = random_sparse_matrix(
    n_rows=12,
    columns_spec=5,
    row_names_generator=random_pet_name,
    column_names_generator=random_pretentious_job_title,
    generators=lambda size: [random.random() for i in range(size)],
    min_number_of_values=12,
    max_number_of_values=None)

matJobs.print_matrix()
