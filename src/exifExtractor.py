import exifread

DEBUG=True

def extract_exif_data(image_path):
    # Open image file for reading (binary mode)
    image = open(image_path, 'rb')

    # Return Exif tags
    tags = exifread.process_file(image)

    if DEBUG:
        if tags:
            import pprint
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(tags)
        else:
            print("No EXIF tags found")

    return tags

if __name__ == '__main__':
    extract_exif_data('../data/s7_image_2.jpg')
