# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mobilevlm']

package_data = \
{'': ['*']}

install_requires = \
['swarms', 'torch', 'zetascale']

setup_kwargs = {
    'name': 'mobilevlm',
    'version': '0.0.1',
    'description': 'MobileVLM - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# MobileVLM\nImplementation of the LDP module block in PyTorch and Zeta from the paper: "MobileVLM: A Fast, Strong and Open Vision Language Assistant for Mobile Devices"\n\n\n# Install\n`pip3 install mobilevlm`\n\n\n## Usage\n```python\n# Import the necessary libraries\nimport torch\nfrom mobilevlm import LDP\n\n# Create an instance of the LDP model\nldp = LDP(in_channels=128, out_channels=128, depth=3)\n\n# Create an example input tensor\ninput_tensor = torch.randn(1, 128, 64, 64)\n\n# Pass the input tensor through the LDP model to get the output\noutput = ldp(input_tensor)\n\n# Print the shape of the output tensor\nprint(output.shape)\n\n```\n\n\n## Lightweight Downsample Projection (LDP) Layer\n\nThe Lightweight Downsample Projection (LDP) Layer is a component designed for efficient feature extraction and dimensionality reduction in convolutional neural networks. The LDP layer is particularly suited for mobile and edge devices where computational resources are limited. \n\nThe LDP layer combines depthwise separable convolutions with pointwise convolutions and skip connections, allowing for a reduced number of parameters while maintaining a rich feature representation. The incorporation of Layer Normalization stabilizes the training process and allows for faster convergence.\n\n### Architecture\n\nThe LDP layer is structured as follows:\n\n1. **Initial Pointwise Convolution**: This is a 1x1 convolution that transforms the input feature map to the desired number of channels. It is computationally efficient and serves as a channel-wise feature transformation.\n\n2. **GELU Activation**: After the initial pointwise convolution, we apply a Gaussian Error Linear Unit (GELU) activation function. GELU provides non-linearity to the model, allowing it to learn more complex patterns.\n\n3. **First Depthwise Convolution**: A depthwise convolution with a stride of 1 follows, which applies a single filter per input channel. It is used for spatial feature extraction without altering the dimensionality of the feature map.\n\n4. **First Skip Connection**: The output of the first depthwise convolution is added back to the output of the initial pointwise convolution. This skip connection allows gradients to flow directly through the network, mitigating the vanishing gradient problem and enabling deeper architectures.\n\n5. **Second Pointwise Convolution**: Another 1x1 convolution is applied to further mix the channel-wise features.\n\n6. **Layer Normalization**: Normalization is applied over the channel dimension to stabilize the mean and variance of activations, leading to improved training dynamics.\n\n7. **Second GELU Activation**: A second GELU activation function is applied for additional non-linearity.\n\n8. **Second Depthwise Convolution**: This depthwise convolution has a stride of 2, halving the spatial dimensions of the feature map and effectively downsampling the input.\n\n9. **Second Skip Connection**: A pixel-wise addition combines the downsampled input to the block with the output of the second depthwise convolution. This connection helps to preserve information lost due to downsampling.\n\n10. **Third Pointwise Convolution**: A final 1x1 convolution adjusts the channel dimensions if necessary and refines the features before passing them to subsequent layers.\n\n11. **Layer Normalization**: Another layer normalization is applied to the output of the final pointwise convolution.\n\n## Why It Works\n\nThe LDP layer is designed to capture the essence of the input features while reducing the spatial resolution in a computationally efficient manner. The use of depthwise separable convolutions significantly decreases the number of parameters compared to standard convolutions, reducing both the computational cost and the risk of overfitting.\n\nSkip connections not only help to preserve information throughout the layer but also improve gradient flow during backpropagation, allowing for deeper network architectures. Layer Normalization is known to accelerate training and make the model less sensitive to initialization and learning rate choices.\n\nThis combination of efficiency and robustness makes the LDP layer a versatile component in designing neural networks for resource-constrained environments.\n\n\n\n# Citation\n```bibtex\n@misc{chu2023mobilevlm,\n    title={MobileVLM : A Fast, Reproducible and Strong Vision Language Assistant for Mobile Devices}, \n    author={Xiangxiang Chu and Limeng Qiao and Xinyang Lin and Shuang Xu and Yang Yang and Yiming Hu and Fei Wei and Xinyu Zhang and Bo Zhang and Xiaolin Wei and Chunhua Shen},\n    year={2023},\n    eprint={2312.16886},\n    archivePrefix={arXiv},\n    primaryClass={cs.CV}\n}\n```\n\n\n# License\nMIT\n\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/MobileVLM',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
