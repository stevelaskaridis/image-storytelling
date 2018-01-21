# import requests
# import base64
# import uuid
# import http.client

# DEBUG = True

# # these need to be hex only
# app_id = '72ca7ecd-1bc9-4d2f-a20a-2fd983c7860e'
# instance_id = str(uuid.uuid4())

# def load_subscription_key(path='../.azure_speech_api_key'):
#     with open(path, 'r') as f:
#         key = f.read().splitlines()[0]
#     return key

# # returns a byte string that is the authorization identifier
# def get_authorization_from_key(key):
#     endpoint = 'https://api.cognitive.microsoft.com/sts/v1.0/issueToken'
#     headers = {
#         'Ocp-Apim-Subscription-Key': key,
#         'Content-Length': 0
#     }
#     try:
#         conn = http.client.HTTPSConnection('api.cognitive.microsoft.com', 443)
#         conn.request(method="POST", url='/sts/v1.0/issueToken', headers=headers, body="")
#         response = conn.getresponse()
#         return response.read()

#         # response = requests.post(url='',
#         #                         headers = headers,
#         #                         body=""
#         #                         )
#         # authorization = response.content
#         # print(authorization)
#         # return authorization
#     except requests.RequestException as e:
#         print("[Errno {0}] {1}".format(e.errno, e.strerror))
#         raise Exception("Could not retrieve authorization from speech key")




# def text_to_speech(key, text, endpoint_url='https://speech.platform.bing.com/synthesize'):
#     # get b'' type authorization
#     authToken = get_authorization_from_key(key)

#     #auth = base64.b64encode(("Bearer " + authorization).encode())
#     auth = "Bearer " + authToken


#     headers = {
#         # Request headers.
#         'Content-Type': 'application/ssml+xml',

#         'X-Search-AppId': app_id,   # NOTE: hex only
#         'X-Search-ClientID': instance_id,   #NOTE: hex only
#         'User-Agent': 'HackCambridge2018',
#         'Authorizaton': auth,
#         'X-Microsoft-OutputFormat': 'audio-16khz-32kbitrate-mono-mp3'
#     }

#     ssml = """<speak version='1.0' xml:lang='en-US'><voice xml:lang='en-US' xml:gender='Female' name='Microsoft Server Speech Text to Speech Voice (en-US, ZiraRUS)'>Hello world</voice></speak>""".format(text)

#     body = {
#         'data': ssml
#     }

#     try:
#         response = requests.post(url = endpoint_url,
#                                 headers = headers,
#                                 json = body
#                                 )
#         print(response)
#     except requests.RequestException as e:
#         print("[Errno {0}] {1}".format(e.errno, e.strerror))

import subprocess
import os

def text_to_speech(text, filename, speedup=30):
    if not filename.endswith('.mp3'):
        filename += '.mp3'
    subprocess.call(['./msft_speech_download.sh "{0}" "{1}" "{2}"'.format(text, filename, speedup)], shell=True)

if __name__ == '__main__':
    text_to_speech("This photo was taken in early January 2016 in London. The London Eye is nearby. There is a large ferris wheel by a river. It was a hot afternoon. There is one woman and one man facing the camera.", "caption_1.mp3")
