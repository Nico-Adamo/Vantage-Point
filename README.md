# Vantage Point
## Using deep learning to reccomend balanced news sources and combat fake news

Vantage Point uses state-of-the-art language modelling in order to aggregate news and recommend a balanced and fair selection of sources on any given topic.
Powered by BERT and OpenAI's GPT-2. 

![Template Chrome Extension](https://github.com/Nico-Adamo/Vantage-Point/blob/master/resources/webTemplate.png?raw=true)

## Current Features:
- News Aggregation
- Source Bias Database, pulled from large-scale academic studies and updated/curated by hand. 
- Database of article embeddings used to group articles by event or topic.
- Article reccomendation using optimization algorithms to minimize bias but maximize variety of viewpoints.  
- Server-side API to query for article similarity, bias, recommendations, etc.

## Not-quite-done Features:
- Front-end chrome extension displaying recommended articles
- Landing page

## Planned Features
- Supervised news article summarization using GPT-3
- Dashboard showing news viewing habits and personal bias
