import os, sys
script_dir = os.path.dirname(os.path.abspath(__file__))
# print(script_dir)
sys.path.insert(0,script_dir)

from retro_star.api import RSPlanner
from time import time
import argparse

def run_retro_planner(product='CCCCC', blocks='data/building_block.csv', iterations=100, exp_topk=10, route_topk=10,
                      beam_size=10, model_type='ensemble', retrieval='true', path_retrieval='true',
                      retrieval_db='data/train_canonicalized.txt', path_retrieval_db='data/pathways.pickle',
                      device='cuda'):

    t_start = time()

    planner = RSPlanner(
        cuda=device == 'cuda',
        iterations=iterations,
        expansion_topk=exp_topk,
        route_topk=route_topk,
        beam_size=beam_size,
        model_type=model_type,
        retrieval=retrieval == 'true',
        retrieval_db=os.path.join(script_dir,retrieval_db),
        path_retrieval=path_retrieval == 'true',
        path_retrieval_db=os.path.join(script_dir,path_retrieval_db),
        starting_molecules=os.path.join(script_dir,blocks)
    )
    result = planner.plan(product)

    if result is None:
        print('None')
    else:
        for i, route in enumerate(result):
            print(f'{i} {route}')

    print(f'\033[92mTotal {time() - t_start:.2f} sec elapsed\033[0m')