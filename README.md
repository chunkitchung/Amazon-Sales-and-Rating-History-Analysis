# Amazon Sales and Rating History Analysis

## Overview
This repository contains the code and data analysis for the final project of EECS4414: Information Networks at York University. The project applies network analysis techniques to Amazon's sales and rating history data to provide personalized customer recommendations and uncover key business insights. The full report can be found [here](https://drive.google.com/file/d/1B8pQfQgy-GqyWi3CFT-NvEFyJejuZ27a/view?usp=sharing) The dataset we used can be found [here](https://www.kaggle.com/code/saurav9786/recommender-system-using-amazon-reviews/notebook)

## Team Members
- Aiza Bajwa - ambajwa@my.yorku.ca
- Chun-Kit Chung - chunkit@my.yorku.ca
- Krupali Patel - kp20@my.yorku.ca
- Harib Shahbaz - harib327@my.yorku.ca

## Project Description
With the rise of online shopping, understanding customer behavior through sales and rating history has become crucial. This project utilizes network and graph theory to analyze Amazon's historical transactions and review data, aiming to solve several key business problems:

1. Identify the most essential users to tailor recommendations and marketing strategies.
2. Identify important products to improve inventory management.
3. Segment users based on similar purchasing and rating patterns.
4. Perform temporal analysis to identify influential trends over time.
5. Forecast future customer purchasing trends.
6. Recommend products to customers to enhance their shopping experience.

## Methodology
1. **Dataset and Sampling**: Used a random sample of 500,000 users from Amazon's sales data spanning from 1999 to 2014.
2. **Data Preprocessing and Network Creation**: Constructed a bipartite graph representing users and products, with edges denoting ratings.
3. **Node Centrality and Community Detection**: Applied degree centrality, Bayesian average rating, and the Louvain method to identify key users, products, and user communities.
4. **Link Prediction and Collaborative Filtering**: Used the Pearson Correlation Coefficient and the Weighted Jaccard Coefficient for link prediction and collaborative filtering for recommendations.

## Tools and Technologies
- **Python**: Core programming language used for data analysis and network creation.
- **NetworkX**: Library for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks.
- **Bayesian Methods**: Applied for calculating product importance.
- **Pearson Correlation Coefficient**: Used to measure user similarity.
- **Louvain Method**: Implemented for community detection.

## Results
The analysis provided several insights, including:
- Identification of key customers and products.
- Temporal trends in product ratings and sales.
- Segmentation of users into communities based on their purchasing behavior.
- Accurate prediction of future purchasing trends and personalized product recommendations.
