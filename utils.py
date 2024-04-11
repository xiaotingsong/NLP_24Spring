import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
import os
from openai import OpenAI
from google_maps_reviews import ReviewsClient
import requests


def generate_travel_plan_gemini(sentence, my_key):
    genai.configure(api_key=my_key)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(sentence)
    result = response.candidates[0].content.parts[0].text

    local_vars = {}
    exec(result, {}, local_vars)

    locations = local_vars.get('locations', [])
    distance = local_vars.get('distance', [])
    place = local_vars.get('place', [])
    moneycost = local_vars.get('moneycost', [])
    timecost = local_vars.get('timecost', [])

    # 返回这些变量
    return locations, distance, place, moneycost, timecost



    # client = OpenAI(api_key=my_key)
    # chat_completion = client.chat.completions.create(
    #     messages=[
    #         {"role": "user", "content": sentence}
    #     ],
    #     model="gpt-3.5-turbo",
    # )
    # mstr = chat_completion.choices[0].message.content
    #
    # local_vars = {}
    # exec(mstr, {}, local_vars)
    #
    # locations = local_vars.get('locations', [])
    # distance = local_vars.get('distance', [])
    # place = local_vars.get('place', [])
    # moneycost = local_vars.get('moneycost', [])
    # timecost = local_vars.get('timecost', [])
    #
    # # 返回这些变量
    # return locations, distance, place, moneycost, timecost


def generate_travel_plan_chat(sentence, my_key):
    client = OpenAI(api_key=my_key)
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": sentence}
        ],
        model="gpt-3.5-turbo",
    )
    mstr = chat_completion.choices[0].message.content

    local_vars = {}
    exec(mstr, {}, local_vars)

    locations = local_vars.get('locations', [])
    distance = local_vars.get('distance', [])
    place = local_vars.get('place', [])
    moneycost = local_vars.get('moneycost', [])
    timecost = local_vars.get('timecost', [])

    # 返回这些变量
    return locations, distance, place, moneycost, timecost

def place_rating(place, my_google_key):

    client = ReviewsClient(api_key=my_google_key)
    results = client.get_reviews(place, reviewsLimit=1, language='en')
    rating = results[0]['rating']

    return rating

def distance_places(place1, place2):
    response = requests.get(
        'https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}&key=AIzaSyAL8SaRkbpMGpfOVU9ClQ5Sfbn2CLsAUS4'.format(
            place1, place2)).json()
    dist = response['routes'][0]['legs'][0]['distance']

    return dist['text']