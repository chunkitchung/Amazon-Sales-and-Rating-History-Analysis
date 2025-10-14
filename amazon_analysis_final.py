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

# confirms our bipartite graph is created correctly (numbers match to dataframe data)
user_nodes = [node for node, attr in bipartite_graph.nodes(data=True) if attr['bipartite'] == 0]
num_user_nodes = len(user_nodes)

product_nodes = [node for node, attr in bipartite_graph.nodes(data=True) if attr['bipartite'] == 1]
num_product_nodes = len(product_nodes)

num_edges = bipartite_graph.number_of_edges()

print("Number of nodes with bipartite=0 (users):", num_user_nodes) # should be number of unique userIDs we sampled: 500,000
print("Number of nodes with bipartite=1 (products):", num_product_nodes)
print("Total number of nodes:", bipartite_graph.number_of_nodes())
print("Number of edges:", num_edges)

## Create degree distribution plots
# Separate users and products
users = {node for node, data in bipartite_graph.nodes(data=True) if data['bipartite'] == 0}
products = set(bipartite_graph) - users

user_degrees = []
for n, degree in bipartite_graph.degree(users):
  user_degrees.append(degree)

product_degrees = []
for n, degree in bipartite_graph.degree(products):
  product_degrees.append(degree)

# Count the occurrences of each degree
user_degree_counts = Counter(user_degrees)
product_degree_counts = Counter(product_degrees)

# Calculate the total number of users and products
total_users = len(users)
total_products = len(products)

# Calculate the probability of each degree for users and products
user_degree_probabilities = {}
for degree, count in user_degree_counts.items():
  user_degree_probabilities[degree] = count / total_users

product_degree_probabilities = {}
for degree, count in product_degree_counts.items():
  product_degree_probabilities[degree] = count / total_products
          
# Create pandas DataFrame with degree and count
user_degree_df = pd.DataFrame(user_degree_counts.items(), columns=['Degree', 'Count']).sort_values(by='Degree')
product_degree_df = pd.DataFrame(product_degree_counts.items(), columns=['Degree', 'Count']).sort_values(by='Degree')

# Print user degree distribution table
print("User Degree Distribution:")
print(user_degree_df.head)

user_degree_probability_df = pd.DataFrame(user_degree_probabilities.items(), columns=['Degree', 'Probability']).sort_values(by='Degree')

# Make figure
plt.figure(figsize=(10, 5))
plt.scatter(user_degree_probability_df['Degree'], user_degree_probability_df['Probability'])

plt.title('User Degree Distribution')
plt.xscale('log')
plt.xlabel('Degree, k')
plt.ylabel('Probability of Degree Distribution, P(k)')
plt.show()


# Print product degree distribution table
print("\nProduct Degree Distribution:")
print(product_degree_df)

# Plot
plt.figure(figsize=(10, 5))
plt.scatter(product_degree_df['Degree'], product_degree_df['Count'])
plt.title('Product Degree Distribution')
plt.xscale('log')
plt.xlabel('Degree, k')
plt.ylabel('Count')
plt.show()

## Filter out unnecessary nodes
# Delete user nodes with degree less than 3
users = {node for node, data in bipartite_graph.nodes(data=True) if data['bipartite'] == 0}

nodes_to_remove = []

for node in users:
  if (bipartite_graph.degree(node) < 3):
    nodes_to_remove.append(node)

bipartite_graph.remove_nodes_from(nodes_to_remove) # altering original graph

print("Number of USER Nodes with degree < 3 removed: ", len(nodes_to_remove))

# Deleting user nodes above have resulted in some product nodes with degree = 0
# Delete product nodes with degree equal to 0, signifying no one reviewed them

products = {node for node, data in bipartite_graph.nodes(data=True) if data['bipartite'] == 1}

nodes_to_remove = []

for node in products:
  if (bipartite_graph.degree(node) == 0):
    nodes_to_remove.append(node)

bipartite_graph.remove_nodes_from(nodes_to_remove)

print("Number of USER Nodes with degree = 0 removed: ", len(nodes_to_remove))

##Create folded graph
#Define Pearson similarity function for user projection/folded graph
def pearson(g, u, v):
  u_ratings = []
  v_ratings = []

  commonProducts = set(g[u]) & set(g[v])

  if not commonProducts:
    return 0
  for product in commonProducts:
    uRating = g[u][product]['weight'][0]
    vRating = g[v][product]['weight'][0]
    u_ratings.append(uRating)
    v_ratings.append(vRating)

  x = np.array(u_ratings)
  y = np.array(v_ratings)
  n = len(x)

  sum_xy = np.sum(x * y)
  sum_x = np.sum(x)
  sum_y = np.sum(y)
  sum_x2 = np.sum(x ** 2)
  sum_y2 = np.sum(y ** 2)

  numerator = n * sum_xy - sum_x * sum_y
  denominator = np.sqrt((n * sum_x2 - sum_x ** 2) * (n * sum_y2 - sum_y ** 2))
  
  # Handle the case where the denominator is zero
  if denominator == 0:
      return 0
    return numerator / denominator
