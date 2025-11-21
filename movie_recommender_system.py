import pandas as pd
import numpy as np
import ast
movies=pd.read_csv(r'C:\Users\abhay\OneDrive\Desktop\archive (1)\tmdb_5000_movies.csv')
credits=pd.read_csv(r'C:\Users\abhay\OneDrive\Desktop\archive (1)\tmdb_5000_credits.csv')
# print(credits.head(1)['cast'].values)                                                
movies=movies.merge(credits,on='title')
# movies.info()
# genre id keywords original_language titlen overview  popularity cast crew
movies=movies[['id','title','overview','genres','keywords','cast','crew']]
# movies.info()

movies.dropna(inplace=True)
# print(movies.isnull().sum())
# print(movies.duplicated().sum())
# print(movies.iloc[0].genres)
def convert(obj):
    L=[]
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L
movies['genres']=movies['genres'].apply(convert)
# movies.head()
movies['keywords']=movies['keywords'].apply(convert)
def convert3(obj):
    L=[]
    counter=0
    for i in ast.literal_eval(obj):
        if counter!=3:
            L.append(i['name'])
            counter+=1
        else:
            break
    return L
movies['cast']=movies['cast'].apply(convert3)               
def fetch_director(obj):
    L=[]
    for i in ast.literal_eval(obj):
        if i['job']=='Director':
            L.append(i['name'])
            break
    return L
movies['crew']=movies['crew'].apply(fetch_director) 
movies['overview'] = movies['overview'].apply(lambda x: x.split())

movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x])

movies['tags']=movies['overview']+movies['genres']+movies['keywords']+movies['cast']+movies['crew']
# print(movies.head())
new_df=movies[['id','title','tags']]
# print(new_df)
new_df.loc[:,'tags']=new_df['tags'].apply(lambda x:" ".join(x))
# print(new_df.head())
# print(new_df['tags'][0])
new_df.loc[:,'tags'] = new_df['tags'].apply(lambda x: x.lower())             
# print(new_df.head())
         
from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(max_features=5000, stop_words='english')
vectors=cv.fit_transform(new_df['tags']).toarray()
cv.get_feature_names_out()
#now apply stemming
import nltk
            
from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()
def stem(text):
    y=[]
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)
new_df.loc[:, 'tags'] = new_df['tags'].apply(stem)

from sklearn.metrics.pairwise import cosine_similarity
similarity=cosine_similarity(vectors)
# sorted(list(enumerate(similarity[0])),reverse=True, key=lambda x:x[1][1:6])
def recommend(movie):
    # case-insensitive match
    matches = new_df[new_df['title'].str.lower() == movie.lower()]

    if matches.empty:
        print("Movie not found in the database.")
        return
    
    movie_index = matches.index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)),reverse=True,key=lambda x: x[1])[1:6]

    for i in movie_list:
        print(new_df.iloc[i[0]].title)


Movie_name = input("Enter the Movie name:: ")
recommend(Movie_name)

import pickle
pickle.dump(new_df,open('movies.pkl','wb'))
pickle.dump(new_df.to_dict(),open('movies_dict.pkl','wb'))
pickle.dump(similarity, open('similarity.pkl','wb'))