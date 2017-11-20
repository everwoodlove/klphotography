from __future__ import unicode_literals
import os
from datetime import *
from PIL import Image
from django.shortcuts import render

categories = {'Pets', 'Portraits', 'Automotive', 'Misc', 'Weddings'}

def home(request):
    photos = get_homepage_photos()
    if photos:
        context = {'photos': photos}
    else:
        context = {}

    print photos

    return render(request, 'website/home.html', context)

def pricing(request):
    return render(request, 'website/pricing.html')

def about(request):
    return render(request, 'website/about-me.html')

def contact(request):
    return render(request, 'website/contact.html')

def shoot(request, category, year, month, day, name):
    # Build URL from params
    # get all images in the folder, including in the preview folder
    # return them

    url = '/Users/bemmons/Documents/Nichole/klphotography/klphotography/klphotography/website/static/website/photos/' + category + '/' + month + '.' + day + '.' + year + '/' + name

    landscapes, portraits = get_all_photos(url)
    landscape_photos = []
    portrait_photos = []

    for photo in landscapes:
        # TODO remove this line when going to prod
        photo = photo.replace('/Users/bemmons/Documents/Nichole/klphotography/klphotography/klphotography/website/static/', '')
        landscape_photos.append(photo)

    for photo in portraits:
        # TODO remove this line when going to prod
        photo = photo.replace('/Users/bemmons/Documents/Nichole/klphotography/klphotography/klphotography/website/static/', '')
        portrait_photos.append(photo)

    context = {'landscapes': landscape_photos, 'portraits': portrait_photos}

    return render(request, 'website/shoot.html', context)

def gallery(request, category):
    url = 'website/gallery/'

    for cat in categories:
        if category == cat:
            url += cat + '.html'
            break

    context = {'photos': get_preview_photos(category, 3)}

    return render(request, url, context)

# Its ideal to have landscape photos be the full images
# and portraits to be the half images
# But what if we only have 1 portrait and 2 landscapes?

#TODO for home photos:
# parse through all directories and get most recent 6-7 shoots to display and pick first image of each in the preview folder
def get_homepage_photos():
    homepage_photos = []
    i = 0

    for category in categories:
        photo_set = get_preview_photos(category, 7)
        for photo in photo_set:
            if i == 0:
                name = 'landscapes'
            else:
                name = 'portraits'

            if photo.get(name, []):
                date = photo.get('date', '')
                date_split = date.split('.')

                if (len(date_split) is 3):
                    day = date_split[1]
                    month = date_split[0]
                    year = date_split[2]
                else:
                    day = ''
                    month = ''
                    year = ''

                shoot_photo = {'name': photo.get('name', ''), 'day': day, 'month': month, 'year': year,
                               'photo': photo.get(name, [''])[0],
                               'category': photo.get('category', ''), 'number': i}
                i += 1

                if i > 2:
                    i = 0

                homepage_photos.append(shoot_photo)

    return homepage_photos

def get_preview_photos(category, list_length):
    #TODO This won't work in prod!
    original_path = '/Users/bemmons/Documents/Nichole/klphotography/klphotography/klphotography/website/static/website/photos/' + category
    dates_directories = get_most_recent_folders_by_date(original_path)

    photos_to_return = []

    if dates_directories:
        for date in dates_directories:
            folder_path = original_path + '/' + date
            shoot_name_directories = os.listdir(folder_path)

            for shoot_name in shoot_name_directories:
                path = folder_path + '/' + shoot_name + '/preview'
                preview_photos = get_images(path)

                landscapes, portraits = sort_images(preview_photos)

                photo_set = {'name': shoot_name, 'date': date, 'landscapes': landscapes, 'portraits': portraits, 'category': category}
                photos_to_return.append(photo_set)

                if len(photos_to_return) > list_length:
                    break

            if len(photos_to_return) > list_length:
                break

    return photos_to_return

def get_all_photos(path):
    photo_set = []

    if os.path.isdir(path):
        photos = get_images(path)
        photo_set = photo_set + photos

    path = path + '/preview'

    if os.path.isdir(path):
        photos = get_images(path)
        photo_set = photo_set + photos

    landscapes, portraits = sort_images(photo_set)

    return landscapes, portraits

def get_most_recent_folders_by_date(path):
    if os.path.isdir(path):
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
    else:
        return []

def get_images(path):
    photos = []

    only_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    for file in only_files:
        if file.endswith(".png") or file.endswith(".jpg"):
            photo_path = os.path.join(path, file)
            photos.append(photo_path)

    return photos

def sort_images(images_list):
    landscapes = []
    portraits = []

    for image in images_list:
        im = Image.open(image)
        width, height = im.size

        # TODO remove this line when going to prod
        image = image.replace('/Users/bemmons/Documents/Nichole/klphotography/klphotography/klphotography/website/static/', '')
        if width > height:
            landscapes.append(image)
        else:
            portraits.append(image)

    return landscapes, portraits