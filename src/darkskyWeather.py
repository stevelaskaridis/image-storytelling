import json, requests

DEBUG = True

def load_subscription_key(path='../.darksky_api_key'):
    with open(path, 'r') as f:
        key = f.read().splitlines()[0]
    return key

def get_weather_data(latitude, longitude, timestamp, key,
                     endpoint_url='https://api.darksky.net/forecast'):
    params = {
        'units': 'si',
        'exclude': ['currently','flags']
    }

    try:
        response = requests.get("{endpoint}/{key}/{latitude},{longitude},{timestamp}".format(endpoint=endpoint_url,
                                                                      key=key,
                                                                      latitude=latitude,
                                                                      longitude=longitude,
                                                                      timestamp=timestamp),
                                params=params)
        print(response.text)
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

def date_to_timestamp(date_time):
    """
    :param date_time: Date and time to covert. It is expected in the form 'Y:m:d H:M:S'.
    :return: the UNIX epoch timestamp
    """
    import time, datetime
    # ts_to_convert = '/'.join(date) + " " + ':'.join(time)

    return int(time.mktime(datetime.datetime.strptime(date_time, "%Y:%m:%d %H:%M:%S").timetuple()))

if __name__ == '__main__':
    key = load_subscription_key()
    ts = date_to_timestamp('2017:12:29 13:34:18')
    get_weather_data(latitude=51.5033273,longitude=-0.1217317,
                     timestamp=ts, key=key)
