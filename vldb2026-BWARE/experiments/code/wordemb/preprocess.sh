#!/bin/bash

mkdir -p results/wordemb/createLog/
mkdir -p data/w2v

if [[ ! -f "data/w2v/dblp_v14.tar.gz" ]]; then
      #https://cn.aminer.org/citation
      # wget https://originalfileserver.aminer.cn/misc/dblp_v14.tar.gz

      cd data/w2v
      wget https://originalfileserver.aminer.cn/misc/dblp_v14.tar.gz &
      cd ../../
fi


if [[ ! -f "data/w2v/wiki-news-300d-1M.vec.zip" ]]; then
      cd data/w2v
      wget https://dl.fbaipublicfiles.com/fasttext/vectors-english/wiki-news-300d-1M.vec.zip &
      cd ../../
fi

## wait for the download to finish
wait

if [[ ! -f "data/w2v/dblp_v14.json" ]]; then
      echo "Extracting the dblp_v14.tar.gz"
      cd data/w2v
      tar -xvzf dblp_v14.tar.gz &
      cd ../../
fi

if [[ ! -f "data/w2v/wiki-news-300d-1M.vec" ]]; then
      cd data/w2v
      unzip -p wiki-news-300d-1M.vec.zip > wiki-news-300d-1M.vec
      tail -n +2 wiki-news-300d-1M.vec > wiki-news-300d-1M.vec.t
      rm wiki-news-300d-1M.vec
      mv wiki-news-300d-1M.vec.t wiki-news-300d-1M.vec
      cd ../../
fi


if [[ ! -f "data/w2v/wiki-news-300d-1M.vec.mtd" ]]; then
      echo "Making metadata file for word emb"

      cd data/w2v
      echo '{
    "data_type": "frame",
    "rows": 999995,
    "cols": 301,
    "format": "csv",
    "header": true,
    "sep": " ",
}' > wiki-news-300d-1M.vec.mtd
      cd ../../
fi


# preprocess
conf="code/conf/ULAb16.xml"

# if [[ ! -f "data/w2v/wiki-news-300d-1M.vec_999995.words.bin" ]]; then
#       echo "extracting words and embeddings to frame and matrix using SystemDS"

#       systemds \
#           code/wordemb/splitToFrameAndMatrix.dml \
#           -config $conf \
#           -stats 100 -debug \
#           -exec singlenode \
#           -args "data/w2v/wiki-news-300d-1M.vec" 1000 \
#           >> "results/wordemb/createLog/1k-$(date +"%m-%d-%y-%r").log" 2>&1 &
      
#       systemds \
#           code/wordemb/splitToFrameAndMatrix.dml \
#           -config $conf \
#           -stats 100 -debug \
#           -exec singlenode \
#           -args "data/w2v/wiki-news-300d-1M.vec" 3000 \
#           >> "results/wordemb/createLog/3k-$(date +"%m-%d-%y-%r").log" 2>&1 &

#       systemds \
#           code/wordemb/splitToFrameAndMatrix.dml \
#           -config $conf \
#           -stats 100 -debug \
#           -exec singlenode \
#           -args "data/w2v/wiki-news-300d-1M.vec" 10000 \
#           >> "results/wordemb/createLog/10k-$(date +"%m-%d-%y-%r").log" 2>&1 &

#       systemds \
#           code/wordemb/splitToFrameAndMatrix.dml \
#           -config $conf \
#           -stats 100 -debug \
#           -exec singlenode \
#           -args "data/w2v/wiki-news-300d-1M.vec" 100000 \
#           >> "results/wordemb/createLog/100K-$(date +"%m-%d-%y-%r").log" 2>&1 &

#       systemds \
#           code/wordemb/splitToFrameAndMatrix.dml \
#           -config $conf \
#           -stats 100 -debug \
#           -exec singlenode \
#           -args "data/w2v/wiki-news-300d-1M.vec" 1000000 \
#           >> "results/wordemb/createLog/1M-$(date +"%m-%d-%y-%r").log" 2>&1
#        echo "Done: extracting words and embeddings to frame and matrix using SystemDS"

# fi

wait

