from RandomDataGenerators import *
import random
import pandas
import numpy

pandas.set_option('display.max_columns', 20)

# Here we generate thousands of random data frames with
# different types of arguments.
# A random data frame is expected every time.

# random.seed(13)

my_indexes = list(range(1, 30)) + [None, ]

my_gen_funcs = [random_pet_name,
                random_word,
                [list("abcdefgh"), random_word(3)],
                lambda size: random_string(size),
                [random_pet_name, random_word, random_string, numpy.random.normal],
                None]

for rs in range(1, 6000):
    random.seed(rs)
    print("random seed:", rs)

    arg1 = random.choice(my_indexes)
    arg2 = random.choice(my_indexes)
    arg3 = random.choice([random_pet_name, random_word, random_string, numpy.random.normal, None])
    arg4 = random.choice(my_gen_funcs)

    args_dict = {"n_rows": arg1,
                 "columns_spec": arg2,
                 "column_names_generator": arg3,
                 "generators": arg4}

    print(args_dict)

    dfTest = random_data_frame(
        n_rows=arg1,
        columns_spec=arg2,
        column_names_generator=arg3,
        generators=arg4
    )

    if not isinstance(dfTest, pandas.core.frame.DataFrame):
        print("Not a data frame for random seed:", rs)

print("All ok.")
