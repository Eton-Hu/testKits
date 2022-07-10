import os 
import numpy as np
from pathlib import Path
import glob
import pandas as pd
from tqdm import tqdm

import matplotlib.pyplot as plt

ROOT = r'C:\Users\ZOE ZHAO\Desktop\yolov5-master\runs\detect\exp20\labels'
HEAD = r'\image_'
start_from = 10001
suffix = '.txt'
counter = 0

# fillin undetected label files
for i in range(3455):
    file_name = Path(ROOT+HEAD+str(start_from)+suffix)
    if not file_name.exists():
        print(file_name)
        counter = counter+1
        with open(file_name, 'w') as f:
            pass
    start_from = start_from + 1
print('None label detected image number = ',counter)

# Enhancing confidence
def expand_confidence(x: int, factor = 3):
    return -(abs((x-1) ** factor)) +1

# Verify a image lable from a txt file
# input: txt file location
# output: imagename, [lable1, confidence1, x1, y1, w1, h1,lable2, confidence2, x2, y2, w2, h2,...]
def verify_lables(lb_file):
    image_name =  os.path.basename(lb_file)
    image_name = image_name.split('.', 1)[0]
    if os.path.isfile(lb_file):
        with open(lb_file) as f:
            lb = [x.split() for x in f.read().strip().splitlines() if len(x)]
            if lb:
                lb = np.array(lb, dtype=np.float32)
                # print(lb[:,1])
                lb[:,1] = list(map(lambda x: expand_confidence(x,3), lb[:,1]))
                # print(type(lb[:,1]),lb[:,1])
                lb = list(lb.flat )
                lb = [int(x) if x in [0.0,1.0,2.0] else x for x in lb]
            else:
                lb = []
        return image_name, lb

# Search for lable file list
def lable_list(path):
    try:
        f = []  # label files
        print("len(path):",len(path))
        for p in path if isinstance(path, list) else [path]:
            p = Path(p)  # os-agnostic
            print(p)
            if p.is_dir():  # dir
                f += glob.glob(str(p / '**' / '*.*'), recursive=True)
        print("len(f):",len(f))
        lb_files = sorted(x.replace('/', os.sep) for x in f)
        assert lb_files, f'No lable found'
    except Exception as e:
        raise Exception(f'Error loading data from {path}: {e}')
    return lb_files


lb_files = lable_list(ROOT)

print(lb_files[3348])

lb_file = lb_files[0]
submission = pd.DataFrame(columns = ['PredictionString'])
submission.index.name = 'ImageId'

for lb_file in tqdm(lb_files):
#for lb_file in lb_files:
    im_name, lb = verify_lables(lb_file)
    submission.loc[im_name] = ' '.join(map(str,lb))

print("Size of lable files:",len(lb_files))
print(len(submission))

submission.to_csv(os.path.join(ROOT,'submission.csv'))