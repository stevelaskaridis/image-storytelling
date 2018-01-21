import json, requests

DEBUG = True

def load_subscription_key(path='../.foursquare_api_key'):
    with open(path, 'r') as f:
        key, secret = f.read().splitlines()[0:2]
    return key, secret

def get_location_data(latitude,longitude, client_id, client_secret, radius=100,
                      endpoint_url="https://api.foursquare.com/v2/venues/search/"):
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'v': 20170801,
        'll': '{},{}'.format(latitude, longitude),
        # 'query': '',
        # 'intent': 'global',
        'limit': 2,
        'radius': radius,
    }
    try:
        response = requests.get("{endpoint}".format(endpoint=endpoint_url),
                                params=params)
        data = response.json()
        # data = json.loads(response.text.encode('ascii', errors='ignore'))

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
    client_id,client_secret = load_subscription_key()
    get_location_data(51.5033273,-0.1217317, client_id,client_secret)
