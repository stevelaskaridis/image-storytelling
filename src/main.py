import bingGeolocation
from captioning import Caption
import darkskyWeather
import exifExtractor
import foursquareGeolocation
import msoftVisionReqs

import datetime

def assess_part_of_day_desc(timestamp):
    hour = datetime.datetime.strptime(timestamp, "%Y:%m:%d %H:%M:%S").hour
    if hour < 12 and hour > 6:
        return 'morning'
    elif hour < 17:
        return 'afternoon'
    elif hour < 20:
        return 'evening'
    else:
        return 'night'


def assess_part_of_month_desc(timestamp):
    day = datetime.datetime.strptime(timestamp, "%Y:%m:%d %H:%M:%S").day
    if day < 10:
        return 'early'
    elif day < 20:
        return 'mid'
    else:
        return 'late'


def assess_weather_desc(temperature_in_c):
    if temperature_in_c < 0:
        return 'freezing'
    elif temperature_in_c < 10:
        return 'cold'
    elif temperature_in_c < 20:
        return 'mild'
    elif temperature_in_c < 27:
        return 'warm'
    else:
        return 'hot'

def count_men_and_women(people):
    males_num = 0
    females_num = 0
    for person in people:
        if person['gender'].lower() == 'male':
            males_num += 1
        elif person['gender'].lower() == 'female':
            females_num += 1
        else:
            continue
    return males_num, females_num

def extract_celebrities(categories):
    names = []
    for category in categories:
        if category.get('detail'):
            if category['detail'].get('celebrities'):
                celebrities = category['detail']['celebrities']
                for celebrity in celebrities:
                    names.append(celebrity['name'])
                break
    return set(names)

def get_caption_from_image(url):
    # Microsoft Vision
    vision_key = msoftVisionReqs.load_subscription_key()
    vision_tags = msoftVisionReqs.describe_image(url=url, key=vision_key,
                                                 visual_features=['Categories', 'Description', 'Color', 'Tags', 'Faces'],
                                                 detail='landmark')
    people = vision_tags['faces']
    males, females = count_men_and_women(people)
    # EXIF tags
    exif_tags = exifExtractor.extract_exif_data(image_path)
    longitude = str(exif_tags['GPS GPSLongitude']).strip('[').strip(']').split(',')
    longitudeType = str(exif_tags['GPS GPSLongitudeRef'])
    longitude = '-'.join(longitude)+longitudeType
    latitude = str(exif_tags['GPS GPSLatitude']).strip('[').strip(']').split(',')
    longitudeType = str(exif_tags['GPS GPSLatitudeRef'])
    latitude = '-'.join(latitude)+longitudeType
    latitude, longitude = foursquareGeolocation.degrees_to_decimal(latitude, longitude)
    timestamp = str(exif_tags['EXIF DateTimeOriginal'])
    epoch_ts = darkskyWeather.date_to_timestamp(timestamp)

    # Foursquare geolocation
    foursquare_client_id, foursquare_client_secret = foursquareGeolocation.load_subscription_key()
    foursquare_tags = foursquareGeolocation.get_location_data(
        latitude=latitude,
        longitude=longitude,
        client_id=foursquare_client_id,
        client_secret=foursquare_client_secret,
        radius=100)

    darksky_key = darkskyWeather.load_subscription_key()
    weather_tags = darkskyWeather.get_weather_data(
        latitude=latitude,
        longitude=longitude,
        timestamp=epoch_ts,
        key=darksky_key)
    temperature = weather_tags['currently']['temperature']

    celebrities = extract_celebrities(vision_tags['categories'])
    if celebrities:
        # captioning
        caption_args = {
            'time_desc': assess_part_of_month_desc(timestamp),
            'month': datetime.datetime.strptime(timestamp, "%Y:%m:%d %H:%M:%S").strftime('%B'),
            'year': datetime.datetime.strptime(timestamp, "%Y:%m:%d %H:%M:%S").year,
            'region': foursquare_tags['response']['venues'][0]['location']['city'],
            'specific_location': foursquare_tags['response']['venues'][0]['name'],
            'msft_caption': vision_tags['description']['captions'][0]['text'],
            'weather_descriptor': assess_weather_desc(temperature),
            'part_of_day': assess_part_of_day_desc(timestamp),
            'women': females,
            'men': males,
            'celebrities': extract_celebrities(vision_tags['categories'])
        }
    else:
        caption_args = {
            'time_desc': assess_part_of_month_desc(timestamp),
            'month': datetime.datetime.strptime(timestamp, "%Y:%m:%d %H:%M:%S").strftime('%B'),
            'year': datetime.datetime.strptime(timestamp, "%Y:%m:%d %H:%M:%S").year,
            'region': foursquare_tags['response']['venues'][0]['location']['city'],
            'specific_location': foursquare_tags['response']['venues'][0]['name'],
            'msft_caption': vision_tags['description']['captions'][0]['text'],
            'weather_descriptor': assess_weather_desc(temperature),
            'part_of_day': assess_part_of_day_desc(timestamp),
            'women': females,
            'men': males,
        }

    cap_obj = Caption(**caption_args)
    print(cap_obj.get_caption())
