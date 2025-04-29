

import io

def load_words(fname):
    fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
   
    data = set()
    c = 0
    with open(fname+".filtered.vec", "w") as fout:
        for line in fin:
            c += 1
            tokens = line.rstrip().split(' ', maxsplit=1)
            key = tokens[0]
            key = str.lower(key)
            if key not in data:
                data.add(key)
                fout.write(line)

    fin.close()
    print(c, len(data))

load_words("data/w2v/wiki-news-300d-1M.vec")