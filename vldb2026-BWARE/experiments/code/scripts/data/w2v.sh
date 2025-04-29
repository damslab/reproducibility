
# https://fasttext.cc/docs/en/english-vectors.html
wget https://dl.fbaipublicfiles.com/fasttext/vectors-english/wiki-news-300d-1M.vec.zip
tail -n +2 data/w2v/wiki-news-300d-1M.vec > data/w2v/wiki-news-300d-1M.vec.t
rm data/w2v/wiki-news-300d-1M.vec
mv data/w2v/wiki-news-300d-1M.vec.t data/w2v/wiki-news-300d-1M.vec


echo '{"data_type": "frame","rows": 999995,"cols": 301,"format": "csv","header": false,"sep": " ",}' \
    > data/w2v/wiki-news-300d-1M.vec.mtd


wget https://lfs.aminer.cn/lab-datasets/aminerdataset/AMiner-Paper.rar \
    -o data/w2v/AMiner-Paper.rar


