# import sys
# import json
#
#
#
# import pandas as pd
# import re
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import numpy as np
#
# movies = pd.read_csv("movies.csv")
#
#
# def clean_title(title):
#     title = re.sub("[^a-zA-Z0-9 ]", "", title)
#     return title
#
#
# movies["clean_title"] = movies["title"].apply(clean_title)
#
# vectorizer = TfidfVectorizer(ngram_range=(1, 2))
#
# tfidf = vectorizer.fit_transform(movies["clean_title"])
#
#
# def search(title):
#     title = clean_title(title)
#     query_vec = vectorizer.transform([title])
#     similarity = cosine_similarity(query_vec, tfidf).flatten()
#     indices = np.argpartition(similarity, -5)[-5:]
#     results = movies.iloc[indices].iloc[::-1]
#
#     return results.to_json(orient="records")
#
#
# movie_id = 89745
#
# # def find_similar_movies(movie_id):
# movie = movies[movies["movieId"] == movie_id]
#
# ratings = pd.read_csv("ratings.csv")
# ratings.dtypes
# similar_users = ratings[(ratings["movieId"] == movie_id) & (ratings["rating"] > 4)]["userId"].unique()
# similar_user_recs = ratings[(ratings["userId"].isin(similar_users)) & (ratings["rating"] > 4)]["movieId"]
# similar_user_recs = similar_user_recs.value_counts() / len(similar_users)
#
# similar_user_recs = similar_user_recs[similar_user_recs > .10]
# all_users = ratings[(ratings["movieId"].isin(similar_user_recs.index)) & (ratings["rating"] > 4)]
# all_user_recs = all_users["movieId"].value_counts() / len(all_users["userId"].unique())
# rec_percentages = pd.concat([similar_user_recs, all_user_recs], axis=1)
# rec_percentages.columns = ["similar", "all"]
#
# rec_percentages["score"] = rec_percentages["similar"] / rec_percentages["all"]
# rec_percentages = rec_percentages.sort_values("score", ascending=False)
# rec_percentages.head(10).merge(movies, left_index=True, right_on="movieId")
#
#
# def find_similar_movies(movie_id):
#     similar_users = ratings[(ratings["movieId"] == movie_id) & (ratings["rating"] > 4)]["userId"].unique()
#     similar_user_recs = ratings[(ratings["userId"].isin(similar_users)) & (ratings["rating"] > 4)]["movieId"]
#     similar_user_recs = similar_user_recs.value_counts() / len(similar_users)
#
#     similar_user_recs = similar_user_recs[similar_user_recs > .10]
#     all_users = ratings[(ratings["movieId"].isin(similar_user_recs.index)) & (ratings["rating"] > 4)]
#     all_user_recs = all_users["movieId"].value_counts() / len(all_users["userId"].unique())
#     rec_percentages = pd.concat([similar_user_recs, all_user_recs], axis=1)
#     rec_percentages.columns = ["similar", "all"]
#
#     rec_percentages["score"] = rec_percentages["similar"] / rec_percentages["all"]
#     rec_percentages = rec_percentages.sort_values("score", ascending=False)
#     return rec_percentages.head(10).merge(movies, left_index=True, right_on="movieId")[["score", "title", "genres"]]
#
#
# # print(search("Iron Man 2008"))
#
#
import socket
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json

# Load movies data
movies = pd.read_csv("movies.csv")


# Function to clean movie titles
def clean_title(title):
    title = re.sub("[^a-zA-Z0-9 ]", "", title)
    return title


# Add a column with cleaned titles
movies["clean_title"] = movies["title"].apply(clean_title)

# Create TF-IDF vectorizer
vectorizer = TfidfVectorizer(ngram_range=(1, 2))
tfidf = vectorizer.fit_transform(movies["clean_title"])


# Function to search for movies based on title
def search(title):
    title = clean_title(title)
    query_vec = vectorizer.transform([title])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argpartition(similarity, -5)[-5:]
    results = movies.iloc[indices].iloc[::-1]
    return results


# Function to find similar movies based on user ratings
def find_similar_movies(movie_id):
    print()
    # Your existing logic for finding similar movies
    # ...


# Take user input for movie title
# user_input = input("Enter a movie title: ")

# Display search results
# results = search(user_input)
# print(results.to_json(orient="records", lines=True))
HOST = '127.0.0.1'  # Use your server's IP address or 'localhost'
PORT = 3002  # Use the same port number as in your Node.js code

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()

print(f'Server is listening on {HOST}:{PORT}')

while True:
    # Accept a connection from a client
    client_socket, client_address = server_socket.accept()
    print(f'Connection established with {client_address}')

    # Receive data from the client
    data = client_socket.recv(1024).decode('utf-8')

    if not data:
        break

    # Process the data (you can replace this with your actual logic)
    processed_data = {'response': f'Received data: {data}'}
    results = search(data)
    # Send the processed data back to the client
    response = results.to_json(orient="records", lines=True)
    print(response)
    client_socket.send(response.encode('utf-8'))

    # Close the connection with the client
    client_socket.close()

# Close the server socket
server_socket.close()
