import random
import nltk
# import num2word

# Starting template:
#   General:
#       This photo was taken in [[early, mid, late], Month] in [large location], near [specific place].
#   Specific scene:
#       ALT 1: There is [msoft vision caption that begins with a 'determiner' (a, an, etc.) and singular noun]
#       ALT 2: There are [vision caption beginning with plural noun]
#   Weather:
#       ALT 1 - condition weather matches trend: It was a [descriptor] [morning, day, afternoon, evening, night]
#       ---ALT 2 - condition unusual weather:  At this time of year, it's usually [freezing, cold, mild, warm, hot], but surprisingly it was [weather rounded to 2C].
#
#   OPT:
#       Faces: There is a group of [x] women and [n] men.
#       condition celebrities:  One of these is [name]
#   -- OPT:
#   --  condition (people): People are [action tag -- standing, running, ... if stem form NOT in msft vision caption stem forms]


DEBUG = False

class Caption:
    # set of starting sentences with templates arguments
 
    """
        arguments:
            time_desc:      eg early, mid, late (march)
            month:          month
            year:           year
            region:      Geolocation API region (admindistrict2)
            specific_location:  Foursquare point of interest if there is one, by GPS coordinates
            msft_caption:       Microsoft vision API caption
            weather_descriptor: eg. freezing, cold, mild, warm, hot
            part_of_day:        eg. morning, day, afternoon, evening, night
            --expected_weather_descriptor: descriptor taken from actual weather at the time
            --actual_temp:        actual temperature from the day, time, location
            women:          Number of women in the image (msft faces, if available)
            men:            Number of men in the image (msft faces, if available)
            celebrities:    List of celibrities by name (or just one)
    """


    general = [
        "This photo was taken in {time_desc} {month} {year} in {region}",
        "From ({time_desc}) {month} {year} in {region}", 
        "{region} - {time_desc} {month} {year}"
    ]

    location_landmark = [
        "The {specific_location} is nearby"
    ]

    msft_caption_singular = [
        "There is {msft_caption}"
    ]
    msft_caption_plural = [
        "There are {msft_caption}"
    ]

    weather_normal = [
        "It was a {weather_descriptor} {part_of_day}"
    ]
#    weather_unusual = [
#        "At this time of year, it's usually [expected_weather_descriptor], but surprisingly it was [actual_temp]"
#    ]

    faces_singlar = [
        "There is {women} women and {men} men facing the camera"
    ]

    faces_plural = [
        "There are {women} and {men} facing the camera"
    ]

    celebrities_singular = [
        "{celebrities} is one of them"
    ]
    celebrities_plural = [
        "{celebrities} are among them them"
    ]

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def get_caption(self):
        order = [
                    self._get_general, 
                    self._get_location_landmark, 
                    self._get_msft_caption,
                    self._get_weather_normal,
                    self._get_faces,
                    self._get_celebrities
                ]

        caption_sentences = []
        for getter in order:
            sentence = getter()
            if sentence is not None:
                caption_sentences.append(sentence)
        caption = ". ".join(caption_sentences)
        return caption + "."


    def _fill(self, template, **override_kwargs):
        # merge in other values from self.kwargs
        for (key, val) in self.kwargs.items():
            if key not in override_kwargs:
                override_kwargs[key] = val
        try:
            filled = template.format(**override_kwargs)
            return filled
        except KeyError as e:
            if DEBUG:
                print("Cannot fill template {0} with kwargs".format(template))
            print("Missing key: " + str(e))
            return None

    def _get_general(self):
        template = random.choice(Caption.general)
        filled = self._fill(template)
        return filled

    def _get_location_landmark(self):
        template = random.choice(Caption.location_landmark)
        filled = self._fill(template)
        return filled

    def _get_msft_caption(self):
        msft_caption = self.kwargs["msft_caption"]
        tokenized = msft_caption.split(' ')
        pos = nltk.pos_tag(tokenized)

        # singular
        if pos[0][1] == 'DT':       # determinant, such as 'a', 'an'
            template = random.choice(Caption.msft_caption_singular)
        
        elif pos[0][1] == 'NNS' or pos[0][1] == 'NNPS':
            template = random.choice(Caption.msft_caption_plural)
        
        else:
            print("Caption does not start with determinant or plural noun: ")
            print(" ", msft_caption)
            print(" Parts of speech: ", pos)
            print(" Defaulting to singular")
            template = random.choice(Caption.msft_caption_singular)
        
        filled = self._fill(template)
        return filled

    def _get_weather_normal(self):
        template = random.choice(Caption.weather_normal)
        filled = self._fill(template)
        return filled

    def _get_faces(self):
        try:
            women = self.kwargs['women']
        except KeyError:
            if DEBUG:
                print("**Women key not present in kwargs")
            return None
        if int(women) == 1:
            template = random.choice(Caption.faces_singlar)
            filled = self._fill(template) #, women=num2word(women))
        elif int(women) > 1:
            template = random.choice(Caption.faces_plural)
            filled = self._fill(template) #, women=num2word(women))
        return filled

    def _get_celebrities(self):
        try:
            celebrities_list = self.kwargs["celebrities"]
        except KeyError:
            if DEBUG:
                print("**Celebrities not present in kwargs")
            return None
        
        assert len(celebrities_list > 0), "Celebrities list is length 0 but key exists"
        if len(celebrities_list) == 1:
            template = random.choice(Caption.celebrities_singular)
            filled = self._fill(template, celebrities=celebrities_list[0])
        else:
            template = random.choice(Caption.celebrities_plural)
            celebrities = ", ".join(celebrities_list[:-1])
            celebrities += " and " + celebrities_list[-1]
            filled = self._fill(template, celebrities=celebrities)
        return filled





test_args = {
    "time_desc":    "early",
    "month":        "January",
    "year":         "2016",
    "region":       "London",
    "specific_location":    "London Eye",
    "msft_caption": "a large ferris wheel by a river",
    "weather_descriptor":   "hot",
    "part_of_day":      "afternoon",
    "women":    1,
    "men":      1
}

if __name__ == "__main__":
    captioner = Caption(**test_args)
    print(captioner.get_caption())