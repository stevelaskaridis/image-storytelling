zero_to_twenty = {
    '1': 'one',
    '2': 'two',
    '3': 'three',
    '4': 'four',
    '5': 'five',
    '6': 'six',
    '7': 'seven',
    '8': 'eight',
    '9': 'nine',
    '10': 'ten',
    '11': 'eleven',
    '12': 'twelve',
    '13': 'thirteen',
    '14': 'fourteen',
    '15': 'fifteen',
    '16': 'sixteen',
    '17': 'seventeen',
    '18': 'eighteen',
    '19': 'ninetee'
}

def num_as_word(num_string):
    if type(num_string) != type(''):
        num_string = str(num_string)
    if num_string in zero_to_twenty:
        return zero_to_twenty[num_string]
    else:
        return num_string