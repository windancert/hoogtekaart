import time
import requests
import json
import numpy as np
import pandas
from country_bounding_boxes import (
      country_subunits_containing_point,
      country_subunits_by_iso_code
    )
import pycountry

# BOUNDING BOXES
# https://data.humdata.org/dataset/bounding-boxes-for-countries

# ELEVATIONS
# https://api.open-elevation.com/api/v1/lookup?locations=51.4231,5.4623

# REVERSE GEOLOCATIONS
# https://geocode.maps.co/reverse?lat=51.4231&lon=5.4623

def get_location_data(lat, lon):
    result = {'lat' : lat, 'lon' : lon }
    height_data_get_string = f'https://api.open-elevation.com/api/v1/lookup?locations={lat:.5},{lon:.5}'
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

    # # reading the CSV file
    country_bound_df = pandas.read_csv('data/country-boundingboxes.csv')
    bounds = country_bound_df.loc[country_bound_df['country'] == country, ["longmin", "latmin", "longmax" , "latmax"]].to_dict(orient='list')
    return bounds

def get_country_bounds_2(country_name):
    # https://github.com/graydon/country-bounding-boxes
    country_code = pycountry.countries.get(name=country_name).alpha_2
    print(f"country code {country_code}")
    bounds = [c.bbox for c in country_subunits_by_iso_code(country_code)][0]
    print(f" bounds {bounds}")
    bounds = {'longmin':bounds[0], 'latmin':bounds[1],'longmax':bounds[2], 'latmax':bounds[3]}
    return bounds
 
def get_country_to_file( country_name, lat_res, lon_res):
    # canada_lat=51.46101274654594;canada_lon=-68.94873314654009
    # get_data(lat=canada_lat, lon=canada_lon)
    # sea_lat = 51.826318646480345; sea_lon= -30.42353091277193
    # get_data(lat=sea_lat, lon=sea_lon)
    
    bounds = get_country_bounds_2(country_name=country_name)
    print(f" {country_name} bounds {bounds} ")
    
#     get_data(lat=51.4231,lon=5.4623)
    country_data = []
    for lat in np.linspace(bounds['latmin'],bounds['latmax'], lat_res ):
        for lon in np.linspace(bounds['longmin'],bounds['longmax'], lon_res ):
            # print(f"{lon:.5}")
            # lon = (bounds['longmin'][0] + bounds['longmax'][0]) / 2
            # lat = (bounds['latmin'][0] + bounds['latmax'][0]) / 2
            loc_data = get_location_data(lat = lat, lon = lon)
            country_data.append(loc_data)
            print(loc_data)
            time.sleep(0.1) # do not flood the web(and get blocked)
    country_data_json = json.dumps(country_data)
    with open(f"country_data_{country_name}.json", "w") as outfile:
        outfile.write(country_data_json)

def load_country_from_file(country_name):
    with open(f"country_data_{country_name}.json", "r") as outfile:
        country_data_json = outfile.read()
    country_data = json.loads(country_data_json)
    return country_data

# ===========================
#  TESTING
# ===========================
if __name__ == '__main__':
    country = 'Netherlands'
    get_country_to_file(country_name=country, lat_res=50, lon_res=50)

    data = load_country_from_file(country)
    import matplotlib.cm as cm
    import matplotlib.pyplot as plt
    lat = []
    lon = []
    el = []
    for d in data:
        if d['country_code']=='nl':
            lat.append(d['lat'])
            lon.append(d['lon'])
            el.append(d['elevation'])
    y = np.array(lat)
    x = np.array(lon)
    z = np.array(el)
    
    f, ax = plt.subplots(1,2, sharex=True, sharey=True)
    ax[0].tripcolor(x,y,z)
    ax[1].tricontourf(x,y,z, 20) # choose 20 contour levels, just to show how good its interpolation is
    ax[1].plot(x,y, 'ko ')
    ax[0].plot(x,y, 'ko ')
    plt.show()