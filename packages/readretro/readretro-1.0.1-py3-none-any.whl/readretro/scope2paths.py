from tqdm import tqdm
from rdkit import Chem
import pandas as pd
import os, sys
import multiprocessing as mp
import numpy as np

def worker(q, thread_id, rootpath, target):
    msg = run_rp2(thread_id, rootpath, target)
    q.put(msg)

def listener(q):
    while True:
        m = q.get()
        if m == '#done#':
            break

def run_rp2(thread_id, rootpath, targets):
    print(f'[Thread {thread_id}] start ({len(targets)} targets)')
    if not os.path.exists(f"{rootpath}/paths"):
            os.mkdir(f'{rootpath}/paths')
    for target in targets:
        os.system(f"python -m rp2paths all {rootpath}/{target} --outdir {rootpath}/paths/{target.replace('.csv','')}")
    return(f'{target} done')

if __name__ == '__main__':
    root = '/home/taein/Retrosynthesis/rp2paths/examples'
    scope = os.listdir(root)
    scope = [i for i in scope if '_scope.csv' in i]
    num_threads = 1

    idx_split = np.array_split(range(len(scope)), num_threads)
    idx_split = [(i[0], i[-1] + 1) for i in idx_split]

    manager = mp.Manager()
    q = manager.Queue()
    file_pool = mp.Pool(1)
    file_pool.apply_async(listener, (q))

    pool = mp.Pool(num_threads)
    jobs = []
    for i in range(num_threads):
        start, end = idx_split[i]
        job = pool.apply_async(worker, (q, i, root, scope[start:end]))
        jobs.append(job)

    for job in jobs:
        job.get()

    q.put('#done#')
    pool.close()
    pool.join()