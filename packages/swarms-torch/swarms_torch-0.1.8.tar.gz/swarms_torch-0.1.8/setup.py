# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['swarms_torch', 'swarms_torch.swarmalators']

package_data = \
{'': ['*']}

install_requires = \
['einops==0.7.0', 'pytest==7.4.2', 'torch==2.1.2', 'zetascale==1.4.4']

setup_kwargs = {
    'name': 'swarms-torch',
    'version': '0.1.8',
    'description': 'swarms-torch - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Swarms in Torch\nSwarms in Torch is an experimental repository designed to cater to your swarming algorithm needs. With a range of useful algorithms including Particle Swarm Optimization (PSO), Ant Colony, Sakana, and more, all implemented using PyTorch primitives, you can easily leverage the power of swarming techniques in your projects.\n\n\n## Installation\n\nYou can install the package using pip\n\n```bash\npip3 install swarms-torch\n```\n\n# Usage\n\n### ParticleSwarmOptimization\n\n```python\nfrom swarms_torch import ParticleSwarmOptimization\n\n\npso = ParticleSwarmOptimization(goal="Attention is all you need", n_particles=100)\n\npso.optimize(iterations=1000)\n```\n\n### Ant Colony Optimization\n```python\nfrom swarms_torch.ant_colony_swarm import AntColonyOptimization\n\n# Usage:\ngoal_string = "Hello ACO"\naco = AntColonyOptimization(goal_string, num_iterations=1000)\nbest_solution = aco.optimize()\nprint("Best Matched String:", best_solution)\n\n```\n\n### Neural Network with Transformers as synapases\n```python\nimport torch\nfrom swarms_torch.nnt import NNTransformer\n\nx = torch.randn(1, 10)\n\nnetwork = NNTransformer(\n    neuron_count = 5, \n    num_states = 10,\n    input_dim = 10,\n    output_dim = 10,\n    nhead = 2,\n)\noutput = network(x)\nprint(output)\n```\n\n### CellularSwarm\na Cellular Neural Net with transformers as cells, time simulation, and a local neighboorhood!\n\n```python\nfrom swarms_torch import CellularSwarm \n\nx = torch.randn(10, 32, 512)  # sequence length of 10, batch size of 32, embedding size of 512\nmodel = CellularSwarm(cell_count=5, input_dim=512, nhead=8)\noutput = model(x)\n\n```\n### Fish School/Sakana\n- An all-new innovative approaches to machine learning that leverage the power of the Transformer model architecture. These systems are designed to mimic the behavior of a school of fish, where each fish represents an individual Transformer model. The goal is to optimize the performance of the entire school by learning from the best-performing fish.\n\n```python\nimport torch\nfrom swarms_torch.fish_school import Fish, FishSchool\n\n# Create random source and target sequences\nsrc = torch.randn(10, 32, 512)\ntgt = torch.randn(10, 32, 512)\n\n# Create random labels\nlabels = torch.randint(0, 512, (10, 32))\n\n# Create a fish and train it on the random data\nfish = Fish(512, 8, 6)\nfish.train(src, tgt, labels)\nprint(fish.food)  # Print the fish\'s food\n\n# Create a fish school and optimize it on the random data\nschool = FishSchool(10, 512, 8, 6, 100)\nschool.forward(src, tgt, labels)\nprint(school.fish[0].food)  # Print the first fish\'s food\n\n```\n\n### Swarmalators\n```python\nfrom swarms_torch import visualize_swarmalators, simulate_swarmalators\n\n# Init for Swarmalator\n# Example usage:\nN = 100\nJ, alpha, beta, gamma, epsilon_a, epsilon_r, R = [0.1] * 7\nD = 3  # Ensure D is an integer\nxi, sigma_i = simulate_swarmalators(\n    N, J, alpha, beta, gamma, epsilon_a, epsilon_r, R, D\n)\n\n\n# Call the visualization function\nvisualize_swarmalators(xi)\n```\n\n### Mixture of Mambas\n- An 100% novel implementation of a swarm of MixtureOfMambas.\n- Various fusion methods through averages, weighted_aggegrate, and more to come like a gating mechanism or other various methods.\n- fusion methods: average, weighted, absmax, weighted_softmax, or your own custom function\n\n```python\nimport torch\nfrom swarms_torch import MixtureOfMambas\n\n# Create a 3D tensor for text\nx = torch.rand(1, 512, 512)\n\n# Create an instance of the MixtureOfMambas model\nmodel = MixtureOfMambas(\n    num_mambas=2,            # Number of Mambas in the model\n    dim=512,                 # Dimension of the input tensor\n    d_state=1024,            # Dimension of the hidden state\n    depth=4,                 # Number of layers in the model\n    d_conv=1024,             # Dimension of the convolutional layers\n    expand=4,                # Expansion factor for the model\n    fusion_method="absmax",  # Fusion method for combining Mambas\' outputs\n    custom_fusion_func=None  # Custom fusion function (if any)\n)\n\n# Pass the input tensor through the model and print the output shape\nprint(model(x).shape)\n\n```\n\n# Documentation\n- [Click here for documentation](https://swarmstorch.readthedocs.io/en/latest/swarms/)\n\n# Playground\n- There are various scripts in the playground folder with various examples for each swarm, like ant colony and fish school and spiral optimization.\n\n# Todo\n- [Check out the project board](https://github.com/users/kyegomez/projects/9/views/1)\n- Make training scripts for each model on enwiki 8\n- Create hivemind model for robotics, 1 model that takes in X inputs from N robots and distributes tasks to individual or many robots\n- Swarm of liquid nets for text sequence modeling or vision\n- Swarm of Convnets for facial recognition?\n- Swarm of transformers where each transformer is an expert and they all share the same weights so they can see each others knowledge, but inference is local.\n\n# License\nMIT\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/swarms-pytorch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
