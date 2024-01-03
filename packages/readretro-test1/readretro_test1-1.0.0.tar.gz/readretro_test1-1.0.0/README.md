# READRetro: Natural Product Biosynthesis Planning with Retrieval-Augmented Dual-View Retrosynthesis
This is the official code repository for the paper *READRetro: Natural Product Biosynthesis Planning with Retrieval-Augmented Dual-View Retrosynthesis (bioRxiv, 2023)*.<br>
We also provide [a web version](https://readretro.net) for ease of use.

## Installation
Run the following commands to install the dependencies:
```bash
conda create -n readretro python=3.8
conda activate readretro
conda install pytorch==1.12.0 cudatoolkit=11.3 -c pytorch
pip install easydict pandas tqdm numpy==1.22 OpenNMT-py==2.3.0 networkx==2.5    # need to fix the miner version of numpy (np.bool was deprecated)
conda install -c conda-forge rdkit=2019.09
```

## Model Preparation
We provide the trained models in [Google Drive](https://drive.google.com/drive/folders/1lt3r6leSn9mI5OeAIfBmh6iBtwa_EYWV?usp=sharing).<br>
Place the checkpoints under the folders `g2s/saved_models` and `retroformer/saved_models`.<br>
You can use your own models trained using the official codes (https://github.com/coleygroup/Graph2SMILES and https://github.com/yuewan2/Retroformer).

## Single-step Planning and Evaluation
Run the following command to evaluate the single-step performance of the models:
```bash
CUDA_VISIBLE_DEVICES=${gpu_id} python eval_single.py                    # ensemble
CUDA_VISIBLE_DEVICES=${gpu_id} python eval_single.py -m retroformer     # Retroformer
CUDA_VISIBLE_DEVICES=${gpu_id} python eval_single.py -m g2s -s 200      # Graph2SMILES
```

## Multi-step Planning
Run the following command to plan paths of multiple products using multiprocessing:
```bash
CUDA_VISIBLE_DEVICES=${gpu_id} python run_mp.py
# e.g., CUDA_VISIBLE_DEVICES=0 python run_mp.py
```
You can modify other hyperparameters described in `run_mp.py`.<br>
Lower `num_threads` if you run out of GPU capacity.

Run the following command to plan the retrosynthesis path of your own molecule:
```bash
CUDA_VISIBLE_DEVICES=${gpu_id} python run.py ${product}
# e.g., CUDA_VISIBLE_DEVICES=0 python run.py 'O=C1C=C2C=CC(O)CC2O1'
```
You can modify other hyperparameters described in `run.py`.

## Multi-step Evaluation
Run the following command to evaluate the planned paths of the test molecules:
```bash
python eval.py ${save_file}
# e.g., python eval.py result/debug.txt
```
