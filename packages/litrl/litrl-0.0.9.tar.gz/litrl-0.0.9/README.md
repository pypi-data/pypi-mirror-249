# Lightning RL

Implementation of Reinforcement Learning algorithms using Lighting, torchrl and mlflow.

This code was largely influenced by the implementations in [CleanRL](https://github.com/vwxyzjn/cleanrl/tree/master) and [Lizhi](https://github.com/Lizhi-sjtu/DRL-code-pytorch), as well as partially [lightning_bolts].

The SAC implementation was also influenced by [Haarnooja SAC](https://github.com/haarnoja/sac), the Online Decision Transformer implementation was influenced by [ODT](https://github.com/facebookresearch/online-dt), Xzero from [werner muzero]

## Get Started

Torchrl is still a bit immature and may be difficult to install. pip install litrl will, by default, not attempt to install it unless you pass the [all] option. Alternatives are to download directly from source:

```bash
pip install 'tensordict @ git+https://github.com/pytorch/tensordict.git@c3caa7612275306ce72697a82d5252681ddae0ab'
pip install 'torchrl @ git+https://github.com/pytorch/rl.git@1bb192e0f3ad9e7b8c6fa769bfa3bb9d82ca4f29'
```

Download all the dependencies

```bash
pip install litrl[all]
```

## Developing

:exclamation: Some of the dependencies don't support python 3.12 yet

Ensure you're using python3.11:

```bash
python -V
```

If not, create a new environment:

```bash
conda create -n python3.11.6 python=3.11.6
conda activate python3.11.6
```

Create a .env file and edit information (optional, needed for Huggingface integration)

```bash
cp .env.example .env
```

```bash
# build a new python virtual environment
make .venv
source .venv/bin/activate
bash scripts/train/sac_connect4.sh
```

## TODO

citizen commit bump

list of validation opponents (MCTS50, MCTS500, MCTS5000)

Clean up Huggingface
    huggingface "no model to upload" problem
    add informations to README.md etc.

code coverage

val run n times instead of rolling window

## Future features

Implement Rainbow
Implement ODT
AlphaGoOffline
AlphaZero
MuZero
