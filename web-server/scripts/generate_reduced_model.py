import os
import sys

from solver.util import generate_reduced_model

try:
    data_dir = sys.argv[1]
except IndexError:
    data_dir = "../data"

generate_reduced_model(input_path=os.path.join(data_dir, "GoogleNews-vectors-negative300.bin"),
                        output_dir=data_dir,
                        reduced_size=100000)