# Extract all abstracts
if [[ ! -f "data/w2v/dblp_v14_abstracts.txt" ]]; then
      python3 code/wordemb/extract_abstracts.py
fi


pyEncode() {
      echo "Encoding abstracts in different variations... can take > 30 minutes"
      # Encode abstracts
      # python3 code/wordemb/lookup.py --words 1000 --abstracts 1000 --maxLength 1000 &
      # python3 code/wordemb/lookup.py --words 1000 --abstracts 3000 --maxLength 1000 &
      # python3 code/wordemb/lookup.py --words 1000 --abstracts 10000 --maxLength 1000 &
      # python3 code/wordemb/lookup.py --words 1000 --abstracts 30000 --maxLength 1000 &
      # python3 code/wordemb/lookup.py --words 1000 --abstracts 100000 --maxLength 1000 &
      # python3 code/wordemb/lookup.py --words 1000 --abstracts 300000 --maxLength 1000 &
      # python3 code/wordemb/lookup.py --words 1000 --abstracts 1000000 --maxLength 1000 &
      # # python3 code/wordemb/lookup.py --words 1000 --abstracts 4000000 --maxLength 1000 &
      # python3 code/wordemb/lookup.py --words 3000 --abstracts 1000 --maxLength 1000 &
      # python3 code/wordemb/lookup.py --words 3000 --abstracts 3000 --maxLength 1000 &
      # python3 code/wordemb/lookup.py --words 3000 --abstracts 10000 --maxLength 1000 &
      # python3 code/wordemb/lookup.py --words 3000 --abstracts 30000 --maxLength 1000 &
      # python3 code/wordemb/lookup.py --words 3000 --abstracts 100000 --maxLength 1000 &
      # python3 code/wordemb/lookup.py --words 3000 --abstracts 300000 --maxLength 1000 &
      # python3 code/wordemb/lookup.py --words 3000 --abstracts 1000000 --maxLength 1000 &
      # # python3 code/wordemb/lookup.py --words 3000 --abstracts 4000000 --maxLength 1000 &
      # python3 code/wordemb/lookup.py --words 10000 --abstracts 1000 --maxLength 1000 &
      # python3 code/wordemb/lookup.py --words 10000 --abstracts 3000 --maxLength 1000 &
      # python3 code/wordemb/lookup.py --words 10000 --abstracts 10000 --maxLength 1000 &
      # python3 code/wordemb/lookup.py --words 10000 --abstracts 30000 --maxLength 1000 &
      # python3 code/wordemb/lookup.py --words 10000 --abstracts 100000 --maxLength 1000 &
      # python3 code/wordemb/lookup.py --words 10000 --abstracts 300000 --maxLength 1000 &
      # python3 code/wordemb/lookup.py --words 10000 --abstracts 1000000 --maxLength 1000 &
      # # python3 code/wordemb/lookup.py --words 10000 --abstracts 4000000 --maxLength 1000 &
      # python3 code/wordemb/lookup.py --words 100000 --abstracts 1000 --maxLength 1000 &
      # python3 code/wordemb/lookup.py --words 100000 --abstracts 3000 --maxLength 1000 &
      # python3 code/wordemb/lookup.py --words 100000 --abstracts 10000 --maxLength 1000 &
      # python3 code/wordemb/lookup.py --words 100000 --abstracts 30000 --maxLength 1000 &
      # python3 code/wordemb/lookup.py --words 100000 --abstracts 100000 --maxLength 1000 &
      # python3 code/wordemb/lookup.py --words 100000 --abstracts 300000 --maxLength 1000 &
      python3 code/wordemb/lookup.py --words 100000 --abstracts 1000000 --maxLength 1000 &
      # python3 code/wordemb/lookup.py --words 100000 --abstracts 4000000 --maxLength 1000 &
      # python3 code/wordemb/lookup.py --words 999995 --abstracts 1000 --maxLength 1000 &
      # python3 code/wordemb/lookup.py --words 999995 --abstracts 3000 --maxLength 1000 &
      # python3 code/wordemb/lookup.py --words 999995 --abstracts 10000 --maxLength 1000 &
      # python3 code/wordemb/lookup.py --words 999995 --abstracts 30000 --maxLength 1000 &
      # python3 code/wordemb/lookup.py --words 999995 --abstracts 100000 --maxLength 1000 &
      # python3 code/wordemb/lookup.py --words 999995 --abstracts 300000 --maxLength 1000 &
      # python3 code/wordemb/lookup.py --words 999995 --abstracts 1000000 --maxLength 1000 &
      # python3 code/wordemb/lookup.py --words 999995 --abstracts 4000000 --maxLength 1000 &

      echo "Done: Encoding abstracts in different variations... can take > 30 minutes"
    
}

