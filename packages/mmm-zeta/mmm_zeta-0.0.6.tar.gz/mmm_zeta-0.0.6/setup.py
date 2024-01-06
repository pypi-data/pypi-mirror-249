# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mm_mamba']

package_data = \
{'': ['*']}

install_requires = \
['swarms', 'torch==2.1.2', 'zetascale==1.4.0']

setup_kwargs = {
    'name': 'mmm-zeta',
    'version': '0.0.6',
    'description': 'MMM - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Multi Modal Mamba - [MMM]\nA novel implementation of fusing ViT with Mamba into a fast, agile, and high performance Multi-Modal Model. Powered by Zeta, the simplest AI framework ever.\n\n\n## Install\n`pip3 install mmm-zeta`\n\n\n## Usage\n```python\n# Import the necessary libraries\nimport torch \nfrom torch import nn\nfrom mm_mamba import MultiModalMambaBlock\n\n# Create some random input tensors\nx = torch.randn(1, 16, 64)  # Tensor with shape (batch_size, sequence_length, feature_dim)\ny = torch.randn(1, 3, 64, 64)  # Tensor with shape (batch_size, num_channels, image_height, image_width)\n\n# Create an instance of the MultiModalMambaBlock model\nmodel = MultiModalMambaBlock(\n    dim = 64,  # Dimension of the token embeddings\n    depth = 5,  # Number of transformer layers\n    dropout = 0.1,  # Dropout probability\n    heads = 4,  # Number of attention heads\n    d_state = 16,  # Dimension of the state embeddings\n    image_size = 64,  # Size of the input image\n    patch_size = 16,  # Size of each image patch\n    encoder_dim = 64,  # Dimension of the encoder token embeddings\n    encoder_depth = 5,  # Number of encoder transformer layers\n    encoder_heads = 4  # Number of encoder attention heads\n)\n\n# Pass the input tensors through the model\nout = model(x, y)\n\n# Print the shape of the output tensor\nprint(out.shape)\n\n```\n\n# License\nMIT\n\n\n\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/MultiModalMamba',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
