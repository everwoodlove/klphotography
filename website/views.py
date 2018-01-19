from __future__ import unicode_literals
import os
from datetime import *
from PIL import Image
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.shortcuts import render
from klphotography.settings import PROJECT_ROOT

categories = {'Pets', 'Portraits', 'Automotive', 'Misc', 'Weddings'}

BASE_URL = 'website/photos/'

def home(request):
    photos = get_homepage_photos()
    if photos:
        context = {'photos': photos}
    else:
        context = {}

    return render(request, 'website/home.html', context)

def blog(request):
    return render(request, 'website/blog.html')

def about(request):
    return render(request, 'website/about-me.html')

def faqs(request):
    return render(request, 'website/faqs.html')

def shoot(request, category, year, month, day, name):
    # Build URL from params
    # get all images in the folder, including in the preview folder
    # return them

    partial_url = static(BASE_URL + category + '/' + month + '.' + day + '.' + year + '/' + name).lower()
    url = PROJECT_ROOT + partial_url
    print url

    landscapes, portraits = get_all_photos(url)

    context = {'landscapes': landscapes, 'portraits': portraits}

    return render(request, 'website/shoot.html', context)

def gallery(request, category):
    url = 'website/gallery/'

    for cat in categories:
        if category == cat.lower():
            url += cat.lower() + '.html'
            break

    preview_photos = get_preview_photos(category, 3)
    photos = categorize_photos(preview_photos)

    context = {'photos': photos}

    return render(request, url, context)


def get_homepage_photos():
    homepage_photos = []
    i = 0

    for category in categories:
        photo_set = get_preview_photos(category, 7)
        homepage_photos = categorize_photos(photo_set)

    return homepage_photos


def categorize_photos(photo_set):
    i = 0
    photoset = []

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

            photoset.append(shoot_photo)

    return photoset


def get_preview_photos(category, list_length):
    partial_path = static(BASE_URL + category).lower()
    original_path = PROJECT_ROOT + partial_path
    dates_directories = get_most_recent_folders_by_date(original_path)

    print dates_directories

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
    print os.path.exists(path)

    if os.path.exists(os.path.dirname(path)):
        print 'hello?'

    if os.path.isdir(path):
        print 'true!'
        photos = get_images(path)
        photo_set = photo_set + photos

    path = path + '/preview'

    if os.path.isdir(path):
        print 'true~'
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

        image = image.replace(PROJECT_ROOT + '/staticfiles/', '')

        if width > height:
            landscapes.append(image)
        else:
            portraits.append(image)

    return landscapes, portraits