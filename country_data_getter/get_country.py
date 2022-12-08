import time
import requests
import json
import numpy as np
import pandas


# BOUNDING BOXES
# https://data.humdata.org/dataset/bounding-boxes-for-countries

# ELEVATIONS
# https://api.open-elevation.com/api/v1/lookup?locations=51.4231,5.4623

# REVERSE GEOLOCATIONS
# https://geocode.maps.co/reverse?lat=51.4231&lon=5.4623

def get_location_data(lat, lon):
    result = {'lat' : lat, 'lon' : lon }
    height_data_get_string = f'https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}'
    # print(height_data_get_string)
    height_data_json = requests.get(height_data_get_string)
    # print(height_data_json.status_code)
    # print(height_data_json.text)
    height_data = json.loads(height_data_json.text)
    elevation = height_data['results'][0]['elevation']
    # print(elevation)
    result['elevation'] = elevation

    get_string_reverse_gecode = f"https://geocode.maps.co/reverse?lat={lat:.5}&lon={lon:.5}"
    # print(get_string_reverse_gecode)
    reverse_location_data_json = requests.get(get_string_reverse_gecode)
    # print(reverse_location_data_json.status_code)
    # print(reverse_location_data_json.text)
    reverse_location_data = json.loads(reverse_location_data_json.text)
    # print(reverse_location_data)
    if 'error' in reverse_location_data :
        result['error'] = 'error in reverse geolocation'
        # print(f"'error in reverse geolocation op lat {lat} lon {lon} ")
    else:
        if 'address' in reverse_location_data:
            if 'state' in reverse_location_data['address'] :
                result['state'] = reverse_location_data['address']['state']
            else:
                result['state'] = 'unknown'
            if 'country' in reverse_location_data['address'] :
                result['country'] = reverse_location_data['address']['country']
            else:
                result['country'] = 'unknown'
            if 'country_code' in reverse_location_data['address'] :
                result['country_code'] = reverse_location_data['address']['country_code']
            else:
                result['country_code'] = 'unknown'
        else:
            result['error'] = 'no address in reverse geolocation'

        
    return result

def get_country_bounds(country):

    # reading the CSV file
    country_bound_df = pandas.read_csv('data/country-boundingboxes.csv')
    
    # displaying the contents of the CSV file
#     print(country_bound_df)


    # bounds = country_bound_df.loc[country_bound_df['country'] == country, ["longmin", "latmin", "longmax" , "latmax"]].values[0]
    bounds = country_bound_df.loc[country_bound_df['country'] == country, ["longmin", "latmin", "longmax" , "latmax"]].to_dict(orient='list')
    # print(f"{bounds}")
    return bounds

 
# ===========================
#  TESTING
# ===========================
if __name__ == '__main__':
    # canada_lat=51.46101274654594;canada_lon=-68.94873314654009
    # get_data(lat=canada_lat, lon=canada_lon)
    # sea_lat = 51.826318646480345; sea_lon= -30.42353091277193
    # get_data(lat=sea_lat, lon=sea_lon)

    bounds = get_country_bounds(country='Netherlands')
#     get_data(lat=51.4231,lon=5.4623)
    for lon in np.linspace(bounds['longmin'][0],bounds['longmax'][0], 10 ):
        # print(f"{lon:.5}")
        # lon = (bounds['longmin'][0] + bounds['longmax'][0]) / 2
        lat = (bounds['latmin'][0] + bounds['latmax'][0]) / 2
        loc_data = get_location_data(lat = lat, lon = lon)
        print(loc_data)
        time.sleep(0.1) # do not flood the web(and get blocked)


