import os
from pprint import pprint
import statistics


def has_images(n):
    return "0B" not in n


def split_and_convert(n):

    split_list = n.split()
    namespace = split_list[0].split('/')[0]
    if "-tools" in namespace or "-dev" in namespace or "-test" in namespace or "-prod" in namespace:
        namespace = namespace[:6]  # get the license plate

    image_name = split_list[0].split('/')[1]

    size = split_list[1][:len(split_list[1])-1]  # cut off the 'B'

    if size[len(size)-2:] == "Gi":  # if it's already in gigs, cut off the Gi
        size = size[:len(size)-2]
    elif size[len(size)-2:] == "Mi":  # if it's in megs, cut off the Mi and convert to gigs
        megs = size[:len(size)-2]
        gigs = float(megs)/1024
        size = str(gigs)
    else:  # if it's anything else, it's too small to care about
        size = 0
    return_list = [namespace, image_name, size]
    return return_list


def get_image_streams():
    stream = os.popen('oc adm top imagestreams')
    output = stream.readlines()
    output = output[1:]
    image_list = list(map(split_and_convert, filter(has_images, output)))
    image_dict = {}
    for image in image_list:
        if image[0] in image_dict:
            image_dict[image[0]] += float(image[2])
        else:
            image_dict[image[0]] = float(image[2])
        #image_dict[image[0]] = round(image_dict[image[0]])
    pprint(image_dict)
    mean = sum(image_dict.values()) / len(image_dict)
    median = statistics.median(image_dict.values())
    maxi = max(image_dict.values())
    print("Mean: " + str(mean))
    print("Median: " + str(median))
    print("Max: " + str(maxi))


get_image_streams()
