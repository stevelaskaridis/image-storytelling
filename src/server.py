from flask import Flask
from flask import request
import urllib
import cv2
import numpy as np

app = Flask(__name__)


@app.route('/get_colours/', methods=['GET'])
def get_colours(show=False):
    data = request.args
    image_url = data['url']
    x = int(data['x'])
    y = int(data['y'])
    image_response = urllib.request.urlopen(image_url)
    img_array = np.array(bytearray(image_response.read()), dtype=np.uint8)
    image = cv2.imdecode(img_array, -1)
    h, w = image.shape[:2]
    image_r = cv2.resize(image, (x, y))
    top = image_r[0, :, :]
    right = image_r[:, -1, :]
    bottom = image_r[-1, :, :]
    left = image_r[:, 0, :]
    if show:
        bs = 100
        hbs = bs // 2
        image_b = np.zeros((h + bs, w + bs, 3), np.uint8)
        image_b[0:hbs, hbs:-hbs, :] = cv2.resize(top.reshape((1, x, 3)), (w, hbs), interpolation=cv2.INTER_NEAREST)
        image_b[-hbs:, hbs:-hbs, :] = cv2.resize(bottom.reshape((1, x, 3)), (w, hbs), interpolation=cv2.INTER_NEAREST)
        image_b[hbs:-hbs, :hbs, :] = cv2.resize(left.reshape((y, 1, 3)), (hbs, h), interpolation=cv2.INTER_NEAREST)
        image_b[hbs:-hbs, -hbs:, :] = cv2.resize(right.reshape((y, 1, 3)), (hbs, h), interpolation=cv2.INTER_NEAREST)
        image_b[hbs:-hbs, hbs:-hbs, :] = image
        cv2.imshow('a', image_b)
        cv2.waitKey(0)
    out = np.vstack((top, right))
    out = np.vstack((out, np.flip(bottom, axis=0)))
    out = np.vstack((out, np.flip(left, axis=0)))
    return np.array_str(out).replace('[', '').replace(']', '')
