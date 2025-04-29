import io

def load_vectors(fname):
    fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
    n, d = map(int, fin.readline().split())
    data = {}

    # n = 1000
    c = 0
    for line in fin:
        tokens = line.rstrip().split(' ')
        data[tokens[0]] = tokens[1:]
        c += 1
        if (c >= n):
            break
    return data


vectorFile = "data/w2v/wiki-news-300d-1M.vec"

d = load_vectors(vectorFile)

print(d)
for x in (d["competitor"]):
    print(x, end=" ")