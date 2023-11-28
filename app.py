# Must run .\.env\Scripts\activate inside of the Homework-4-APIs
import os
import requests

from pprint import PrettyPrinter
from datetime import datetime, timedelta, date
from dotenv import load_dotenv
from flask import Flask, render_template, request, send_file
# from geopy.geocoders import Nominatim


################################################################################
## SETUP
################################################################################

app = Flask(__name__)

# Get the API key from the '.env' file
load_dotenv()

pp = PrettyPrinter(indent=4)

API_KEY = os.getenv('API_KEY')
API_URL = 'http://api.openweathermap.org/data/2.5/weather'


################################################################################
## ROUTES
################################################################################

@app.route('/')
def home():
    """Displays the homepage with forms for current or historical data."""
    context = {
        'min_date': (datetime.now() - timedelta(days=5)),
        'max_date': datetime.now()
    }
    return render_template('home.html', **context)

# ----------------------------------------------------------------
# Get a letter for units given
def get_letter_for_units(units):
    """Returns a shorthand letter for the given units."""
    return 'F' if units == 'imperial' else 'C' if units == 'metric' else 'K'

# ----------------------------------------------------------------
# Display Current Weather Conditions
@app.route('/results')
def results():
    """Displays results for current weather conditions."""
    # Use 'request.args' to retrieve the city & units from the query
    # parameters.
    city = request.args.get('city')
    units = request.args.get('units')

    params = {
        # Enter query parameters here for the 'appid' (your api key),
        "appid": API_KEY,
        # the city, and the units (metric or imperial).   
        # See the documentation here: https://openweathermap.org/current
        "q": city,
        "units": units
    }

    result_json = requests.get(API_URL, params=params, timeout=20).json()
    # Uncomment the line below to see the results of the API call!
    pp.pprint(result_json)

    # Replace the empty variables below with their appropriate values.
    # You'll need to retrieve these from the result_json object above.

    # For the sunrise & sunset variables, I would recommend to turn them into
    # datetime objects. You can do so using the `datetime.fromtimestamp()`
    # function.
    # print(result_json)
    context = {
        'current_date': datetime.now().strftime("%m/%d/%Y"),
        'units': units,
        'description': result_json["weather"][0]["description"],
        'city': result_json["name"],
        'temp': result_json["main"]["temp"],
        'humidity': result_json["main"]["humidity"],
        'wind_speed': result_json["wind"]["speed"],
        'sunrise': datetime.fromtimestamp(result_json["sys"]["sunrise"]),
        'sunset': datetime.fromtimestamp(result_json["sys"]["sunset"]),
        'units_letter': get_letter_for_units(units)
    }

    return render_template('results.html', **context)

# ----------------------------------------------------------------
# Make a API call
def create_api_call(city, units):
    """ Make a API call and store as a dictionary"""
    params = {
        # Enter query parameters here for the 'appid' (your api key),
        "appid": API_KEY,
        # the city, and the units (metric or imperial).        
        # See the documentation here: https://openweathermap.org/current
        "q": city,
        "units": units
    }

    result = requests.get(API_URL, params=params).json()
    # Results of the API call!
    return result

# ----------------------------------------------------------------
# Display weather for 2 different cities
@app.route('/comparison_results')
def comparison_results():
    """Displays the relative weather for 2 different cities."""
    # Use 'request.args' to retrieve the cities & units from the query parameters.
    city_1 = request.args.get('city1')
    city_2 = request.args.get('city2')
    units = request.args.get('units')

    # Make 2 API calls, one for each city.
    # HINT: You may want to write a helper function for this!
    city_1_api_call = create_api_call(city_1, units)
    city_2_api_call = create_api_call(city_2, units)

    # pp.pprint(city_1_api_call)
    # print("-------------------------")
    # pp.pprint(city_2_api_call)

    # Store today's date
    today = date.today()
    # -----------------------------------
    # Place City 1's info in a separate context or dictionary
    city_1_info = {
        'date': today.strftime("%m/%d/%Y"),
        'units': units,
        'description': city_1_api_call["weather"][0]["description"],
        'name': city_1_api_call["name"],
        'temp': city_1_api_call["main"]["temp"],
        'humidity': city_1_api_call["main"]["humidity"],
        'wind_speed': city_1_api_call["wind"]["speed"],
        'sunrise': datetime.fromtimestamp(city_1_api_call["sys"]["sunrise"]),
        'sunset': datetime.fromtimestamp(city_1_api_call["sys"]["sunset"]),
        'units_letter': get_letter_for_units(units)
    }
    # -----------------------------------
    # Place City 2's info in a separate context or dictionary
    city_2_info = {
        'units': units,
        'description': city_2_api_call["weather"][0]["description"],
        'name': city_2_api_call["name"],
        'temp': city_2_api_call["main"]["temp"],
        'humidity': city_2_api_call["main"]["humidity"],
        'wind_speed': city_2_api_call["wind"]["speed"],
        'sunrise': datetime.fromtimestamp(city_2_api_call["sys"]["sunrise"]),
        'sunset': datetime.fromtimestamp(city_2_api_call["sys"]["sunset"]),
        'units_letter': get_letter_for_units(units)
    }
    context = {"city1": city_1_info,
               "city2": city_2_info
            }
    return render_template('comparison_results.html', **context)

# ---------------------------------------------------------------
if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.run(debug=True)
