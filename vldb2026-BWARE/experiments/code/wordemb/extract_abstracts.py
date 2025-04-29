import re

def removeUnicode(fi:str):
    fi = re.sub("\\\\u[0-f]{4}", " ", fi)
    fi = re.sub("\\\\u[0-f]{3}", " ", fi)
    return fi

def removeNewline(fi:str):
    fi = fi.replace("  ", " ")
    fi = fi.replace(" .", ".")
    fi = fi.replace(" ,", ",")
    fi = fi.replace("\n", " ")
    fi = fi.replace("\r", " ")
    fi = fi.replace("\t", " ")
    fi = fi.replace("\\t", " ")
    return fi

def replaceUnicode(fi:str):
    if "\\u" in fi:    
        fi = fi.replace("\\u00b7", "*")
        fi = fi.replace("\\u2217", "*")
        fi = fi.replace("\\u009d", " ")
        fi = fi.replace("\\u2218", "*")
        fi = fi.replace("\\u0094", '"')
        fi = fi.replace("\\u3001", ",")
        fi = fi.replace("\\u204e", "*")
        fi = fi.replace("\\u0300", "'")
        fi = fi.replace("\\u211b", " set of real numbers ")
        fi = fi.replace("\\u223c", "~")
        fi = fi.replace("\\u22c5", "*")
        fi = fi.replace("\\u2286", "subset of or equal to")
        fi = fi.replace("\\u22c7", " division times ")
        fi = fi.replace("\\u2282", "subset of")
        fi = fi.replace("\\u2019", "'")
        fi = fi.replace("\\u2018", "'")
        fi = fi.replace("\\u2253", "approximately equal to ")
        fi = fi.replace("\\u00fd", "'")
        fi = fi.replace("\\u02d9", "'")
        fi = fi.replace("\\u03d1", "theta")
        fi = fi.replace("\\u2032", "'")
    if "\\u" in fi:
        fi = fi.replace("\\u0302", "^")
        fi = fi.replace("\\u03d2", " upsilon ")
        fi = fi.replace("\\u0027", "'")
        fi = fi.replace("\\u2034", "'''")
        fi = fi.replace("\\u0308", " ")
        fi = fi.replace("\\u220f", "product")
        fi = fi.replace("\\u2209", " not an element of ")
        fi = fi.replace("\\u2005", " ")
        fi = fi.replace("\\u2216", "\\")
        fi = fi.replace("\\u02bc", "'")
        fi = fi.replace("\\u00b4", "'")
        fi = fi.replace("\\u2248", "almost equal to")
        fi = fi.replace("\\u201a", "'")
        fi = fi.replace("\\u003e", "greater than")
        fi = fi.replace("\\u0092", "'")
        fi = fi.replace("\\u2245", "approximately equal to")
        fi = fi.replace("\\u00af", " overline ")
        fi = fi.replace("\\u2033", '"')
        fi = fi.replace("\\u201c", '"')
        fi = fi.replace("\\u224c", "all equal to")
        fi = fi.replace("\\u00ab", '"')
        fi = fi.replace("\\u00ab", '"')
        fi = fi.replace("\\u0084", '"')
        fi = fi.replace("\\u201d", '"')
        fi = fi.replace("\\u2013", '-')
        fi = fi.replace("\\u29f9", "\\")
        fi = fi.replace("\\u2014", '---')
        fi = fi.replace("\\u2022", " ") # bullet
        fi = fi.replace("\\ue5fc", "identical to") # custom ... is triple equals.
        fi = fi.replace("\\u2261", "identical to")
        fi = fi.replace("\\u8305", "e") # odd one .. not canonical
    if "\\u" in fi:
        fi = fi.replace("\\u2161", "roman 2")
        fi = fi.replace("\\u00a1", "!")
        fi = fi.replace("\\u008d", " ")
        fi = fi.replace("\\u007f", " ")
        fi = fi.replace("\\u2002", " ")
        fi = fi.replace("\\u0097", " ")
        fi = fi.replace("\\u0096", " ")
        fi = fi.replace("\\u2009", " ")
        fi = fi.replace("\\u01eb", "o")
        fi = fi.replace("\\u00bf", ' inverse ? ')
        fi = fi.replace("\\u016f", "u")
        fi = fi.replace("\\u2008", " ")
        fi = fi.replace("\\u03c5", "u")
        fi = fi.replace("\\u03b1", " alpha ")
        fi = fi.replace("\\u00f6", "o")
        fi = fi.replace("\\u03bc", " mu ")
        fi = fi.replace("\\u00b6", " paragraph sign ")
        fi = fi.replace("\\u00b5", " mu ")
        fi = fi.replace("\\u03c7", "CHI")
        fi = fi.replace("\\u03bb", " lambda ")
        fi = fi.replace("\\u039b", " Lambda ")
        fi = fi.replace("\\u03b5", " epsilon ")
        fi = fi.replace("\\u03c9", " omega ")
        fi = fi.replace("\\u03a9", " Omega ")
        fi = fi.replace("\\u03b4", " delta ")
        fi = fi.replace("\\u0394", " Delta ")
        fi = fi.replace("\\u03a3", " Sigma ")
        fi = fi.replace("\\u2211", " Sigma ")
        fi = fi.replace("\\u00d3", "O")
        fi = fi.replace("\\u00f3", "o")
        fi = fi.replace("\\u0141", "L")
    if "\\u" in fi:
        fi = fi.replace("\\u0170", "U")
        fi = fi.replace("\\u00ef", "i")
        fi = fi.replace("\\u0151", "o")
        fi = fi.replace("\\u010c", "C")
        fi = fi.replace("\\u00ee", "i")
        fi = fi.replace("\\u03be", " xi ")
        fi = fi.replace("\\u010d", "c")
        fi = fi.replace("\\u00c1", "A")
        fi = fi.replace("\\u03a0", "Pi")
        fi = fi.replace("\\u8070", "u")
        fi = fi.replace("\\u03b7", " eta ")
        fi = fi.replace("\\u010b", "c")
        fi = fi.replace("\\u03c4", " tau ")
        fi = fi.replace("\\u00fc", "u")
        fi = fi.replace("\\u00c2", "A")
        fi = fi.replace("\\u00f9", "u")
        fi = fi.replace("\\u22b3", " contains as normal subgroup ")
        fi = fi.replace("\\u011b", "e")
        fi = fi.replace("\\u017a", "z")
        fi = fi.replace("\\u00fa", "u")
        fi = fi.replace("\\ufffd", "u")
        fi = fi.replace("\\u203e", " overline ")
        fi = fi.replace("\\u0305", " overline ")
        fi = fi.replace("\\u00ea", "e")
        fi = fi.replace("\\u03bf", " omicron ")
        fi = fi.replace("\\u00e2", "a")
        fi = fi.replace("\\u0159", "r")
        fi = fi.replace("\\u222b", " integral ")
        fi = fi.replace("\\u00e0", "a")
        fi = fi.replace("\\u00f1", "n")
        fi = fi.replace("\\u00ec", "i")
        fi = fi.replace("\\u0161", "s")
        fi = fi.replace("\\u015f", "s")
        fi = fi.replace("\\u2061", " function application ")
        fi = fi.replace("\\u03c8", " psi ")
        fi = fi.replace("\\u03a8", " Psi ")
        fi = fi.replace("\\u2207", " backwards difference ")
        fi = fi.replace("\\u25ca", " white diamond suit ")
        fi = fi.replace("\\u0192", "f")
        fi = fi.replace("\\u0338", "/")
        fi = fi.replace("\\u00a8", "")
        fi = fi.replace("\\u03bd", "v")
        fi = fi.replace("\\u0144", "n")
        fi = fi.replace("\\u00be", " three fourths ")
        fi = fi.replace("\\u0107", "c")
    if "\\u" in fi:
        fi = fi.replace("\\u00e7", "c")
        fi = fi.replace("\\u00e3", "a")
        fi = fi.replace("\\u2605", " black star ")
        fi = fi.replace("\\u8133", "x")
        fi = fi.replace("\\u0131", "i")
        fi = fi.replace("\\u2113", " ell ")
        fi = fi.replace("\\u0301", "'")
        fi = fi.replace("\\u00e8", "e")
        fi = fi.replace("\\u00e1", "a")
        fi = fi.replace("\\u00e4", "a")
        fi = fi.replace("\\u00ed", "i")
        fi = fi.replace("\\u00f4", "o")
        fi = fi.replace("\\u00eb", "e")
        fi = fi.replace("\\u2131", "f")
        fi = fi.replace("\\u22c8", " bowtie ")
        fi = fi.replace("\\u00c8", "E")
        fi = fi.replace("\\u00c9", "E")
        fi = fi.replace("\\u227a", " precedes ")
        fi = fi.replace("\\u03b8", " theta ")
        fi = fi.replace("\\u3008", " < ")
        fi = fi.replace("\\u00a9", " copy right ")
        fi = fi.replace("\\u2122", " trade mark ")
        fi = fi.replace("\\u00ae", " registered trade mark ")
        fi = fi.replace("\\u3009", " > ")
        fi = fi.replace("\\u00e5", "aa")
        fi = fi.replace("\\u00f8", "oe")
        fi = fi.replace("\\u2308", " ceiling ")
        fi = fi.replace("\\u221a", " square root ")
        fi = fi.replace("\\u2309", "")
        fi = fi.replace("\\u00a0", " ")
        fi = fi.replace("\\u2015", " - ")
        fi = fi.replace("\\u00f7", " / ")
    if "\\u" in fi:
        fi = fi.replace("\\u2010", " - ")
        fi = fi.replace("\\u25cb", " white circle ")
        fi = fi.replace("\\u2254", " colon equals ")
        fi = fi.replace("\\u2124", " set of integers ")
        fi = fi.replace("\\u2115", " natural numbers ")
        fi = fi.replace("\\u9a74", " - ")
        fi = fi.replace("\\u2212", " - ")
        fi = fi.replace("\\u00ad", " - ")
        fi = fi.replace("\\u03b2", " beta ")
        fi = fi.replace("\\u2208", " in the set of ")
        fi = fi.replace("\\u2223", " divides ")
        fi = fi.replace("\\u2020", " cross ")
        fi = fi.replace("\\u211d", " real numbers ")
        fi = fi.replace("\\u2229", " intersection ")
        fi = fi.replace("\\u2205", " empty set ")
        fi = fi.replace("\\u00d8", " empty set ")
        fi = fi.replace("\\u00a7", " paragraph sign ")
        fi = fi.replace("\\u00a3", " pound ")
        fi = fi.replace("\\u03c0", " pi ")
        fi = fi.replace("\\u2044", " / ")
        fi = fi.replace("\\u2203", " there exists ")
        fi = fi.replace("\\u2200", " for all ")
        fi = fi.replace("\\u221e", " infinity ")
        fi = fi.replace("\\u2264", " less than or equal to ")
        fi = fi.replace("\\u2a7d", " less than or equal to ")
        fi = fi.replace("\\u2260", " not equal to ")
        fi = fi.replace("\\u2265", " greater than or equal to ")
        fi = fi.replace("\\u2a7e", " greater than or equal to ")
        fi = fi.replace("\\u00b1", " plus minus ")
        fi = fi.replace("\\u2266", " less than over equal to ")
        fi = fi.replace("\\u222a", " union ")
        fi = fi.replace("\\u22c3", " union ")
        fi = fi.replace("\\u2082", " subscript two ")
        fi = fi.replace("\\u2083", " subscript three ")
        fi = fi.replace("\\u2084", " subscript four ")
        fi = fi.replace("\\u0088", " ^ ")
    if "\\u" in fi:
        fi = fi.replace("\\u00bb", " >> ")
        fi = fi.replace("\\u0398", " Theta ")
        fi = fi.replace("\\u2295", " circled plus ")
        fi = fi.replace("\\u2298", " circled division ")
        fi = fi.replace("\\u2119", " double strick capital p ")
        fi = fi.replace("\\u2296", " circled minus ")
        fi = fi.replace("\\u2297", " circled times ")
        fi = fi.replace("\\u2228", " logical or ")
        fi = fi.replace("\\u2016", " double vertical bar ")
        fi = fi.replace("\\u03c3", " sigma ")
        fi = fi.replace("\\u021e", "H")
        fi = fi.replace("\\u25ba", " black right pointing pointer ")
        fi = fi.replace("\\u2192", " right arrow ")
        fi = fi.replace("\\u227d", " succeeds or equal to ")
        fi = fi.replace("\\u0086", " start of selected area ")
        fi = fi.replace("\\u00ba", " degree ")
        fi = fi.replace("\\u22ad", " not true equals ")
        fi = fi.replace("\\u22a8", " true equals ")
        fi = fi.replace("\\ufb01", " fi ")
        fi = fi.replace("\\u21d4", " left right double arrow ")
        fi = fi.replace("\\u2194", " left right arrow ")
        fi = fi.replace("\\u00e9", "e")
        fi = fi.replace("\\u03c6", " phi ")
        fi = fi.replace("\\u22a5", " perpendicular ")
        fi = fi.replace("\\u226a", " much less than ")
        fi = fi.replace("\\u2118", " weierstrass elliptic function ")
        fi = fi.replace("\\u2227", " logical and ")
        fi = fi.replace("\\u03d5", " Phi ")
        fi = fi.replace("\\u03b3", " gamma ")
        fi = fi.replace("\\u00c3", "A")
        fi = fi.replace("\\u02c6", " ^ ")
        fi = fi.replace("\\u00c6", "AE")
    if "\\u" in fi:
        fi = fi.replace("\\u030a", " degree ")
        fi = fi.replace("\\u0303", " ~ ")
        fi = fi.replace("\\u00bd", " one half ")
        fi = fi.replace("\\u0393", " gamma ")
        fi = fi.replace("\\u00f0", " eth ")
        fi = fi.replace("\\u03a6", " Phi ")
        fi = fi.replace("\\u00a6", " broken bar ")
        fi = fi.replace("\\u20ac", " euro ")
        fi = fi.replace("\\u03c1", " rho ")
        fi = fi.replace("\\u22a2", " yields ")
        fi = fi.replace("\\u22a3", " does not yield ")
        fi = fi.replace("\\u03ba", " kappa ")
        fi = fi.replace("\\u2225", " parallel to ")
        fi = fi.replace("\\u00b0", " degree ")
        fi = fi.replace("\\ue020", "g")
        fi = fi.replace("\\u00ac", " not sign ")
        fi = fi.replace("\\u2135", " first transfinite cardinal")
        fi = fi.replace("\\u02dc", " ~ ")
        fi = fi.replace("\\u03f5", " epsilon ")
        fi = fi.replace("\\u00a2", " cent sign ")
        fi = fi.replace("\\u21d2", " right double arrow ")
        fi = fi.replace("\\u00d7", " cartesian product ")
        fi = fi.replace("\\u22c6", " star operator ")
        fi = fi.replace("(\\ud835\\udcb1)", "(V)") # specific case... not encode
        fi = fi.replace("\\u0083", " function ")
        fi = fi.replace("\\u00cf", "i")
        fi = fi.replace("\\u2aeb", " independence ")
        fi = fi.replace("\\u250c", " box drawing top left ")
        fi = fi.replace("\\u2aa1", " double nested less than ")
        fi = fi.replace("\\u2271", " neither greater than nor equal to ")
        fi = fi.replace("\\u2510", " box drawing top right ")
        fi = fi.replace("\\u2026", " ... ")
        fi = fi.replace("\\u02da", " degree ")
        fi = fi.replace("\\u22ef", " ... ")
        fi = fi.replace("\\u2215", " / ")
    if "\\u" in fi:
        fi = fi.replace("\\u230a", " floor ")
        fi = fi.replace("\\u230b", "")
        fi = fi.replace("\\u2243", " asymptotically equal to ")
        fi = fi.replace("\\u2329", " < ")
        fi = fi.replace("\\u2213", " plus or minus sign ")
        fi = fi.replace("\\u2193", " downwards arrow ")
        fi = fi.replace("\\u2190", " leftwards arrow ")
        fi = fi.replace("\\u21a6", " rightwards arrow ")
        fi = fi.replace("\\u232a", " > ")
        fi = fi.replace("\\u203a", " > ")
        fi = fi.replace("\\u2202", " partial differential ")
        fi = fi.replace("\\u03b6", " zeta ")
        fi = fi.replace("\\u2021", "f") # should be double dagger, but is f in the abstract where it is used
        fi = fi.replace("\\u00e6", "ae")

    # if "\\u" in fi:# three character embeddings
        # fi = fi.replace("\\u00d", " thorn ")
    return fi

