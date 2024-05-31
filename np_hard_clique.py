# -*- coding: utf-8 -*-
"""NP hard clique.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ibI6HDtNXcKScuaDdN5UFMh0li0d4YKa
"""

pip install dwave-ocean-sdk

import dimod
import numpy as np

# Defining the graph
graph = {
    0: [1, 2],
    1: [0, 2],
    2: [0, 1, 3],
    3: [2]
}

# Creating a binary quadratic model
bqm = dimod.BinaryQuadraticModel(vartype='SPIN')

# Adding positive terms to encourage spins to align for connected vertices
for i in graph:
    for j in graph[i]:
        if i < j:
            bqm.add_quadratic(i, j, -1)

# Adding negative terms to discourage spins from aligning for unconnected vertices
for i in graph:
    for j in set(graph.keys()) - set([i]) - set(graph[i]):
        bqm.add_quadratic(i, j, 2)

# Setting up the sampler
sampler = dimod.SimulatedAnnealingSampler()

# Sample from the BQM
sampleset = sampler.sample(bqm, num_reads=100)

# Finding the sample with the lowest energy
lowest_energy = min(sampleset.data(['energy']), key=lambda x: x[1] if len(x) > 1 else float('inf'))

# Decoding the solution
clique = set()
for sample, energy in sampleset.data(['sample', 'energy']):
    if energy == lowest_energy:
        for node, value in sample.items():
            if value == 1:
                clique.add(node)
        break

# Printing the maximum clique
print(clique)