# Mistral JAX

## Usage

Simple installation from PyPI.

```sh
pip install mistral-jax
```

Import MistralLMParams and MistralModelParams.

```python
from mistral import MistralLMParams, MistralModelParams
```

## Roadmap

- [x] Model architecture
- [x] Publish a Python library
- [ ] Model parallelism
- [ ] Generation
    - [ ] KV cache
    - [ ] Sampling
- [ ] Training

## Install

This project requires Python 3.11, JAX 0.4.20.

Create venv:

```sh
python3.11 -m venv venv
```

Install dependencies:

CPU:

```sh
pip install -U pip
pip install -U wheel
pip install "jax[cpu]"
pip install --pre torch --index-url https://download.pytorch.org/whl/nightly/cpu
pip install git+https://github.com/huggingface/transformers
pip install -r requirements.txt
```

CUDA 11:

```sh
pip install -U pip
pip install -U wheel
pip install "jax[cuda11_pip]" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
pip install --pre torch --index-url https://download.pytorch.org/whl/nightly/cu118
pip install git+https://github.com/huggingface/transformers
pip install -r requirements.txt
```

TPU VM:

```sh
pip install -U pip
pip install -U wheel
pip install "jax[tpu]" -f https://storage.googleapis.com/jax-releases/libtpu_releases.html
pip install --pre torch --index-url https://download.pytorch.org/whl/nightly/cpu
pip install git+https://github.com/huggingface/transformers
pip install -r requirements.txt
```

## Model architecture

```
MistralForCausalLM(
  (model): MistralModel(
    (embed_tokens): Embedding(32000, 4096)
    (layers): ModuleList(
      (0-31): 32 x MistralDecoderLayer(
            (self_attn): MistralAttention(
                    (q_proj): Linear(in_features=4096, out_features=4096, bias=False)
                    (k_proj): Linear(in_features=4096, out_features=1024, bias=False)
                    (v_proj): Linear(in_features=4096, out_features=1024, bias=False)
                    (o_proj): Linear(in_features=4096, out_features=4096, bias=False)
                    (rotary_emb): MistralRotaryEmbedding()
            )
            (mlp): MistralMLP(
                    (gate_proj): Linear(in_features=4096, out_features=14336, bias=False)
                    (up_proj): Linear(in_features=4096, out_features=14336, bias=False)
                    (down_proj): Linear(in_features=14336, out_features=4096, bias=False)
                    (act_fn): SiLUActivation()
            )
            (input_layernorm): MistralRMSNorm()
            (post_attention_layernorm): MistralRMSNorm()
      )
    )
    (norm): MistralRMSNorm()
  )
  (lm_head): Linear(in_features=4096, out_features=32000, bias=False)
)
```
