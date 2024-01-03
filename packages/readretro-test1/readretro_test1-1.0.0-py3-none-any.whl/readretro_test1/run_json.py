from retro_star.api import RSPlanner
from time import time
import argparse
import os
import networkx as nx
import json
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('product',              type=str)
parser.add_argument('output',               type=str)
parser.add_argument('-b', '--blocks',       type=str, default='data/building_block.csv')
parser.add_argument('-i', '--iterations',   type=int, default=100)
parser.add_argument('-e', '--exp_topk',     type=int, default=10)
parser.add_argument('-k', '--route_topk',   type=int, default=10)
parser.add_argument('-s', '--beam_size',    type=int, default=10)
parser.add_argument('-m', '--model_type',   type=str, default='ensemble', choices=['ensemble','retroformer','g2s','retriever_only'])
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

result = planner.plan(args.product)


def line_to_graph(line,token):
    rs = line.split('|')
    edges = []
    for r in rs:
        es = r.split('>')
        if token in es[2]:
            edges.extend([es])
        else:
            ps = es[2].split('.')
            edges.extend([(es[0],es[1],p)for p in ps])
    edges = pd.DataFrame(edges,columns=['from','weight','to'])
    g = nx.from_pandas_edgelist(edges, 'from', 'to', ['weight'], create_using = nx.DiGraph())
    return g

def graph_to_dict(graph):
    nodes = [{'id': node} for node in graph.nodes()]
    edges = [{'source': source, 'target': target, 'weight': weight} for source, target, weight in graph.edges(data='weight')]
    
    return {'nodes': nodes, 'edges': edges}

def save_to_json(pathways, output_name, token='keggpath'):
    graphs = [line_to_graph(p,token) for p in pathways]
    graph_dicts = {f'g{i+1}': graph_to_dict(graph) for i, graph in enumerate(graphs)}
    with open(output_name, 'w') as json_file:
        json.dump(graph_dicts, json_file, indent=4)

output_name = args.output

if result is None:
    with open(output_name, 'w') as json_file:
        os.system(f'touch {output_name}')
    print(None)
else:
    save_to_json(result, output_name)
    for i, route in enumerate(result):
        print(f'{i} {route}')

print(f'\033[92mTotal {time() - t_start:.2f} sec elapsed\033[0m')
