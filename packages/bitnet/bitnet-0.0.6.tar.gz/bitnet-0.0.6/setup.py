# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bitnet']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'torch', 'zetascale']

setup_kwargs = {
    'name': 'bitnet',
    'version': '0.0.6',
    'description': 'bitnet - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# BitNet\n![bitnet](/bitnet.png)\nImplementation of the "BitNet: Scaling 1-bit Transformers for Large Language Models"\n\n[Paper link:](https://arxiv.org/pdf/2310.11453.pdf)\n\nBitLinear = tensor -> layernorm -> Binarize -> abs max quantization -> dequant\n\n"The implementation of the BitNet architecture is quite simple, requiring only the replacement of linear projections (i.e., nn.Linear in PyTorch) in the Transformer. " -- BitNet is really easy to implement just swap out the linears with the BitLinear modules! \n\n## **NEWS**\n- BitNet Transformer has been trained using the `train.py` file that trains on enwiki8 a small 1gb dataset of wikipedia: [HERE IS THE LINK](https://drive.google.com/file/d/1gBuZRFBqMV3cVD902LXA_hmZl4e0dLyY/view)\n\n## Appreciation\n- Dimitry, Nullonix for analysis and code review and revision\n- Vyom, for providing 4080 to train!\n\n## Installation\n`pip install bitnet`\n\n## Usage:\n- Example of the BitLinear layer which is the main innovation of the paper!\n```python\nimport torch\n\nfrom bitnet import BitLinear\n\n# Input\nx = torch.randn(10, 512)\n\n# BitLinear layer\nlayer = BitLinear(512, 400)\n\n# Output\ny = layer(x)\n\nprint(y)\n\n```\n----\n\n- Running random inputs to a full BitNet Transformer as shown in paper:\n```python\nimport torch\nfrom bitnet import BitNetTransformer\n\nbitnet = BitNetTransformer(\n    num_tokens=20000,\n    dim=512,\n    depth=6,\n    dim_head=64,\n    heads=8,\n    ff_mult=4,\n)\n\ntokens = torch.randint(0, 20000, (1, 512))\nlogits = bitnet(tokens)\nprint(logits.shape)\n\n```\n\n## Inference\n```python\nfrom bitnet import BitNetInference\n\nbitnet = BitNetInference()\nbitnet.load_model(\'../model_checkpoint.pth\') #Download model\noutput_str = bitnet.generate("The dog jumped over the ", 512)\nprint(output_str)\n\n```\n\n# License\nMIT\n\n# Citation\n```bibtex\n@misc{2310.11453,\nAuthor = {Hongyu Wang and Shuming Ma and Li Dong and Shaohan Huang and Huaijie Wang and Lingxiao Ma and Fan Yang and Ruiping Wang and Yi Wu and Furu Wei},\nTitle = {BitNet: Scaling 1-bit Transformers for Large Language Models},\nYear = {2023},\nEprint = {arXiv:2310.11453},\n}\n\n```\n\n\n# Todo\n- [ ] Double check BitLinear implementation and make sure it works exactly as in paper \n- [x] Implement training script for `BitNetTransformer`\n- [x] Train on Enwiki8, copy and past code and data from Lucidrains repos\n- [x] Benchmark performance\n- [x] Look into Straight Through Estimator for non-differentiable backprop\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/bitnet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
