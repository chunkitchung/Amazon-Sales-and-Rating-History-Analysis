import pandas as pd
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

#file path of dataset
file_path = 'ratings_Electronics.csv'

#reading csv file
data = pd.read_csv(file_path, header=None)

print(data)
