import requests, base64
DEBUG = True

def load_subscription_key(path='../.azure_vision_api_key'):
    with open(path, 'r') as f:
        key = f.read().splitlines()[0]
    return key

def describe_image(url, key, visual_features, detail, endpoint_url='https://westcentralus.api.cognitive.microsoft.com/'):
    """
    :param visual_features: List of visual features for the Vision API to report in response (Categories,Description,Color)
    :param detail: None, Landmark or Celebrity
    """
    if url.split(':')[0].startswith('http'):
        describe_image_by_url(url, key, visual_features, detail, endpoint_url)
    else:
        describe_local_image(url, key, visual_features, detail, endpoint_url)

def describe_image_by_url(image_url, key, visual_features, detail, endpoint_url='https://westcentralus.api.cognitive.microsoft.com/'):
    headers = {
        # Request headers.
        'Content-Type': 'application/json',

        # NOTE: Replace the "Ocp-Apim-Subscription-Key" value with a valid subscription key.
        'Ocp-Apim-Subscription-Key': key,
    }

    visual_features = ','.join(visual_features)
    if detail is None:
        detail = ''

    params = {
        # Request parameters. All of them are optional.
        'visualFeatures': visual_features,
        'detail': detail,
        'language': 'en',
    }

    # Replace the three dots below with the URL of a JPEG image of a celebrity.
    body = {
        'url': '{}'.format(image_url)
    }
    print('body',body)

    try:
        # NOTE: You must use the same location in your REST call as you used to obtain your subscription keys.
        #   For example, if you obtained your subscription keys from westus, replace "westcentralus" in the
        #   URL below with "westus"
        response = requests.post(url = endpoint_url + '/vision/v1.0/analyze',
                                 headers = headers,
                                 params = params,
                                 json = body)
        data = response.json()
        if DEBUG:
            import pprint
            pp = pprint.PrettyPrinter(indent=4)

        pp.pprint(data)
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def describe_local_image(image_path, key, visual_features, detail, endpoint_url='https://westcentralus.api.cognitive.microsoft.com/'):
    headers = {
        # Request headers.
        'Content-Type': 'application/octet-stream',

        # NOTE: Replace the "Ocp-Apim-Subscription-Key" value with a valid subscription key.
        'Ocp-Apim-Subscription-Key': key,
    }

    visual_features = ','.join(visual_features)
    if detail is None:
        detail = ''

    params = {
        # Request parameters. All of them are optional.
        'visualFeatures': visual_features,
        'detail': detail,
        'language': 'en',
    }

    # Replace the three dots below with the URL of a JPEG image of a celebrity.
    image = open(image_path, 'rb').read()

    try:
        # NOTE: You must use the same location in your REST call as you used to obtain your subscription keys.
        #   For example, if you obtained your subscription keys from westus, replace "westcentralus" in the
        #   URL below with "westus"
        response = requests.post(url = endpoint_url + '/vision/v1.0/analyze',
                                 headers = headers,
                                 params = params,
                                 data = image)
        data = response.json()
        if DEBUG:
            import pprint
            pp = pprint.PrettyPrinter(indent=4)

        pp.pprint(data)
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

if __name__ == '__main__':
    key = load_subscription_key()
    describe_image(url='http://cdn-image.travelandleisure.com/sites/default/files/styles/1600x1000/public/1487701021/eiffel-tower-paris-france-EIFFEL0217.jpg',
                   key=key,
                   visual_features=['Categories', 'Description', 'Color'],
                   detail='Landmark')
    describe_image(url='/tmp/1200px-London-Eye-2009.JPG',
                   key=key,
                   visual_features=['Categories', 'Description', 'Color'],
                   detail='Landmark')