# nIjv=$(find data/w2v/ -name '*.ijv' -printf '.' | wc -m)
# echo $nIjv
# if [[ $nIjv != 24 ]]; then 
      pyEncode
# fi

wait 

toB() {
      mkdir -p results/wordemb/toBinary/
      # if [[ ! -f "data/w2v/$1.bin" ]] && [[ ! -d "data/w2v/$1.bin" ]]; then
            systemds \
                  code/wordemb/toBinary.dml \
                  -config $conf \
                  -stats 100 -debug \
                  -exec singlenode \
                  -args "data/w2v/$1.csv" \
                        "data/w2v/$1.bin" \
                  >> "results/wordemb/toBinary/${1}_embeddin_$(date +"%m-%d-%y-%r").log" 2>&1
      # fi 
}

# toB dblp_v14_abstracts_embedded_1000_1000 &
# toB dblp_v14_abstracts_embedded_1000_3000 &
# toB dblp_v14_abstracts_embedded_1000_10000 &
# toB dblp_v14_abstracts_embedded_1000_30000 &
# toB dblp_v14_abstracts_embedded_1000_100000 &
# toB dblp_v14_abstracts_embedded_1000_300000 &
# toB dblp_v14_abstracts_embedded_1000_1000000 &
# toB dblp_v14_abstracts_embedded_3000_1000 &
# toB dblp_v14_abstracts_embedded_3000_3000 &
# toB dblp_v14_abstracts_embedded_3000_10000 &
# toB dblp_v14_abstracts_embedded_3000_30000 &
# toB dblp_v14_abstracts_embedded_3000_100000 &
# toB dblp_v14_abstracts_embedded_3000_300000 &
# toB dblp_v14_abstracts_embedded_3000_1000000 &

# wait 
# # toB dblp_v14_abstracts_embedded_1000_4000000 &
# toB dblp_v14_abstracts_embedded_10000_1000 &
# toB dblp_v14_abstracts_embedded_10000_3000 &
# toB dblp_v14_abstracts_embedded_10000_10000 &
# toB dblp_v14_abstracts_embedded_10000_30000 &
# toB dblp_v14_abstracts_embedded_10000_100000 &
# toB dblp_v14_abstracts_embedded_10000_300000 &
# toB dblp_v14_abstracts_embedded_10000_1000000 &
# # toB dblp_v14_abstracts_embedded_10000_4000000 &
# toB dblp_v14_abstracts_embedded_100000_1000 &
# toB dblp_v14_abstracts_embedded_100000_3000 &
# toB dblp_v14_abstracts_embedded_100000_10000 &
# toB dblp_v14_abstracts_embedded_100000_30000 &
# toB dblp_v14_abstracts_embedded_100000_100000 &
# toB dblp_v14_abstracts_embedded_100000_300000 &
toB dblp_v14_abstracts_embedded_100000_1000000 &

wait 

# # toB dblp_v14_abstracts_embedded_100000_4000000 &
# toB dblp_v14_abstracts_embedded_999995_1000 &
# toB dblp_v14_abstracts_embedded_999995_3000 &
# toB dblp_v14_abstracts_embedded_999995_10000 &
# toB dblp_v14_abstracts_embedded_999995_30000 &
# toB dblp_v14_abstracts_embedded_999995_100000 &
# toB dblp_v14_abstracts_embedded_999995_300000 &
# toB dblp_v14_abstracts_embedded_999995_1000000 &
# # toB dblp_v14_abstracts_embedded_999995_4000000 &

# wait


rm -r data/w2v/*.crc