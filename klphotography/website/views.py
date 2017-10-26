from __future__ import unicode_literals
import os
from datetime import *
from PIL import Image
from django.shortcuts import render
from klphotography import settings

def home(request):
    return render(request, 'website/home.html')

def pricing(request):
    return render(request, 'website/pricing.html')

def about(request):
    return render(request, 'website/about-me.html')

def contact(request):
    return render(request, 'website/contact.html')

def gallery(request, category):
    url = 'website/gallery/'

    if category == 'pets':
        url += 'pets.html'
    elif category == 'portraits':
        url += 'portraits.html'
    elif category == 'automotive':
        url += 'automotive.html'
    elif category == 'misc':
        url += 'misc.html'

    context = {'photos': get_gallery_preview_photos(category)}

    return render(request, url, context)

# Its ideal to have landscape photos be the full images
# and portraits to be the half images
# But what if we only have 1 portrait and 2 landscapes?


# TODO set containers on images to overflow: hidden and height: 50vh or maybe 80 for big images
# Set half landscapes no higher than 60
# Doesn't work on mobile --- might need 2 separate divs for this
# Then set background images via inline styling so that we can do
# background: url(bg_apple_little.gif) no - repeat center center; to center it

def get_gallery_preview_photos(category):
    #TODO THis won't work in prod!
    original_path = '/Users/bemmons/Documents/Nichole/klphotography/klphotography/klphotography/website/static/website/photos/' + category + '/'
    folders = get_most_recent_folders_by_date(original_path)

    photos_to_return = []

    for folder in folders:
        folder_path = original_path + '/' + folder
        directory_names = os.listdir(folder_path)

        for directory in directory_names:
            path = folder_path + '/' + directory + '/preview'
            preview_photos = get_images(path)

            landscapes, portraits = sort_images(preview_photos)

            photo_set = {'name': directory, 'landscapes': landscapes, 'portraits': portraits}
            photos_to_return.append(photo_set)

            if len(photos_to_return) > 2:
                break

        if len(photos_to_return) > 2:
            break

    return photos_to_return

def get_most_recent_folders_by_date(path):
    directory_names = os.listdir(path)

    dates_list = []

    for name in directory_names:
        date_split = name.split('.')

        if (len(date_split) is 3):
            folderDate = datetime(int(date_split[2]), int(date_split[0]), int(date_split[1]))
            dates_list.append(folderDate)

    folders_to_use = []
    now = datetime.today()

    list_length = len(dates_list)


    for i in xrange(list_length):
        youngest = max(dt for dt in dates_list if dt < now)

        folders_to_use.append(youngest)
        dates_list.remove(youngest)

    folders = []

    for i in xrange(list_length):
        folders.append(folders_to_use[i].strftime('%m.%d.%Y'))

    return folders

def get_images(path):
    photos = []

    only_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    for file in only_files:
        if file.endswith(".png") or file.endswith(".jpg"):
            photos.append(os.path.join(path, file))

    return photos

def sort_images(images_list):
    landscapes = []
    portraits = []

    for image in images_list:
        im = Image.open(image)
        width, height = im.size
        if width > height:
            landscapes.append(image)
        else:
            portraits.append(image)

    return landscapes, portraits