s = 0
n = 10000000
c = 0

errors = 0

a_out = open("data/w2v/dblp_v14_abstracts.txt", "w")
m_out = open("data/w2v/dblp_v14_meta.csv", "w")

first = True
with open("data/w2v/dblp_v14.json", "r") as f:
    for l in f:
        if len(l) < 10:
            continue
        if c < s:
            c += 1
        if '"abstract": ""' in l: # empty abstract
            continue
        
        if not '"lang": "en"' in l:
            continue
        fi = l.split('"abstract": "')[1].split('", "')[0].replace('\\"', '"')
       


        number_spaces = fi.count(" ")
        if number_spaces < 30 or number_spaces > 1000:
            continue


        if "\\end{document}" in fi or "\\\\begin{array}" in fi:
            continue
        if " de la " in fi or " par le " in fi or " Une technique " in fi:
            continue ## french
        if "Asanapplicationofthesenotionsofforcing" in fi:
            continue ## error ....
        if "In dieser Arbeit" in fi or " und wird " in fi or " ein neues " in fi or " der ein " in fi:
            continue ## German
        if "\\u00a8" in fi:
            continue ## misformatted umlaud
        if "\\ue3a" in fi:
            continue # misuse of unicode.
        if "\\\Big" in fi:
            continue # this is a heavy math abstract that does not parse nicely.
        if "is op en " in fi:
            continue # Is this dutch?


        fi = fi.replace("\\n", ' ')
        fi = fi.replace("\\r", ' ')
        if "\\u" in fi:
            if "\\u8059" in fi or "\\u806f" in fi or "\\uf6d9" in fi or "\\u5364" in fi or "\\u8117" in fi:
                continue
            if "\\u8072" in fi or "\\ue5f8" in fi or "\\u807d" in fi or "\\u8302" in fi or "\\u622e" in fi:
                continue # invalid
            if "\\u00e4" in fi or "\\u864f" in fi or "\\uf8e8" in fi:
                continue # ä
            if "\\u00df" in fi:
                continue # ß 
            if "\\u00dc" in fi:
                continue # ü
        fi = replaceUnicode(fi)
        # fi = fi.replace("\\u2265", "greater than or equal to")

        if "a exploracao e a" in fi or "les proprietes" in fi or " e uso de " in fi or "Resumo" in fi:
            continue ## Spanish
        
        if "</font>" in fi or "</font >" in fi:
            continue
        
        fi = re.sub('<[^<]+>', "", fi)

        b = fi
        fi = removeUnicode(fi)

        if b != fi:
            print("")
            print(b)
            print("")
            print(fi)
            print("")
            print("-"*20)
            errors += 1
            # break
        
        fi = removeNewline(fi)


        title = l.split('"title": "')[1].split('", "')[0].replace('\\"', '"')

        title = replaceUnicode(title)

        if "nas Revis" in title or "e Acesso ao" in title  or "real com requisitos" in title:
            continue; # spanish
        
        title = re.sub('<[^<]+>', "", title)

        title2 = removeUnicode(title)

        if title != title2:
            print(title)
            print(title2)
            continue

        title2 = removeNewline(title2)

 
        year = l.split('"year": ')[1].split(', "')[0]
        m_out.write(year.strip())
        m_out.write(",")

        m_out.write(title2)
        m_out.write("\n")
        # m_out.write(",")
        # m_out.write(fi)

        if "\\\\" in fi:
            fi = fi.replace("\\\\mathcal", "")
            fi = fi.replace("\\\\mathbb", "")
            fi = fi.replace("\\\\times", " * ")
            fi = fi.replace('\\\\"', '"')
            fi = fi.replace("\\\\bf", "")
            fi = fi.replace("\\\\alpha", " alpha ")
            fi = fi.replace("\\\\in" , " in ")
            fi = fi.replace("\\\\it", "")
            fi = fi.replace("\\\\cup", " set union ")
            fi = fi.replace("\\\\em", "")
            fi = fi.replace("\\\\dots", " ... ")
            fi = fi.replace("\\\\cal", "")
            fi = fi.replace("\\\\epsilon", " epsilon ")
            fi = fi.replace("\\\\linebreak", "")
            fi = fi.replace("\\\\overline", " overline ")
            fi = fi.replace("\\\\sqrt", " square root ")
            fi = fi.replace("\\\\oplus", " circled plus ")
            fi = fi.replace("\\ ", " ")
            fi = fi.replace("\\\\le", " less than equal ")
            fi = fi.replace("\\\\cdot", " * ")
            fi = fi.replace("\\\\geq", " greater than or equal to ")
            fi = fi.replace("\\\\mathbf", "")
            fi = fi.replace("\\\\hat", " circumflex ")
            fi = fi.replace("&quot;", '"')
        
        if "\\\\" in fi:
            fi = re.sub(r"\\\\frac\{([0-9a-zA-Z + - () \\]*)\}\{([0-9a-zA-Z + - () \\]*)\}" , r' ( \1 / \2 ) ',fi)
            fi = re.sub(r"\\\\cite[ ]*\{.*\}", "", fi) ## remove cite code.

            fi = fi.replace("\\\\frac", " divide ")

        fi = re.sub(' +', " ", fi)
        fi = re.sub('<[^<]+>', "", fi)
        fi = fi.strip()

        a_out.write(fi)
        a_out.write("\n")

        # if errors == 1: 
        #     break
        c += 1 
        if n == c:
            break


a_out.flush()
a_out.close()

m_out.flush()
m_out.close()

print("Errors : ", errors, "of:" , c)