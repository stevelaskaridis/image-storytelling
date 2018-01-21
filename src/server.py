from flask import Flask, request, send_file
import urllib
#import cv2
import numpy as np
import main
import os
import random

app = Flask(__name__, static_url_path='')
#app.run(host='0.0.0.0', port=80)
#app.config["APPLICATION_ROOT"] = '/app'

@app.route('/get_pic_url/')
def get_pic_url():
    return 'https://source.unsplash.com/random'


images = {}
captions = {}
audio = {}

# files = os.listdir('../data/')
# filemame = random.choice(files)
# caption = main.get_caption_from_image(filename)
# with open(filename,'rb') as f:
#     image = read(f)

def validate_image_or_random(image_id):
    images = os.listdir('../data')
    if "image_{}.jpg".format(image_id) in images:
        return image_id
    else:
        return random.choice(images).split('_')[1].split('.')[0]

@app.route('/get_caption/<id>')
def get_caption(id):
    image_id = id
    caption = main.get_caption_from_image("../data/image_{}.jpg".format(image_id))
    return caption


@app.route('/get_audio/<id>')
def get_audio(id):
    image_id = id
    main.audio_from_caption(id="../data/caption_{}.mp3".format(id), caption=get_caption(id))
    return send_file("../data/caption_{}.mp3".format(id), mimetype='audio/mpeg')

@app.route('/get_image/<id>')
def get_image(id):
    #image_id = request.args.get('id')
    image_id = id
    image_id = validate_image_or_random(image_id)
    return send_file("../data/image_{}.jpg".format(image_id), mimetype='image/jpg')


# @app.route('/get_colours/', methods=['GET'])
# def get_colours(show=False):
#     data = request.args
#     image_url = data['url']
#     x = int(data['x'])
#     y = int(data['y'])
#     image_response = urllib.request.urlopen(image_url)
#     img_array = np.array(bytearray(image_response.read()), dtype=np.uint8)
#     image = cv2.imdecode(img_array, -1)
#     h, w = image.shape[:2]
#     image_r = cv2.resize(image, (x, y))
#     top = image_r[0, :, :]
#     right = image_r[:, -1, :]
#     bottom = image_r[-1, :, :]
#     left = image_r[:, 0, :]
#     if show:
#         bs = 100
#         hbs = bs // 2
#         image_b = np.zeros((h + bs, w + bs, 3), np.uint8)
#         image_b[0:hbs, hbs:-hbs, :] = cv2.resize(top.reshape((1, x, 3)), (w, hbs), interpolation=cv2.INTER_NEAREST)
#         image_b[-hbs:, hbs:-hbs, :] = cv2.resize(bottom.reshape((1, x, 3)), (w, hbs), interpolation=cv2.INTER_NEAREST)
#         image_b[hbs:-hbs, :hbs, :] = cv2.resize(left.reshape((y, 1, 3)), (hbs, h), interpolation=cv2.INTER_NEAREST)
#         image_b[hbs:-hbs, -hbs:, :] = cv2.resize(right.reshape((y, 1, 3)), (hbs, h), interpolation=cv2.INTER_NEAREST)
#         image_b[hbs:-hbs, hbs:-hbs, :] = image
#         cv2.imshow('a', image_b)
#         cv2.waitKey(0)
#     out = np.vstack((top, right))
#     out = np.vstack((out, np.flip(bottom, axis=0)))
#     out = np.vstack((out, np.flip(left, axis=0)))
#     return np.array_str(out).replace('[', '').replace(']', '')

# Xn = 95.047
# Yn = 100.0
# Zn = 108.883
# EPSILON = 0.008856
# KAPPA = 903.3


# def rgb_to_xyz(R, G, B):
#     R = pivotRgb(R / 255)
#     G = pivotRgb(G / 255)
#     B = pivotRgb(B / 255)
#     X = R * 0.4124 + G * 0.3576 + B * 0.1805
#     Y = R * 0.2126 + G * 0.7152 + B * 0.0722
#     Z = R * 0.0193 + G * 0.1192 + B * 0.9505
#     return X, Y, Z


# def xyz_to_rgb(X, Y, Z):
#     X /= 100
#     Y /= 100
#     Z /= 100
#     R = X * 3.2406 + Y * -1.5372 + Z * -0.4986
#     G = X * -0.9689 + Y * 1.8758 + Z * 0.0415
#     B = X * 0.0557 + Y * -0.2040 + Z * 1.0570
#     R = 1.055 * pow(R, 1 / 2.4) - 0.055 if R > 0.0031308 else 12.92 * R
#     G = 1.055 * pow(G, 1 / 2.4) - 0.055 if G > 0.0031308 else 12.92 * G
#     B = 1.055 * pow(B, 1 / 2.4) - 0.055 if B > 0.0031308 else 12.92 * B
#     return toRgb(R), toRgb(G), toRgb(B)


# def toRgb(n):
#     result = 255.0 * n
#     if (result < 0):
#         return 0
#     if (result > 255):
#         return 255
#     return result


# def pivotRgb(n):
#     return pow((n + 0.055) / 1.055, 2.4) if n > 0.04045 else (n / 12.92) * 100.0


# def pivotXyz(n):
#     return pow(n, (1 / 3)) if n > EPSILON else (KAPPA * n + 16) / 116


# def xyz_to_lab(X, Y, Z):
#     X = pivotXyz(X / Xn)
#     Y = pivotXyz(Y / Yn)
#     Z = pivotXyz(Z / Zn)
#     return max(0, 116.0 * Y - 16.0), 500.0 * (X - Y), 200.0 * (Y - Z)


# def lab_to_xyz(L, A, B):
#     Y = (L + 16) / 116
#     X = A / 500 + Y
#     Z = Y - B / 200
#     X3 = pow(X, 3)
#     Z3 = pow(Z, 3)
#     X = Xn * (X3 if X3 > EPSILON else (X - 16 / 116) / 7.787)
#     Y = Yn * (pow(((L + 16.0) / 116.0), 3) if L > KAPPA * EPSILON else L / KAPPA)
#     Z = Zn * (Z3 if Z3 > EPSILON else (Z - 16 / 116) / 7.787)
#     return X, Y, Z


# def rgb_to_lab(R, G, B):
#     X, Y, Z = rgb_to_xyz(R, G, B)
#     return xyz_to_lab(X, Y, Z)


# def lab_to_rgb(L, A, B):
#     X, Y, Z = lab_to_xyz(L, A, B)
#     return xyz_to_rgb(X, Y, Z)


# def normalise_rgb(R, G, B, goal_l):
#     _, A, B = rgb_to_lab(R, G, B)
#     L = goal_l
#     return lab_to_rgb(L, A, B)


# R, G, B = normalise_rgb(255, 0, 0, 75)
# print(R, G, B)
# R, G, B = normalise_rgb(0, 255, 0, 75)
# print(R, G, B)
# R, G, B = normalise_rgb(0, 0, 255, 75)
# print(R, G, B)
