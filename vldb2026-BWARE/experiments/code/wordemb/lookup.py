

import io

import argparse


def load_words(fname, words):
    fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
    
    data = {}

    c = 1
    for line in fin:
        tokens = line.rstrip().split(' ', maxsplit=1)
        data[tokens[0]] = c 
        c += 1
        if c >= words:
            break
    return data

def split_d(s, delim):
    ss = s.split(delim, 1)
    if len(ss[0]) == 0:
        return (delim, ss[1])
    elif len(ss[1]) == 0:
        return (ss[0], delim)
    else:
        return (ss[0], delim + ss[1])

def split(s):
    if "'" in s:
        return split_d(s, "'")
    elif '"' in s:
        return split_d(s, '"')
    elif "." in s:
        return split_d(s, '.')
    elif "," in s:
        return split_d(s, ',')
    elif "-" in s:
        return split_d(s, '-')
    elif ";" in s:
        return split_d(s, ';')
    elif ":" in s:
        return split_d(s, ':')
    elif "(" in s:
        return split_d(s, '(')
    elif ")" in s:
        return split_d(s, ')')
    elif "/" in s:
        return split_d(s, '/')
    elif "[" in s:
        return split_d(s, '[')
    elif "]" in s:
        return split_d(s, ']')
    elif "{" in s:
        return split_d(s, '{')
    elif "}" in s:
        return split_d(s, '}')
    elif "+" in s:
        return split_d(s, '+')
    elif "#" in s:
        return split_d(s, '#')
    elif "=" in s:
        return split_d(s, '=')
    elif "&" in s:
        return split_d(s, '&')
    elif "<" in s:
        return split_d(s, '<')
    elif ">" in s:
        return split_d(s, '>')
    elif "!" in s:
        return split_d(s, '!')
    elif "?" in s:
        return split_d(s, '?')
    elif "*" in s:
        return split_d(s, '*')
    elif "%" in s:
        return split_d(s, '%')
    elif "$" in s:
        return split_d(s, '$')
    elif "^" in s:
        return split_d(s, '^')
    elif "@" in s:
        return split_d(s, '@')
    elif "_" in s:
        if len(s) == 1:
            return ["underscore"]
        return split_d(s, '_')
    elif "\\\\" == s:
        return ["\\"]
    else:
        return s
    
def embed(w, d, emb, unknown):
    errors = 0
    if w in d:
        emb.append(d[w])
    elif len(w) == 1:
        emb.append(unknown)
        errors += 1
    else:
        s = split(w) # try to split
        if isinstance(s, tuple) or isinstance(s, list):
            for s in split(w):
                errors += embed(s, d, emb, unknown) 
        else:
            if str.lower(w) in d:
                emb.append(d[str.lower(w)])
            else:
                emb.append(unknown)
                errors += 1

    return errors



parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--words', type=int, required=True,
                    help='an integer for how many words to use')
parser.add_argument('--abstracts', type= int, required=True,
                    help='an integer for how many abstracts to use')
parser.add_argument('--maxLength', type=int, required =True, 
                    help='an integer for how many tokens abstracts are padded to' )
args = parser.parse_args()

maxLength = args.maxLength
c = 0 # rows
n = args.abstracts
with open("data/w2v/dblp_v14_abstracts.txt", "r") as f:
    with open("data/w2v/dblp_v14_abstracts_embedded_{words}_{abstracts}.csv".format(words= args.words, abstracts = args.abstracts)
        , "w") as o:
  
        d = load_words("data/w2v/wiki-news-300d-1M.vec", args.words)
        # print(len(d))
        for l in f:
            
            sp = l.strip().split(" ")
            emb = []
            # print("")
            for w in sp:
                errors = embed(w, d, emb, args.words)
            # if errors   > 0:
                # print(errors, end=" ")
            # else:
                # print(".", end ="")
            # if errors > 0:
                # print("---"*20)
                # print(l)
                # print(emb)
                # print("---"*20)

            if len(emb) >= maxLength:
                for i in emb[:maxLength-1]:
                    o.write(str(i))
                    o.write(",")
                o.write(str(emb[-1]))
                o.write("\n")
            else:
                for i in emb:
                    o.write(str(i))
                    o.write(",")
                for i in range(len(emb), maxLength-1):
                    o.write(str(args.words))
                    o.write(",")
                o.write(str(args.words))
                o.write("\n")
                
            c += 1
            if n == c:
                break
print("\n\nDone embedding using {words} words and {abstracts} abstracts to data/w2v/dblp_v14_abstracts_embedded_{words}_{abstracts}.csv".format(words= args.words, abstracts = args.abstracts))


with open("data/w2v/dblp_v14_abstracts_embedded_{words}_{abstracts}.csv.mtd".format(words= args.words, abstracts = args.abstracts)
          , "w") as o:
    mtd = """
    \"data_type\": \"matrix\",
    \"rows\": {c},
    \"cols\": {maxLength},
    \"format\": \"csv\",
""".format( c= c, maxLength= maxLength)
    o.write("{")
    o.write(mtd)
    o.write("}")
print(maxLength)