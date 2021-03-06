#!/bin/bash
text=$1
filename=$2
speedup=$3

apiKey="Ocp-Apim-Subscription-Key: $(cat ../.bing_speech_api_key)"

authToken=`curl --header $apiKey --header "Content-Length:0" -X POST https://api.cognitive.microsoft.com/sts/v1.0/issueToken`

authHeader="Authorization:Bearer "$authToken

curl --header "$authHeader" --header "Content-Type:application/ssml+xml" --header "X-Microsoft-OutputFormat:audio-16khz-32kbitrate-mono-mp3" -d "<speak version='1.0' xml:lang='en-US'><voice xml:lang='en-US' xml:gender='Female' name='Microsoft Server Speech Text to Speech Voice (en-US, ZiraRUS)'><prosody rate='+$speedup%'>$text</prosody></voice></speak>" --verbose https://speech.platform.bing.com/synthesize -o "$2"
