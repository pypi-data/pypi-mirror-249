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

    parser = argparse.ArgumentParser()
    parser.add_argument('product',              type=str)
    parser.add_argument('-b', '--blocks',       type=str, default='data/building_block.csv')
    parser.add_argument('-i', '--iterations',   type=int, default=100)
    parser.add_argument('-e', '--exp_topk',     type=int, default=10)
    parser.add_argument('-k', '--route_topk',   type=int, default=10)
    parser.add_argument('-s', '--beam_size',    type=int, default=10)
    parser.add_argument('-m', '--model_type', type=str, default='ensemble', choices=['ensemble','retroformer','g2s','retriever_only'])
    parser.add_argument('-r', '--retrieval',    type=str, default='true', choices=['true', 'false'])
    parser.add_argument('-pr', '--path_retrieval',    type=str, default='true', choices=['true', 'false'])
    parser.add_argument('-d', '--retrieval_db', type=str, default='data/train_canonicalized.txt')
    parser.add_argument('-pd', '--path_retrieval_db', type=str, default='data/pathways.pickle')
    parser.add_argument('-c', '--device',       type=str, default='cuda', choices=['cuda', 'cpu'])
    args = parser.parse_args()

    t_start = time()

    planner = RSPlanner(
        cuda=args.device=='cuda',
        iterations=args.iterations,
        expansion_topk=args.exp_topk,
        route_topk=args.route_topk,
        beam_size=args.beam_size,
        model_type=args.model_type,
        retrieval=args.retrieval=='true',
        retrieval_db=args.retrieval_db,
        path_retrieval=args.path_retrieval=='true',
        path_retrieval_db=args.path_retrieval_db,
        starting_molecules=args.blocks
    )

    if result is None:
        print('None')
    else:
        for i, route in enumerate(result):
            print(f'{i} {route}')

    print(f'\033[92mTotal {time() - t_start:.2f} sec elapsed\033[0m')