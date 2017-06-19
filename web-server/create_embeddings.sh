DATA_DIR=data

echo Downloading word2vec model
wget -P $DATA_DIR https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz
echo Unzipping model
gzip -d $DATA_DIR/GoogleNews-vectors-negative300.bin.gz
echo Generating reduced model embedding
python scripts/generate_reduced_model.py $DATA_DIR
echo Cleaning up
rm -f $DATA_DIR/GoogleNews-vectors-negative300.*
echo Done
