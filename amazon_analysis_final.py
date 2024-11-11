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
