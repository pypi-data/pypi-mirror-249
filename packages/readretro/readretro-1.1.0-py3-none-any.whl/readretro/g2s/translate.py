import os
import sys
root = os.path.abspath('.')
if root not in sys.path:
    sys.path.insert(0, root)

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from time import time
import torch
import numpy as np
from g2s.models.graph2seq_series_rel import Graph2SeqSeriesRel
from g2s.utils.data_utils import load_vocab
from g2s.utils.preprocess import build_batch

from rdkit import RDLogger, Chem
RDLogger.DisableLog("rdApp.*")


def filter_invalid(generations, scores):
    filtered_generations, filtered_scores = [], []
    for generation, score in zip(generations, scores):
        mol = Chem.MolFromSmiles(generation)
        if mol is None:
            continue
        filtered_generations.append(Chem.MolToSmiles(mol))
        filtered_scores.append(score)
    
    return filtered_generations, filtered_scores


def filter_single_atom(generations):
    filtered_generations = []
    for generation in generations:
        filtered_generations.append('.'.join([smi for smi in generation.split('.') if len(smi) > 1]))
    
    return filtered_generations


def translate(model, batch, args, vocab_tokens):
    with torch.no_grad():
        results = model.predict_step(
            reaction_batch=batch,
            batch_size=batch.size,
            beam_size=args.beam_size,
            n_best=args.expansion_topk,
            temperature=1,
            min_length=1,
            max_length=512
        )

        for predictions in results["predictions"]:
            smis = []
            for prediction in predictions:
                predicted_idx = prediction.detach().cpu().numpy()
                predicted_tokens = [vocab_tokens[idx] for idx in predicted_idx[:-1]]
                smi = "".join(predicted_tokens)
                smis.append(smi)
    
    generations, scores = smis, [s.cpu() for s in results['scores'][0]]

    generations, scores = filter_invalid(generations, scores)
    generations = filter_single_atom(generations)
    generations, scores = generations[:args.expansion_topk], scores[:args.expansion_topk]

    if len(scores) > 0:
        scores = list(np.exp(np.array(scores)) / np.sum(np.exp(np.array(scores))))   # softmax

    return {'reactants': generations, 'scores': scores}


def prepare_g2s(cuda=True, beam_size=200, expansion_topk=10, ckpt='.'):
    device = torch.device("cuda") if cuda else torch.device("cpu")
    # print(f'g2s device: {device}')
    # state = torch.load('g2s/saved_models/clean.pt')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # state = torch.load(os.path.join(script_dir,'saved_models/biochem.pt'))
    state = torch.load(ckpt,map_location=torch.device('cpu'))
    args = state["args"]
    args.beam_size = beam_size
    args.expansion_topk = expansion_topk
    args.vocab_file = os.path.join(script_dir,'saved_models/vocab_smiles.txt')

    vocab = load_vocab(args.vocab_file)
    vocab_tokens = [k for k, v in sorted(vocab.items(), key=lambda tup: tup[1])]

    model = Graph2SeqSeriesRel(args, vocab)
    model.load_state_dict(state["state_dict"])
    model.to(device)
    model.eval()

    return model, args, vocab, vocab_tokens, device


def run_g2s(model, args, smi, vocab, vocab_tokens, device):
    # print(f'rung2s')
    batch = build_batch(smi, vocab)
    batch.to(device)
    result = translate(model, batch, args, vocab_tokens)
    result['templates'] = [None for _ in range(len(result['scores']))]
    result['retrieved'] = [False for _ in range(len(result['scores']))]
    return result


if __name__ == "__main__":
    t_start = time()
    model, args, vocab, vocab_tokens, device = prepare_g2s()
    # smi = 'N[C@@H](CNC(=O)C(=O)O)C(=O)O'
    smi = 'C=CC(C)(C)[C@@]12C[C@H]3c4nc5ccccc5c(=O)n4[C@H](C)C(=O)N3C1N(C(C)=O)c1ccccc12'
    print(run_g2s(model, args, smi, vocab, vocab_tokens, device))
    print(f'\033[92mTotal {time() - t_start:.2f} sec elapsed\033[0m')
