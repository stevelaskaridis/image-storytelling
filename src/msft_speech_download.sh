#!/bin/bash

text=$1
filename=$2

apiKey="Ocp-Apim-Subscription-Key:fa1a1cd6b1f2454087a43290a07671b8"

authToken=`curl --header $apiKey --header "Content-Length:0" -X POST https://api.cognitive.microsoft.com/sts/v1.0/issueToken`

authHeader="Authorization:Bearer "$authToken

curl --header "$authHeader" --header "Content-Type:application/ssml+xml" --header "X-Microsoft-OutputFormat:audio-16khz-32kbitrate-mono-mp3" -d "<speak version='1.0' xml:lang='en-US'><voice xml:lang='en-US' xml:gender='Female' name='Microsoft Server Speech Text to Speech Voice (en-US, ZiraRUS)'>$text</voice></speak>" https://speech.platform.bing.com/synthesize -o $2