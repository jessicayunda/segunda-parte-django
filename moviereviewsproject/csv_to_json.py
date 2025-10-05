import pandas as pd 
import json

df = pd.read_csv('peliculas.csv', sep=";")
df.to_json('movies.json', orient = 'records')


with open('movies.json','r') as file:
    movies = json.load(file)

for i in range(100):
    movie = movies[i]
    print(movie)
    break