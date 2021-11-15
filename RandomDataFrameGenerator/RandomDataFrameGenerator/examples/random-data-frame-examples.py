import random
import numpy.random
from RandomDataFrameGenerator import random_data_frame
from RandomDataFrameGenerator import random_word
from RandomDataFrameGenerator import random_pet_name
from RandomDataFrameGenerator import random_string

random.seed(991)
print(random_data_frame())

print(120 * "=")
print(random_data_frame(8, ['FL', 'CA', 'MA', 'SC'],
                        generators={'FL': random_pet_name,
                                    "CA": random_string,
                                    "MA": random_word,
                                    "SC": numpy.random.normal}))
