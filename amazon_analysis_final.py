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

"""#Data Exploration and Preprocessing"""
data.columns = ['UserID', 'ProductID', 'Rating', 'UnixTime'] # adds headers to columns
data['UserID'] = data['UserID'].astype(str) # converts column to string
data['ProductID'] = data['ProductID'].astype(str)
data['RatingTimestamp'] = pd.to_datetime(data['UnixTime'], unit='s', utc=True) # Converts Unix timestamps to datetime objects
data['RatingTimestamp'] = data['RatingTimestamp'].dt.tz_convert('America/New_York') # Adjusts datetime objects to America/New_York time zone
data['RatingTimestamp'] = data['RatingTimestamp'].dt.strftime('%Y-%m-%d %H:%M:%S') # Converts datetime objects to strings in preferred format
data = data.drop(columns=['UnixTime'])
print(data)

#Outputting the number of unique users and products
numUniqueUsers = len(pd.unique(data['UserID']))
print(numUniqueUsers)
numUniqueProducts = len(pd.unique(data['ProductID']))
print(numUniqueProducts)

# Explore data: rating column only
data.describe()

# Explore data: rating time stamp
print("Earliest Date:", data['RatingTimestamp'].min())
print("Latest Date:", data['RatingTimestamp'].max())

##Choose random sample, n = 500,000
unique_user_ids = data['UserID'].unique()
# Sample a subset of unique user IDs
sampled_user_ids = pd.Series(unique_user_ids).sample(n=500000, replace=False, random_state=42)
# Use the sampled user IDs to make a subset of your original DataFrame
data = data[data['UserID'].isin(sampled_user_ids)]
print("Sampled DataFrame:")
print(data)


##Create bipartite graph
bipartite_graph = nx.Graph()
userIDs = data['UserID'].tolist()
productIDs = data['ProductID'].tolist()
ratings = data['Rating'].tolist()
ratingTimestamps = data['RatingTimestamp'].tolist()

# add both sets of nodes with specific attribute to distinguish them
bipartite_graph.add_nodes_from(userIDs, bipartite=0) # give set of users the bipartite attribute with value = 0
bipartite_graph.add_nodes_from(productIDs, bipartite=1) # give set of products the bipartite attribute with value = 1

weighted_edges = []
for i in range(len(userIDs)):
  weighted_edges.append((userIDs[i], productIDs[i], (ratings[i], ratingTimestamps[i])))

# Add weighted edges to the graph
bipartite_graph.add_weighted_edges_from(weighted_edges, weight='weight') # weight=weight just means keep the attribute name weight

# get the first 5 edges with weights
edges_with_weights = list(bipartite_graph.edges(data=True))[:5]

# Print the first 5 edges with weights
print("First 5 edges of the graph with weights:")
for edge in edges_with_weights:
    print(edge[:2], "Weight:", edge[2]['weight']


user_nodes = [node for node, attr in bipartite_graph.nodes(data=True) if attr['bipartite'] == 0]
num_user_nodes = len(user_nodes)

product_nodes = [node for node, attr in bipartite_graph.nodes(data=True) if attr['bipartite'] == 1]
num_product_nodes = len(product_nodes)

num_edges = bipartite_graph.number_of_edges()

print("Number of nodes with bipartite=0 (users):", num_user_nodes) 
print("Number of nodes with bipartite=1 (products):", num_product_nodes)
print("Total number of nodes:", bipartite_graph.number_of_nodes())
print("Number of edges:", num_edges)




          
