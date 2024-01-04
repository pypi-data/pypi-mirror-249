# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['se_attn']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'torch', 'zetascale']

setup_kwargs = {
    'name': 'selfextend',
    'version': '0.0.1',
    'description': 'SelfExtendAttn - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# SelfExtendAttn\nImplementation of SelfExtendAttn from the paper "LLM Maybe LongLM: Self-Extend LLM Context Window Without Tuning" from Pytorch and Zeta. This implementation is based mostly on the pseudocode listed in Algorithm 1 in page 4\n\n\n# Install\n`pip install selfextend`\n\n\n## Usage\n```python\nimport torch\nfrom se_attn import SelfExtendAttn\n\n# Example usage\ndim = 512  # Dimension of model\ng_size = 2  # Group size\nw_size = 4  # Window size for neighbor tokens\nself_extend = SelfExtendAttn(dim, g_size, w_size, qk_norm=True)\n\n# Example tensors for q, k, v, and pos\nq = torch.randn(1, 10, dim)\nk = torch.randn(1, 10, dim)\nv = torch.randn(1, 10, dim)\npos = torch.arange(0, 10).unsqueeze(0)  # Example positional indices\n\noutput = self_extend(q, k, v, pos)\nprint(output)\n```\n\n---\n\n## Technical Architecture\n\n### Key Concepts\n\n- **Grouped Attention**: This mechanism divides the input sequence into groups and applies the attention operation within each group. It uses a floor operation to adjust the positions within the groups, enabling efficient handling of longer sequences.\n  \n- **Normal Attention**: Standard self-attention used in transformers, focusing on nearby tokens within a specified window.\n\n### Attention Mechanism\n\nThe `SelfExtendAttn` module integrates these two attention strategies:\n\n1. **Normal Attention** is applied to tokens within a neighborhood window, maintaining precise positional information for closely related tokens.\n   \n2. **Grouped Attention** is used for tokens outside this neighborhood window. It reduces the granularity of positional information for distant tokens, which is less critical but still contributes to the overall context understanding.\n\n### Merge Strategy\n\nThe attention values outside the neighborhood window are replaced by those obtained from the grouped attention. This merging strategy ensures a smooth transition and efficient processing of longer sequences while preserving the essential context captured by the normal attention within the neighborhood window.\n\n### Positional Encoding\n\nSine and cosine functions generate positional encodings, ensuring that the model retains an understanding of token order and position.\n\n## Implementation Details\n\n- **Module Class**: `SelfExtendAttn` is implemented as a subclass of `nn.Module` in PyTorch.\n- **Configurability**: Key parameters such as group size and neighbor window size are configurable.\n- **Causal Masking**: Ensures that the attention mechanism respects the autoregressive property of language models.\n\n\n\n# Citation\n```bibtext\n@misc{jin2024llm,\n    title={LLM Maybe LongLM: Self-Extend LLM Context Window Without Tuning}, \n    author={Hongye Jin and Xiaotian Han and Jingfeng Yang and Zhimeng Jiang and Zirui Liu and Chia-Yuan Chang and Huiyuan Chen and Xia Hu},\n    year={2024},\n    eprint={2401.01325},\n    archivePrefix={arXiv},\n    primaryClass={cs.CL}\n}\n```\n\n# License\nMIT',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/SelfExtend',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
