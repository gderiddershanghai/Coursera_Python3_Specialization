import requests_with_caching
import json

def get_movies_from_tastedive(movie_title):
    baseurl = "https://tastedive.com/api/similar"
    d = {"q": movie_title, "type": "movies", "limit": 5}
    requests_with_caching.get(baseurl, params=d)
    page = requests_with_caching.get(baseurl, params=d)
    words_dic = page.json()
    return words_dic

def extract_movie_titles(dict):
    movie_list = [i["Name"] for i in dict["Similar"]["Results"]]
    return movie_list

def get_related_titles(lst):
    recommendations = []
    for movie in lst:
        #result = get_movies_from_tastedive(movie)
        item = extract_movie_titles(get_movies_from_tastedive(movie))
        if movie not in recommendations:
            recommendations.append(item)
    rec2 = []
    for mlist in recommendations:
        for movie in mlist:
            if movie not in rec2:
                rec2.append(movie)
    return rec2

import requests_with_caching
import json

def get_movie_data(movie_title):
    baseurl = "http://www.omdbapi.com/"
    d = {"t": movie_title, "r": "json"}
    requests_with_caching.get(baseurl, params=d)
    page = requests_with_caching.get(baseurl, params=d)
    movie_dic = page.json()
    return movie_dic

def get_movie_rating(dct):
    if len(dct["Ratings"]) < 3: #There are three ratings in the list that includes Rotten Tomatoes
        return 0
    else:
        result = dct["Ratings"][1]["Value"] #Rotten Tomatoes is the second value [1]
        return int(result[:-1])

def get_sorted_recommendations(movie_title_list):
    ratings_dictionary = {}
    movie_list = get_related_titles(movie_title_list)
    for movie_title in movie_list:
        ratings_dictionary[movie_title] = get_movie_rating(get_movie_data(movie_title))
    # return list of movies sorted by score, or sorted alphabetically if there's a tie in score
    return sorted(ratings_dictionary, key=lambda w: (ratings_dictionary[w], w), reverse=True)
