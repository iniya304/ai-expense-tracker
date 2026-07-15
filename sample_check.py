import os
import random

folder = 'data/ocr_output'
files = [f for f in os.listdir(folder) if f.endswith('.txt')]

random.seed(42)  # so we get the same "random" list every time we run this
sample = random.sample(files, 15)

print("Review these 15 files:")
for f in sample:
    print(f)