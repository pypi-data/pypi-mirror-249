from retro_star.api import RSPlanner
from time import time
import argparse

def run_retro_planner(product, blocks='data/building_block.csv', iterations=100, exp_topk=10, route_topk=10,
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
        retrieval_db=retrieval_db,
        path_retrieval=path_retrieval == 'true',
        path_retrieval_db=path_retrieval_db,
        starting_molecules=blocks
    )

    result = planner.plan(product)

    if result is None:
        print('None')
    else:
        for i, route in enumerate(result):
            print(f'{i} {route}')

    print(f'\033[92mTotal {time() - t_start:.2f} sec elapsed\033[0m')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('product', type=str)
    parser.add_argument('-b', '--blocks', type=str, default='data/building_block.csv')
    parser.add_argument('-i', '--iterations', type=int, default=100)
    parser.add_argument('-e', '--exp_topk', type=int, default=10)
    parser.add_argument('-k', '--route_topk', type=int, default=10)
    parser.add_argument('-s', '--beam_size', type=int, default=10)
    parser.add_argument('-m', '--model_type', type=str, default='ensemble',
                        choices=['ensemble', 'retroformer', 'g2s', 'retriever_only'])
    parser.add_argument('-r', '--retrieval', type=str, default='true', choices=['true', 'false'])
    parser.add_argument('-pr', '--path_retrieval', type=str, default='true', choices=['true', 'false'])
    parser.add_argument('-d', '--retrieval_db', type=str, default='data/train_canonicalized.txt')
    parser.add_argument('-pd', '--path_retrieval_db', type=str, default='data/pathways.pickle')
    parser.add_argument('-c', '--device', type=str, default='cuda', choices=['cuda', 'cpu'])
    args = parser.parse_args()

    run_retro_planner(args.product, args.blocks, args.iterations, args.exp_topk, args.route_topk,
                      args.beam_size, args.model_type, args.retrieval, args.path_retrieval,
                      args.retrieval_db, args.path_retrieval_db, args.device)