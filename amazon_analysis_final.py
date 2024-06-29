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
