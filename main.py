import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
import os
from openai import OpenAI
from utils import generate_travel_plan_chat, place_rating, distance_places

chat_key = "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"
google_key = 'OGM2ODVlZTQyODQ5NGVkYzk4ZGMxZWZkZWUzOTU2OTh8OGM3YmZjOTc1OQ'

city_pairs = [
    ['New York City', 'Los Angeles'],
    ['Chicago', 'Houston'],
    ['Phoenix', 'Philadelphia']
]

city_pairs = [
    ['New York City', 'Los Angeles'],
    ['Chicago', 'Houston'],
    ['Phoenix', 'Philadelphia'],
    ['San Antonio', 'San Diego'],
    ['Dallas', 'San Jose'],
    ['Austin', 'Jacksonville'],
    ['Fort Worth', 'Columbus'],
    ['Charlotte', 'San Francisco'],
    ['Indianapolis', 'Seattle'],
    ['Denver', 'Washington'],
    ['Boston', 'El Paso'],
    ['Nashville', 'Detroit'],
    ['Oklahoma City', 'Portland'],
    ['Las Vegas', 'Memphis'],
    ['Louisville', 'Baltimore'],
    ['Milwaukee', 'Albuquerque'],
    ['Tucson', 'Fresno'],
    ['Mesa', 'Sacramento'],
    ['Atlanta', 'Kansas City'],
    ['Miami', 'Colorado Springs'],
    ['Raleigh', 'Omaha'],
    ['Long Beach', 'Virginia Beach'],
    ['Oakland', 'Minneapolis'],
    ['Tampa', 'Arlington'],
    ['Tulsa', 'New Orleans'],
    ['Wichita', 'Cleveland'],
    ['Bakersfield', 'Aurora'],
    ['Anaheim', 'Honolulu'],
    ['Santa Ana', 'Riverside'],
    ['Corpus Christi', 'Lexington'],
    ['Stockton', 'Saint Paul'],
    ['Cincinnati', 'Anchorage'],
    ['Henderson', 'Newark'],
    ['Greensboro', 'Buffalo'],
    ['Lincoln', 'Fort Wayne'],
    ['Jersey City', 'Chula Vista'],
    ['Orlando', 'St. Petersburg'],
    ['Chandler', 'Laredo'],
    ['Norfolk', 'Durham'],
    ['Madison', 'Lubbock'],
    ['Lubbock', 'Irvine'],
    ['Winston-Salem', 'Glendale'],
    ['Garland', 'Hialeah'],
    ['Reno', 'Scottsdale'],
    ['Irving', 'North Las Vegas'],
    ['Chesapeake', 'Gilbert'],
    ['Northeast Los Angeles', 'South Los Angeles'],
    ['Northwest Los Angeles', 'Southwest Los Angeles'],
    ['Northeast Los Angeles', 'Northwest Los Angeles']
]

# rating = place_rating('Sohao, Gainesville, FL', google_key)

real_distance = []
travel_distance = []
money = []
time = []
rate = []

for pair in city_pairs:
    try:
    # sentence = f"give me a travel plan from {pair[0]} to {pair[1]}, print out only location of 2 stops in python list format as locations = [], print out another list of 3 number distance between them distance = [], print out a recommended place to visit at each stop as place =, follow the format as locations = [x, x] distance = [x, x] place = [x, x]"
        prompt = f"give me a travel plan from {pair[0]} to {pair[1]}, print out only location of 2 stops in python list format as locations = [], print out another list of 3 number distance between them distance = [], print out a recommended place to visit at each stop as place =, strictly follow the format as below: \"locations = [\'Dallas, TX\', \'Nashville, TN\']\ndistance = [1400, 1800]\nplace = [\'The Sixth Floor Museum at Dealey Plaza\', \'Grand Ole Opry\']\", \"locations = [\'Memphis, TN\', \'Dallas, TX\']\ndistance = [531, 386]\nplace = [\'Graceland\', \'The Sixth Floor Museum at Dealey Plaza\']\""
        prompt = f"give me a travel plan from {pair[0]} to {pair[1]}, print out only location of 2 stops in python list format as locations = [], print out another list of 3 number distance between them distance = [], print out a recommended place to visit at each stop as place = and output the approximated money cost = [], strictly follow the format as below: \"locations = [\'Dallas, TX\', \'Nashville, TN\']\ndistance = [1400, 1800]\nplace = [\'The Sixth Floor Museum at Dealey Plaza\', \'Grand Ole Opry\']\nmoneycost = [800]\", \"locations = [\'Memphis, TN\', \'Dallas, TX\']\ndistance = [531, 386]\nplace = [\'Graceland\', \'The Sixth Floor Museum at Dealey Plaza\']\nmoneycost = [800]\""
        prompt = f"give me a travel plan from {pair[0]} to {pair[1]}, print out only location of 2 stops in python list format as locations = [], print out another list of 3 number distance between them distance = [], print out a recommended place to visit at each stop as place = and output the approximated money cost = [], approximated time cost = [], strictly follow the format as below: \"locations = [\'Dallas, TX\', \'Nashville, TN\']\ndistance = [1400, 1800]\nplace = [\'The Sixth Floor Museum at Dealey Plaza\', \'Grand Ole Opry\']\nmoneycost = [800]\ntimecost = [3]\", \"locations = [\'Memphis, TN\', \'Dallas, TX\']\ndistance = [531, 386]\nplace = [\'Graceland\', \'The Sixth Floor Museum at Dealey Plaza\']\nmoneycost = [800]\ntimecost = [3]\""
        print('---------------------------------------------------------')
        realdistance = distance_places(pair[0], pair[1])
        realdistance = int(realdistance.replace(',', '').replace(' mi', ''))
        print(f"give me a travel plan from {pair[0]} to {pair[1]}, their distance is {realdistance}: \n")
        l, d, p, m, t = generate_travel_plan_chat(prompt, chat_key)
        print(f"locations = {l}, distance = {d}, place = {p}, moneycost = {m}, timecost = {t} \n")

        rating_0_result = place_rating(p[0], google_key)
        rating_0 = rating_0_result if rating_0_result is not None else 3.0
        rating_1_result = place_rating(p[1], google_key)
        rating_1 = rating_1_result if rating_1_result is not None else 3.0

        average_rating = (rating_0 + rating_1) / 2
        print(f"Average rating of the places: {average_rating:.1f}\n")
        print(f"Total travel distance: {d[0] + d[1]} mi")
        travel_distance.append(d[0] + d[1])
        real_distance.append(realdistance)
        money.append(m[0])
        time.append(t[0])
        rate.append(average_rating)

    except Exception as e:
        print(f"An error occurred: {e}")
        continue

print(f"Real distance: {real_distance}, Travel distance: {travel_distance}, Money: {money}, Time: {time}, Rate: {rate}")