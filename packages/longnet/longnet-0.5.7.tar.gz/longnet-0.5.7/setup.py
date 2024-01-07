# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['long_net']

package_data = \
{'': ['*']}

install_requires = \
['accelerate',
 'beartype',
 'bitsandbytes',
 'dataclasses',
 'einops',
 'torch',
 'torchscale',
 'transformers',
 'zetascale']

setup_kwargs = {
    'name': 'longnet',
    'version': '0.5.7',
    'description': 'LongNet - Pytorch',
    'long_description': "[![Multi-Modality](images/agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n\n# LongNet: Scaling Transformers to 1,000,000,000 Tokens\n![LongNetBanner](images/longnet.jpg)\n\n\n[![GitHub issues](https://img.shields.io/github/issues/kyegomez/LongNet)](https://github.com/kyegomez/LongNet/issues) \n[![GitHub forks](https://img.shields.io/github/forks/kyegomez/LongNet)](https://github.com/kyegomez/LongNet/network) \n[![GitHub stars](https://img.shields.io/github/stars/kyegomez/LongNet)](https://github.com/kyegomez/LongNet/stargazers) [![GitHub license](https://img.shields.io/github/license/kyegomez/LongNet)](https://github.com/kyegomez/LongNet/blob/master/LICENSE)\n[![Share on Twitter](https://img.shields.io/twitter/url/https/twitter.com/cloudposse.svg?style=social&label=Share%20%40kyegomez/LongNet)](https://twitter.com/intent/tweet?text=Excited%20to%20introduce%20LongNet,%20the%20all-new%20LongSequence%20model%20with%20the%20potential%20to%20revolutionize%20automation.%20Join%20us%20on%20this%20journey%20towards%20a%20smarter%20future.%20%23LongNet%20%23LongSequence&url=https%3A%2F%2Fgithub.com%2Fkyegomez%2FLongNet)\n[![Share on Facebook](https://img.shields.io/badge/Share-%20facebook-blue)](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fgithub.com%2Fkyegomez%2FLongNet)\n[![Share on LinkedIn](https://img.shields.io/badge/Share-%20linkedin-blue)](https://www.linkedin.com/shareArticle?mini=true&url=https%3A%2F%2Fgithub.com%2Fkyegomez%2FLongNet&title=Introducing%20LongNet%2C%20the%20All-New%20LongSequence%20Model&summary=LongNet%20is%20the%20next-generation%20LongSequence%20model%20that%20promises%20to%20transform%20industries%20with%20its%20intelligence%20and%20efficiency.%20Join%20us%20to%20be%20a%20part%20of%20this%20revolutionary%20journey%20%23LongNet%20%23LongSequence&source=)\n![Discord](https://img.shields.io/discord/999382051935506503)\n[![Share on Reddit](https://img.shields.io/badge/-Share%20on%20Reddit-orange)](https://www.reddit.com/submit?url=https%3A%2F%2Fgithub.com%2Fkyegomez%2FLongNet&title=Exciting%20Times%20Ahead%20with%20LongNet%2C%20the%20All-New%20LongSequence%20Model%20%23LongNet%20%23LongSequence) [![Share on Hacker News](https://img.shields.io/badge/-Share%20on%20Hacker%20News-orange)](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fgithub.com%2Fkyegomez%2FLongNet&t=Exciting%20Times%20Ahead%20with%20LongNet%2C%20the%20All-New%20LongSequence%20Model%20%23LongNet%20%23LongSequence)\n[![Share on Pinterest](https://img.shields.io/badge/-Share%20on%20Pinterest-red)](https://pinterest.com/pin/create/button/?url=https%3A%2F%2Fgithub.com%2Fkyegomez%2FLongNet&media=https%3A%2F%2Fexample.com%2Fimage.jpg&description=LongNet%2C%20the%20Revolutionary%20LongSequence%20Model%20that%20will%20Change%20the%20Way%20We%20Work%20%23LongNet%20%23LongSequence)\n[![Share on WhatsApp](https://img.shields.io/badge/-Share%20on%20WhatsApp-green)](https://api.whatsapp.com/send?text=I%20just%20discovered%20LongNet,%20the%20all-new%20LongSequence%20model%20that%20promises%20to%20revolutionize%20automation.%20Join%20me%20on%20this%20exciting%20journey%20towards%20a%20smarter%20future.%20%23LongNet%20%23LongSequence%0A%0Ahttps%3A%2F%2Fgithub.com%2Fkyegomez%2FLongNet)\n\n\n\nThis is an open source implementation for the paper [LongNet: Scaling Transformers to 1,000,000,000 Tokens](https://arxiv.org/abs/2307.02486) by Jiayu Ding, Shuming Ma, Li Dong, Xingxing Zhang, Shaohan Huang, Wenhui Wang, Furu Wei. The LongNet is a Transformer variant designed to scale sequence length up to more than 1 billion tokens without sacrificing performance on shorter sequences.\n\n\n## Installation\n\n```shell\npip install longnet\n```\n\n## Usage\n\nOnce you have installed LongNet, you can use the `DilatedAttention` class as follows:\n\n```python\nimport torch\nfrom long_net import DilatedAttention\n\n\n# model config\ndim = 512\nheads = 8\ndilation_rate = 2\nsegment_size = 64\n\n# input data\nbatch_size = 32\nseq_len = 8192\n\n\n# create model and data\nmodel = DilatedAttention(dim, heads, dilation_rate, segment_size, qk_norm=True)\nx = torch.randn((batch_size, seq_len, dim))\n\noutput = model(x)\nprint(output)\n\n\n```\n\n### `LongNetTransformer`\nA fully ready to train transformer model with dilated transformer blocks with Feedforwards with layernorm, SWIGLU, and a parallel transformer block\n\n```python\nimport torch\nfrom long_net.model import LongNetTransformer\n\nlongnet = LongNetTransformer(\n    num_tokens=20000,\n    dim=512,\n    depth=6,\n    dim_head=64,\n    heads=8,\n    ff_mult=4,\n)\n\ntokens = torch.randint(0, 20000, (1, 512))\nlogits = longnet(tokens)\nprint(logits)\n\n\n```\n\n# Train\n- To run a simple training run on the enwiki8 dataset, gitclone, install the requirements.txt, and then run `python3 train.py`\n\n## LongNet Summarized\n\nScaling sequence length has become a critical bottleneck in the era of large language models. However, existing methods struggle with either computational complexity or model expressivity, rendering the maximum sequence length restricted. In this paper, they introduce LongNet, a Transformer variant that can scale sequence length to more than 1 billion tokens, without sacrificing the performance on shorter sequences. Specifically, they propose dilated attention, which expands the attentive field exponentially as the distance grows.\n\n## Features\nLongNet has significant advantages:\n1. It has a linear computation complexity and a logarithm dependency between tokens.\n2. It can be served as a distributed trainer for extremely long sequences.\n3. Its dilated attention is a drop-in replacement for standard attention, which can be seamlessly integrated with the existing Transformer-based optimization.\n\nExperiment results demonstrate that LongNet yields strong performance on both long-sequence modeling and general language tasks. Their work opens up new possibilities for modeling very long sequences, e.g., treating a whole corpus or even the entire Internet as a sequence.\n\n\n## Citation\n```bibtex\n@inproceedings{ding2023longnet,\n  title={LongNet: Scaling Transformers to 1,000,000,000 Tokens},\n  author={Ding, Jiayu and Ma, Shuming and Dong, Li and Zhang, Xingxing and Huang, Shaohan and Wang, Wenhui and Wei, Furu},\n  booktitle={Proceedings of the 10th International Conference on Learning Representations},\n  year={2023}\n}\n```\n\n-----\n\n# Todo\n\n- [ ] Fix the ParallelTransformer Block's forward pass with dilated attn\n- [ ] Train on enwiki 8 and test\n- [ ] Create multihead iteration\n",
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/LongNet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
