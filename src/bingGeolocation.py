import json, requests

DEBUG = True

def load_subscription_key(path='../.bing_api_key'):
    with open(path, 'r') as f:
        key = f.read().splitlines()[0]
    return key

def get_location_data(latitude,longitude, key='', endpoint_url="http://dev.virtualearth.net/REST/v1/Locations/"):

    params = {
        'o': 'json',
        'key': key
    }
    try:
        response = requests.get("{endpoint}/{latitude},{longitude}".format(endpoint=endpoint_url, latitude=latitude, longitude=longitude),
                                params=params)
        data = json.loads(response.text.encode('ascii', errors='ignore'))

        if DEBUG:
            import pprint
            pp = pprint.PrettyPrinter(indent=4)

        pp.pprint(data)
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
        data = {}

    return data

def degrees_to_decimal(latitude, longitude):
    """
    Assumed to be in the form:
    * x-y-z{N/S}
    * a-b=c{W/E}
    """
    latitude = sum(float(x) / 60 ** n for n, x in enumerate(latitude[:-1].split('-')))  * (1 if 'N' in latitude[-1] else -1)
    longitude = sum(float(x) / 60 ** n for n, x in enumerate(longitude[:-1].split('-'))) * (1 if 'E' in longitude[-1] else -1)

    return latitude, longitude

if __name__ == '__main__':
    key = load_subscription_key()
    latitude = '40-24-34N'
    longitude = '22-58-35E'
    lat,lon = degrees_to_decimal(latitude=latitude, longitude=longitude)
    get_location_data(latitude=lat,
                      longitude=lon,
                      key=key)
