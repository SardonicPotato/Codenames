import sys, os
from subprocess import call
from solver.util import generated_reduced_model

data_dir = sys.argv[1]

print ("Downloading word2vec model.")
call(["wget", "-c", "-P", data_dir, "https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz"])
print ("Unzipping model.")
call(["gzip", "-d", os.path.join(data_dir, "GoogleNews-vectors-negative300.bin.gz")])
print ("Generating reduced model embedding.")
generated_reduced_model(input_path=os.path.join(data_dir, "GoogleNews-vectors-negative300.bin"),
                        output_dir=data_dir,
                        reduced_size=100000)
print ("Cleaning up.")
call(["rm", "-f", os.path.join(data_dir, "GoogleNews-vectors-negative300.bin.gz")])
call(["rm", "-f", os.path.join(data_dir, "GoogleNews-vectors-negative300.bin")])
