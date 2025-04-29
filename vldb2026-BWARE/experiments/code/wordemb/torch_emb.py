
import argparse 
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import torch
import time 


start = time.time()

parser = argparse.ArgumentParser()
parser.add_argument('--words', type=int, required=True,
                    help='an integer for how many words to use')
parser.add_argument('--abstracts', type= int, required=True,
                    help='an integer for how many abstracts to use')
parser.add_argument(
    "--abstractlength",
      type=int,
    required=True,
    help="an integer for how long abstracts are",
)
args = parser.parse_args()

print("ParseTime:       " ,(time.time()-start))
start = time.time()
A = torch.randint(1, args.words, (args.abstracts, args.abstractlength))
embedding_layer = torch.nn.Embedding(args.words, 300, dtype=torch.float64)
print("embedding Alloc: " , (time.time()-start))
for i in range(10):
    start = time.time()
    res = embedding_layer(A)
    print("embed:           " , (time.time()-start))
    start = time.time()

colSum = torch.mean(res, 1)
print(colSum)
print("colsum           " , (time.time()-start))
start = time.time()
